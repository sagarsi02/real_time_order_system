
from fastapi import FastAPI

from shared.kafka.producer import send_message

app = FastAPI(title="Order Service")

@app.post("/order")
async def create_order(order_id: int, status: str):
    message = f'{{"order_id": {order_id}, "status": "{status}"}}'
    print(f'Creating order: {message}')
    await send_message("order_created", message)  # Send event to Kafka
    return {"message": "Order created and event sent to Kafka"}
