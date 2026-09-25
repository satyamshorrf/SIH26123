import asyncio
import random
import websockets
import json


async def robot(robot_id):

    uri = "ws://127.0.0.1:8765"

    async with websockets.connect(uri) as ws:

        x = random.uniform(0, 10)
        y = random.uniform(0, 10)

        while True:

            message = {
                "robot_id": robot_id,
                "x": round(x, 2),
                "y": round(y, 2),
                "battery": random.randint(60, 100),
                "status": "MOVING",
            }

            await ws.send(json.dumps(message))

            response = await ws.recv()

            print(robot_id, response)

            x += random.uniform(-0.2, 0.2)
            y += random.uniform(-0.2, 0.2)

            await asyncio.sleep(1)


async def main():

    await asyncio.gather(
        robot("AMR-01"),
        robot("AMR-02"),
        robot("AMR-03"),
    )


asyncio.run(main())