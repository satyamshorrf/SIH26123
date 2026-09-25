from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import asyncio
import json

app = FastAPI(title="EdgeFleet")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

robots = {
    "AMR-01": {
        "robot_id": "AMR-01",
        "x": 1.0,
        "y": 1.0,
        "battery": 95,
        "status": "IDLE",
        "task": "None",
    },
    "AMR-02": {
        "robot_id": "AMR-02",
        "x": 5.0,
        "y": 2.0,
        "battery": 87,
        "status": "IDLE",
        "task": "None",
    },
    "AMR-03": {
        "robot_id": "AMR-03",
        "x": 2.0,
        "y": 6.0,
        "battery": 76,
        "status": "IDLE",
        "task": "None",
    },
}

dashboard_clients = set()


@app.get("/")
def root():
    return {
        "system": "EdgeFleet",
        "status": "running",
        "robots": len(robots),
        "time": datetime.now().isoformat(),
    }


@app.get("/robots")
def get_robots():
    return robots


async def broadcast():
    message = json.dumps({
        "type": "fleet_state",
        "robots": robots,
    })

    disconnected = set()

    for client in dashboard_clients:
        try:
            await client.send_text(message)
        except Exception:
            disconnected.add(client)

    for client in disconnected:
        dashboard_clients.discard(client)


@app.websocket("/ws/robot")
async def robot_websocket(websocket: WebSocket):
    await websocket.accept()

    robot_id = None

    try:
        while True:
            data = await websocket.receive_json()

            robot_id = data.get("robot_id")

            if robot_id not in robots:
                await websocket.send_json({
                    "type": "error",
                    "message": "Unknown robot"
                })
                continue

            robots[robot_id].update({
                "x": data.get("x", robots[robot_id]["x"]),
                "y": data.get("y", robots[robot_id]["y"]),
                "battery": data.get(
                    "battery",
                    robots[robot_id]["battery"]
                ),
                "status": data.get(
                    "status",
                    robots[robot_id]["status"]
                ),
                "task": data.get(
                    "task",
                    robots[robot_id]["task"]
                ),
            })

            await broadcast()

            await websocket.send_json({
                "type": "ack",
                "robot_id": robot_id
            })

    except WebSocketDisconnect:
        print(f"{robot_id} disconnected")


@app.websocket("/ws/dashboard")
async def dashboard_websocket(websocket: WebSocket):
    await websocket.accept()

    dashboard_clients.add(websocket)

    await websocket.send_json({
        "type": "fleet_state",
        "robots": robots,
    })

    try:
        while True:
            await websocket.receive_text()

    except WebSocketDisconnect:
        dashboard_clients.discard(websocket)