#!/usr/bin/env python3.8

import asyncio
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

            await websocket.send(reply)

            # ab hier kommt dann komplette Logik
            await decode_message(data)
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
