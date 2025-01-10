#!/usr/bin/env python

import asyncio
import json

from websockets.asyncio.client import connect

from messaging.messaging_client import create_initial_json_message, continuing_message


async def connect_to_server():
    async with connect("ws://localhost:8765") as websocket:
        print(f"Mit Server verbunden!")

        initial_message = create_initial_json_message()

        print(f"Sendet Anfangsnachricht: {initial_message}")

        await websocket.send(initial_message)

        keep_alive_task = asyncio.create_task(send_keep_alive(websocket))

        while True:

            response = await websocket.recv()
            print(response)

            json_message = continuing_message()
            if json_message:
                await websocket.send(json_message)

            if json_message.lower() == "exit":
                print("Verbindung wird geschlossen.")
                keep_alive_task.cancel()
                break

async def send_keep_alive(websocket):
    while True:
        await asyncio.sleep(10)
        keep_alive_message = json.dumps({"type": "keep_alive"})
        await websocket.send(keep_alive_message)
        print("keep alive")



if __name__ == "__main__":
    asyncio.run(connect_to_server())
