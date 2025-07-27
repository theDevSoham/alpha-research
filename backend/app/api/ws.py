from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import asyncio
import redis.asyncio as redis

router = APIRouter()

r = redis.Redis(host="redis", port=6379, decode_responses=True)

@router.websocket("/ws/progress/{job_id}")
async def websocket_endpoint(websocket: WebSocket, job_id: str):
    await websocket.accept()
    try:
        while True:
            # Get progress from Redis
            progress = await r.get(f"job_progress:{job_id}") or "0"
            await websocket.send_json({"progress": int(progress)})
            if progress == "100":
                break
            await asyncio.sleep(0.5)
    except WebSocketDisconnect:
        print(f"WebSocket disconnected for job {job_id}")