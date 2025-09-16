# OTEL-LGTM Demo


## How the Services Work

- **service1** receives an HTTP request and calls **service2**.
- **service2** processes the request and calls **service3**.
- **service3** returns a result to **service2**, which then returns it to **service1**.
- After **service1** gets the final response, it produces a message to a Kafka topic.
- **service4** consumes messages from that Kafka topic and processes them.

### OTEL Integration

For this test, I used OTEL zero-code instrumentation by installing the OpenTelemetry instrumentation package:

```bash
pip install opentelemetry-distro opentelemetry-exporter-otlp
opentelemetry-bootstrap -a install
```

Run the services with the `opentelemetry-instrument` command:

```bash
export OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED=true
opentelemetry-instrument \
    --metrics_exporter otlp \
    --traces_exporter otlp \
    --logs_exporter otlp \
    --service_name fastapi-service-1 \
    uvicorn service1.main:app --port 8001 
```

**Notes:**  
- You can run all services using the `run.sh` script.
- For Kafka integration, I used the `opentelemetry-instrumentation-kafka` package (just install it).

---

### Usage

Run Containers:
```bash
docker-compose up -d
```
Install requirements:
```bash
pip install -r requirements.txt
```

Run all services:
```bash
./run.sh
```