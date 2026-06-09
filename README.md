# AI-Powered Kubernetes Incident Response Platform

[![AWS](https://img.shields.io/badge/AWS-EKS-FF9900?logo=amazonaws&logoColor=white)](https://aws.amazon.com/eks/)
[![Kubernetes](https://img.shields.io/badge/Kubernetes-1.34-326CE5?logo=kubernetes&logoColor=white)](https://kubernetes.io/)
[![Terraform](https://img.shields.io/badge/Terraform-IaC-844FBA?logo=terraform&logoColor=white)](https://www.terraform.io/)
[![Prometheus](https://img.shields.io/badge/Prometheus-Monitoring-E6522C?logo=prometheus&logoColor=white)](https://prometheus.io/)
[![Python](https://img.shields.io/badge/Python-Flask-3776AB?logo=python&logoColor=white)](https://flask.palletsprojects.com/)
[![AI](https://img.shields.io/badge/AI-Ollama%20%7C%20LLaMA3-412991)](https://ollama.com/)

---

## Overview

**IncidentWire project** is a production-style DevOps capstone project that demonstrates how to build a **fully automated monitoring and incident-response workflow** on **Amazon Elastic Kubernetes Service (EKS)**.

The platform:

1. **Provisions cloud infrastructure** using modular Terraform (VPC, IAM, EKS cluster, worker nodes)
2. **Deploys workloads** into a dedicated `monitoring` namespace
3. **Collects metrics** via the Prometheus Operator (kube-prometheus-stack)
4. **Fires alerts** when thresholds are breached (e.g., high CPU, pod restarts)
5. **Routes alerts** from Alertmanager to a custom webhook service — **IncidentWire**
6. **Automatically pulls pod logs** using the Kubernetes API (in-cluster authentication)
7. **Analyzes incidents with AI** (Ollama + LLaMA 3) and suggests root cause and remediation

This project bridges **Infrastructure as Code**, **Kubernetes operations**, **observability**, and **AI-assisted SRE workflows** — a combination increasingly sought after in modern platform and DevOps engineering roles.

---

## Problem Statement

In real-world production environments, on-call engineers often face alert fatigue. Multiple alerts can fire simultaneously, but identifying the root cause requires manual correlation of logs, metrics, and system events.

Traditional monitoring systems:
- Detect failures
- Send alerts
- Require manual debugging

This project addresses that gap by automating the analysis phase.

---

## Solution

IncidentWire introduces a closed-loop incident response system:

Alert → Correlate signals → Analyze → Suggest remediation

Instead of just notifying engineers, the system:
- Collects logs and alert metadata
- Uses AI to interpret the issue
- Suggests root cause and next actions

---

## Architecture

![IncidentWire Architecture](application/incidentwire.jpeg)
---

## Technology Stack

| Layer | Technologies |
|-------|-------------|
| **Cloud** | Amazon Web Services (EKS, VPC, IAM, EC2, S3) |
| **IaC** | Terraform 1.14+, AWS Provider 6.40.0 |
| **Orchestration** | Kubernetes 1.34 |
| **Monitoring** | Prometheus Operator, kube-prometheus-stack, Alertmanager |
| **Alerting** | PromQL, PrometheusRule CRDs |
| **Application** | Python 3.11, Flask, Kubernetes Python Client |
| **AI** | Ollama, LLaMA 3 |
| **Containers** | Docker, Docker Hub |
| **Languages** | HCL, YAML, Python |

---

## Key Features

- **Modular Terraform** — VPC, IAM, EKS, and node group split into reusable modules
- **Remote state management** — S3 backend with lockfile support for team-safe deployments
- **Multi-AZ networking** — Public subnets across `us-east-1a` and `us-east-1b`
- **Custom Prometheus alerting** — Pod-level CPU and restart detection with rich labels
- **Alertmanager webhook integration** — Routes all alerts to IncidentWire automatically
- **Automated log correlation** — Pulls logs for the exact pod named in the alert
- **AI-assisted triage** — LLM analyzes alert + logs and recommends safe remediation
- **Kubernetes-native auth** — In-cluster ServiceAccount with scoped RBAC (no `kubectl` binary required)
- **Health probes** — Liveness and readiness checks on the incident engine
- **Configurable AI backend** — `OLLAMA_URL` and `OLLAMA_MODEL` environment variables

---

## Project Structure

```
monitor-eks/
│
├── terraform/                      # Root Terraform configuration
│   ├── main.tf                     # Wires VPC, IAM, EKS, and node modules
│   ├── variables.tf                # Cluster name, region, node sizing
│   └── providers.tf                # AWS provider + S3 remote backend
│
├── modules/
│   ├── vpc/                        # VPC, subnets, IGW, route tables
│   ├── iam/                        # EKS cluster and worker node IAM roles
│   ├── eks/                        # EKS control plane
│   └── node-group/                 # Managed worker node group
│
├── python-app/                     # IncidentWire — AI incident engine
│   ├── app.py                      # Flask webhook, log fetcher, AI analyzer
│   └── Dockerfile                  # Container image definition
│
└── application/                    # Kubernetes manifests
    ├── app-deployment.yaml         # Sample workload (my-app)
    ├── app-service.yaml            # ClusterIP service for sample app
    ├── incident-deployment.yaml    # IncidentWire deployment
    ├── incident-service.yaml       # IncidentWire ClusterIP service
    ├── incident-rbac.yaml          # ServiceAccount, Role, RoleBinding
    ├── alert-rules.yaml            # PrometheusRule custom alerts
    ├── alertmanager-values.yaml    # Alertmanager → webhook routing
    └── docker-secret.yaml          # Image pull secret (do not commit real credentials)
```

---

## Implementation Steps

### 1. Infrastructure Setup
- Provisioned AWS EKS cluster using Terraform
- Configured node groups (t3.small for adequate resources)

### 2. Application Deployment
- Deployed sample application using Kubernetes Deployment and Service
- Verified pod health and service accessibility

### 3. Monitoring Setup
- Installed kube-prometheus-stack via Helm
- Verified Prometheus targets and Grafana dashboards

### 4. Alerting Configuration
- Created custom Prometheus alert rules
- Configured Alertmanager for alert routing

### 5. Incident Engine Deployment
- Built Python-based webhook service
- Containerized using Docker
- Deployed in Kubernetes

### 6. AI Integration
- Installed Ollama locally
- Integrated LLM into incident engine
- Enabled real-time AI-based analysis

### 7. End-to-End Testing
- Simulated CPU stress using test pods
- Verified alert triggering
- Confirmed webhook invocation
- Observed AI-generated incident analysis
---

## Challenges Faced

- ImagePullBackOff due to private Docker repositories
- ARM vs AMD64 architecture mismatch on EKS nodes
- Alertmanager webhook configuration issues
- Kubernetes networking and service discovery debugging
- Alert lifecycle understanding (event-based vs continuous)

---

## Key Learnings

- Deep understanding of Kubernetes networking and debugging
- Prometheus and Alertmanager architecture
- Handling container image compatibility across architectures
- Designing event-driven systems
- Integrating AI into infrastructure workflows
- Real-world SRE practices such as incident triage

---

## Skills Demonstrated

This project is designed to showcase competencies relevant to **DevOps Engineer**, **Platform Engineer**, **SRE**, and **Cloud Engineer** roles:

- **Infrastructure as Code** — Modular Terraform, remote state, AWS resource orchestration
- **Container orchestration** — Kubernetes deployments, services, probes, namespaces
- **Observability engineering** — Prometheus metrics, PromQL, Alertmanager routing
- **Incident automation** — Event-driven webhook pipelines
- **Cloud security** — IAM roles, RBAC, scoped ServiceAccounts
- **Software development** — Python microservice, REST API, Docker packaging
- **AI/ML integration** — LLM prompt design for operational use cases
- **Networking** — VPC design, multi-AZ subnets, in-cluster service discovery
- **CI/CD readiness** — Containerized apps, infrastructure reproducibility
---

## Future Enhancements

- [ ] GitHub Actions pipeline for Terraform plan/apply and Docker image builds
- [ ] In-cluster Ollama Helm chart deployment
- [ ] Slack / PagerDuty notification integration alongside AI analysis
- [ ] Grafana dashboards for alert and incident metrics
- [ ] Support for OpenAI / Anthropic APIs as alternative LLM backends
- [ ] Persistent incident history store (PostgreSQL or DynamoDB)
- [ ] Horizontal Pod Autoscaler for IncidentWire under high alert volume
- [ ] NetworkPolicies to restrict incident-engine egress
- [ ] Terraform outputs for cluster endpoint and kubeconfig helpers

---

<p align="center">
  <strong>Built with AWS · Kubernetes · Terraform · Prometheus · Python · AI</strong><br/>
  <em>Turning alerts into actionable intelligence automatically.</em>
</p>

