from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from starlette.websockets import WebSocketState
import asyncio
import redis.asyncio as redis

router = APIRouter()

r = redis.Redis(host="redis", port=6379, decode_responses=True)

@router.websocket("/ws/progress/{job_id}")
async def websocket_endpoint(websocket: WebSocket, job_id: str):
    await websocket.accept()
    print(f"WebSocket connected for job {job_id}")
    try:
        # Optional: Wait until the Redis key is set
        while not await r.exists(f"job_progress:{job_id}"):
            await asyncio.sleep(0.2)

        while True:
            if websocket.client_state == WebSocketState.CONNECTED:
                progress = await r.get(f"job_progress:{job_id}") or "0"
                print(progress)
                await websocket.send_json({"progress": int(progress)})
                if progress == "100":
                    await asyncio.sleep(1)  # allow client to receive final progress
                    break
                await asyncio.sleep(0.1)
    except WebSocketDisconnect:
        print(f"WebSocket disconnected for job {job_id}")
    except Exception as e:
        print(f"WebSocket error for job {job_id}: {e}")
    finally:
        if websocket.application_state == WebSocketState.CONNECTED:
            await websocket.close()
