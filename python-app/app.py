import os
import sys

from flask import Flask, request
import requests

app = Flask(__name__)

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://host.docker.internal:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3")
DEFAULT_NAMESPACE = os.getenv("DEFAULT_NAMESPACE", "monitoring")


def get_k8s_client():
    from kubernetes import client, config

    try:
        config.load_incluster_config()
    except config.ConfigException:
        config.load_kube_config()
    return client.CoreV1Api()


def list_pods_in_namespace(namespace):
    try:
        api = get_k8s_client()
        pods = api.list_namespaced_pod(namespace=namespace).items
        return [pod.metadata.name for pod in pods if pod.status.phase == "Running"]
    except Exception as exc:
        print(f"Failed to list pods in {namespace}: {exc}", flush=True)
        return []


def get_logs(namespace, pod):
    if not pod:
        running_pods = list_pods_in_namespace(namespace)
        if not running_pods:
            return "No running pods found in namespace"
        pod = running_pods[0]
        print(f"No pod label on alert; using first running pod: {pod}", flush=True)

    try:
        api = get_k8s_client()
        return api.read_namespaced_pod_log(
            name=pod,
            namespace=namespace,
            tail_lines=20,
        )
    except Exception as exc:
        print(f"Failed to fetch logs for {namespace}/{pod}: {exc}", flush=True)
        return f"No logs available: {exc}"


def analyze_with_ai(alert_name, logs):
    prompt = f"""You are a Kubernetes SRE assistant.

Alert: {alert_name}

Logs:
{logs}

1. What is the likely root cause?
2. What is the safest remediation action?
"""

    try:
        response = requests.post(
            f"{OLLAMA_URL.rstrip('/')}/api/generate",
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False,
            },
            timeout=120,
        )
        response.raise_for_status()
        return response.json()["response"]
    except Exception as exc:
        return f"Error contacting AI at {OLLAMA_URL}: {exc}"


@app.route("/health", methods=["GET"])
def health():
    return "OK", 200


@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(silent=True) or {}

    print("\n===== RAW ALERT DATA =====", flush=True)
    print(data, flush=True)

    alerts = data.get("alerts", [])
    if not alerts:
        print("Webhook received with no alerts", flush=True)
        return "OK", 200

    for alert in alerts:
        labels = alert.get("labels", {})
        name = labels.get("alertname", "unknown")
        pod = labels.get("pod", "")
        namespace = labels.get("namespace", DEFAULT_NAMESPACE)

        print(f"\nProcessing alert: {name} (namespace={namespace}, pod={pod or 'auto'})", flush=True)

        logs = get_logs(namespace, pod)
        print("\n===== POD LOGS =====", flush=True)
        print(logs, flush=True)

        result = analyze_with_ai(name, logs)
        print("\n===== INCIDENT ANALYSIS =====", flush=True)
        print(result, flush=True)

    return "OK", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
