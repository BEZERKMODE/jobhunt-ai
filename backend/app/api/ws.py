from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import json
from app.core.redis import redis_client

router = APIRouter()


@router.websocket("/ws/tasks/{user_id}")
async def task_status_ws(websocket: WebSocket, user_id: int):
    await websocket.accept()
    pubsub = redis_client.pubsub()
    await pubsub.subscribe(f"task_updates:{user_id}")
    try:
        async for message in pubsub.listen():
            # redis-py returns dicts; skip subscribe/unsubscribe events
            if not message:
                continue
            mtype = message.get("type")
            if mtype == "message":
                data = message.get("data")
                # data may be bytes
                if isinstance(data, (bytes, bytearray)):
                    data = data.decode()
                await websocket.send_text(data)
    except WebSocketDisconnect:
        await pubsub.unsubscribe()
