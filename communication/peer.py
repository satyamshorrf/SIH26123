import asyncio
import json
import websockets


PORT = 8765


async def handler(websocket):
    print("Robot connected")

    try:
        async for message in websocket:
            data = json.loads(message)
            print("Received:", data)

            await websocket.send(
                json.dumps({
                    "type": "ack",
                    "robot_id": data.get("robot_id")
                })
            )

    except websockets.exceptions.ConnectionClosed:
        print("Robot disconnected")


async def main():
    print(f"EdgeFleet P2P server running on port {PORT}")

    async with websockets.serve(handler, "0.0.0.0", PORT):
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())