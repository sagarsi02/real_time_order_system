import json
from typing import Awaitable, Callable

from aiokafka import AIOKafkaConsumer

KAFKA_BROKER = "localhost:9092"

# `on_message` is a callback you pass from the service (e.g., inventory or notification)
async def consume_messages(topic: str, group_id: str, on_message: Callable[[dict], Awaitable[None]]):
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=KAFKA_BROKER,
        group_id=group_id,  # unique group per service
    )
    await consumer.start()
    try:
        async for msg in consumer:
            message = json.loads(msg.value.decode("utf-8"))
            await on_message(message)
    finally:
        await consumer.stop()
