#!/usr/bin/env python3.8

import asyncio
import json
import logging

from websockets.asyncio.server import serve
from websockets.exceptions import ConnectionClosedOK, ConnectionClosedError
from messaging.messaging_service import decode_message


async def handler(websocket):
    while True:
        try:
            print("Nächste Anweisung bitte!")
            data = await websocket.recv()
            reply = f"Daten erhalten als: {data}"
            print(reply)

            try:
                message = json.loads(data)
            except json.JSONDecodeError:
                print("Ungültige JSON-Nachricht erhalten.")
                await websocket.send("Ungültige Nachricht")
                continue

                # Keep-Alive-Nachrichten ignorieren
            if message.get("type") == "keep_alive":
                print("Keep-Alive-Nachricht erhalten. Ignorieren.")
                continue

            await websocket.send(reply)

            # ab hier kommt dann komplette Logik
            try:
                await decode_message(data)
            except Exception:
                print("exception in decode_message")
                await websocket.send("error. retry")
                raise
        except ConnectionClosedOK:
            print("Connection closed OK")
            break
        except ConnectionClosedError:
            print("Connection closed Error")
            break


async def start_server():
    async with serve(handler, "localhost", 8765):
        print("server laeuft!")
        await asyncio.get_running_loop().create_future()  # run forever


if __name__ == "__main__":
    # logging.basicConfig(level=logging.DEBUG)
    asyncio.run(start_server(), debug=True)
