from typing import Any

from aiokafka import AIOKafkaProducer
from aiokafka.errors import KafkaConnectionError

KAFKA_BROKER = "localhost:9092"

async def send_message(topic: str, message: Any):
    producer = AIOKafkaProducer(bootstrap_servers=KAFKA_BROKER)
    try:
        await producer.start()
        print("Kafka Producer started")
        metadata = await producer.send_and_wait(topic, message.encode('utf-8'))
        print(f"Message sent to {topic}, metadata: {metadata}")
    except KafkaConnectionError as e:
        print(f"Kafka connection failed: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        await producer.stop()
        print("Kafka Producer stopped")

# asyncio.run(send_message('order_created', '{"order_id": 1234, "status": "created"}'))
