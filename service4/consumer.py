import asyncio
from aiokafka import AIOKafkaConsumer
import json
from loguru import logger

async def consume():
    topic = "service1-output"
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=["localhost:9092"],
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='service4-group',
        value_deserializer=lambda x: json.loads(x.decode('utf-8')),
    )
    await consumer.start()
    logger.info(f"[service4] Listening to topic: {topic}")
    try:
        async for message in consumer:
            logger.info(f"[service4] Received message: {message.value}")
    finally:
        await consumer.stop()

if __name__ == "__main__":
    asyncio.run(consume())
