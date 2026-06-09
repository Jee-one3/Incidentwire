FROM python:3.11-slim

WORKDIR /app

COPY app.py .

RUN pip install --no-cache-dir flask requests kubernetes

CMD ["python", "app.py"]
