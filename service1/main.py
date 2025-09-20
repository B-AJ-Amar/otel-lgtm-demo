


from fastapi import FastAPI, HTTPException, Request, Response
import logging
import random
import time
import requests
from logger import logger
from aiokafka import AIOKafkaProducer
import json
from opentelemetry.instrumentation.aiokafka import AIOKafkaInstrumentor

# activate instrumentation
AIOKafkaInstrumentor().instrument()

app = FastAPI()
producer = None

@app.on_event("startup")
async def startup_event():
    global producer
    producer = AIOKafkaProducer(
        bootstrap_servers=["kafka:9092"],
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    await producer.start()
    logger.info("[service1] Kafka producer started.")

@app.on_event("shutdown")
async def shutdown_event():
    global producer
    if producer:
        await producer.stop()
        logger.info("[service1] Kafka producer stopped.")

@app.get("/process")
async def process(request: Request):
    logger.info(f"[service1] Received request: {request.url}")
    try:
        resp = requests.get("http://service2:8002/job")
        data = resp.json()
        logger.info(f"[service1] Received response from service2: {data}")
        # Produce to Kafka (await send)
        await producer.send_and_wait("service1-output", data)
        logger.info(f"[service1] Produced message to Kafka: {data}")
        return {"service": "service1", "result": data}
    except Exception as e:
        logger.error(f"[service1] Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))



@app.get("/random_sleep")
async def random_sleep(response: Response):
    time.sleep(random.randint(0, 5))
    logging.error("random sleep")
    return {"path": "/random_sleep"}


@app.get("/error_test")
async def error_test(response: Response):
    logging.error("got error!!!!")
    raise ValueError("value error")