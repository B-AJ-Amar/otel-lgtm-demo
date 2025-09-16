#!/bin/bash
# Run all FastAPI microservices in separate terminals

opentelemetry-instrument \

# Start service3
export OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED=true
opentelemetry-instrument \
    --metrics_exporter otlp \
    --traces_exporter otlp \
    --logs_exporter otlp \
    --service_name fastapi-service-3 \
    uvicorn service3.main:app --port 8003 &
PID3=$!


# Start service2
export OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED=true
opentelemetry-instrument \
    --metrics_exporter otlp \
    --traces_exporter otlp \
    --logs_exporter otlp \
    --service_name fastapi-service-2 \
    uvicorn service2.main:app --port 8002 &
PID2=$!


# Start service1
export OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED=true
opentelemetry-instrument \
    --metrics_exporter otlp \
    --traces_exporter otlp \
    --logs_exporter otlp \
    --service_name fastapi-service-1 \
    uvicorn service1.main:app --port 8001 &
PID1=$!

# Start service4 (Kafka consumer)
export OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED=true
opentelemetry-instrument \
    --metrics_exporter otlp \
    --traces_exporter otlp \
    --logs_exporter otlp \
    --service_name k-consumer \
    python service4/consumer.py &
PID4=$!


# Wait for all
wait $PID3 $PID2 $PID1 $PID4
