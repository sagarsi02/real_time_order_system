import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI

from shared.kafka.consumer import consume_messages


# Kafka message handler
async def handle_kafka_message(message: dict):
    print(f"📨 [Inventory Service] New Kafka Consume: {message}")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    consumer_task = asyncio.create_task(consume_messages("order_created", group_id="inventory_service", on_message=handle_kafka_message))
    yield
    # Shutdown
    consumer_task.cancel()
    try:
        await consumer_task
    except asyncio.CancelledError:
        pass

app = FastAPI(title="Inventory Service", lifespan=lifespan)
