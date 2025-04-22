import asyncio
from contextlib import asynccontextmanager
from typing import List

from fastapi import FastAPI, WebSocket, WebSocketDisconnect

from shared.kafka.consumer import consume_messages

# List to store active WebSocket connections
connected_clients: List[WebSocket] = []

# Broadcast function to send message to all connected WebSocket clients
async def notify_clients(message: dict):
    for ws in connected_clients:
        try:
            await ws.send_json(message)
        except Exception as e:
            print(f"❌ Error sending to client: {e}")
            connected_clients.remove(ws)

# Kafka message handler
async def handle_kafka_message(message: dict):
    print(f"📨 [Notification Service] New Kafka message: {message}")
    # Add custom processing here if needed, for example formatting or adding new fields
    # Then push the message to all WebSocket clients
    await notify_clients(message)

# Lifespan context for startup/shutdown handling
@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(consume_messages("order_created", group_id="notification_service", on_message=handle_kafka_message))
    yield
    task.cancel()

# FastAPI app with lifespan handler to manage the lifecycle of Kafka consumer
app = FastAPI(
    title="Notification Service",
    description="Real-time updates via WebSocket based on Kafka messages",
    lifespan=lifespan,
)

# WebSocket endpoint for client connections
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()  # Accept WebSocket connection
    connected_clients.append(websocket)  # Add the client to the connected clients list
    print("✅ WebSocket client connected.")

    try:
        while True:
            await websocket.receive_text()  # Keeps connection alive and receives any message
    except WebSocketDisconnect:
        connected_clients.remove(websocket)  # Remove client when they disconnect
        print("🔌 WebSocket client disconnected.")
