import asyncio
import json
import math
import random
import websockets


SERVER = "ws://127.0.0.1:8000/ws/robot"


robots = {
    "AMR-01": {
        "x": 1.0,
        "y": 1.0,
        "battery": 95,
        "phase": 0.0,
    },
    "AMR-02": {
        "x": 5.0,
        "y": 2.0,
        "battery": 87,
        "phase": 2.0,
    },
    "AMR-03": {
        "x": 2.0,
        "y": 6.0,
        "battery": 76,
        "phase": 4.0,
    },
}


async def robot(robot_id):
    robot = robots[robot_id]

    while True:
        try:
            print(f"{robot_id}: connecting...")

            async with websockets.connect(SERVER) as ws:

                print(f"{robot_id}: connected")

                while True:
                    robot["phase"] += 0.08

                    if robot_id == "AMR-01":
                        robot["x"] = 1 + (
                            math.sin(robot["phase"]) * 4
                        )
                        robot["y"] = 1 + (
                            math.cos(robot["phase"]) * 2
                        )

                    elif robot_id == "AMR-02":
                        robot["x"] = 5 + (
                            math.cos(robot["phase"]) * 3
                        )
                        robot["y"] = 4 + (
                            math.sin(robot["phase"]) * 3
                        )

                    elif robot_id == "AMR-03":
                        robot["x"] = 5 + (
                            math.sin(robot["phase"]) * 3
                        )
                        robot["y"] = 6 + (
                            math.cos(robot["phase"]) * 2
                        )

                    robot["battery"] -= 0.01

                    if robot["battery"] < 20:
                        robot["battery"] = 100

                    message = {
                        "robot_id": robot_id,
                        "x": round(robot["x"], 2),
                        "y": round(robot["y"], 2),
                        "battery": round(robot["battery"], 1),
                        "status": "MOVING",
                        "task": "Warehouse Task",
                    }

                    await ws.send(json.dumps(message))

                    await ws.recv()

                    print(
                        f"{robot_id} | "
                        f"x={message['x']} "
                        f"y={message['y']} "
                        f"battery={message['battery']}%"
                    )

                    await asyncio.sleep(0.5)

        except Exception as error:
            print(f"{robot_id}: disconnected - {error}")
            print(f"{robot_id}: retrying in 2 seconds...")
            await asyncio.sleep(2)


async def main():
    await asyncio.gather(
        robot("AMR-01"),
        robot("AMR-02"),
        robot("AMR-03"),
    )


if __name__ == "__main__":
    asyncio.run(main())