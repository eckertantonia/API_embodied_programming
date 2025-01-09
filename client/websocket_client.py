#!/usr/bin/env python

import asyncio
from websockets.asyncio.client import connect

from client.messaging.messaging_client import continuing_message
from messaging.messaging_client import hardcoded_message, create_initial_json_message


async def connect_to_server():

    async with connect("ws://localhost:8765") as websocket:
        print(f"Mit Server verbunden!")

        initial_message = create_initial_json_message()

        print(f"Sendet Anfangsnachricht: {initial_message}")

        await websocket.send(initial_message)

        while True:

            json_message = continuing_message()

            if json_message is None:
                continue

            await websocket.send(json_message)

            if json_message.lower() == "exit":
                print("Verbindung wird geschlossen.")
                break

            response = await websocket.recv()
            print(response)

if __name__ == "__main__":
    asyncio.run(connect_to_server())