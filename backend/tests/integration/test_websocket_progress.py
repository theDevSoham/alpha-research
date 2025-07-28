# tests/integration/test_websocket_progress.py
import asyncio
import websockets
import json
import pytest

@pytest.mark.asyncio
async def test_websocket_progress():
    task_id = "your-task-id"  # Replace with actual dynamic ID if needed
    uri = f"ws://localhost:8000/ws/progress/{task_id}"
    async with websockets.connect(uri) as ws:
        while True:
            message = await ws.recv()
            data = json.loads(message)
            print(f"Progress: {data['progress']}")
            if data["progress"] == 100:
                ws.close()
                break
