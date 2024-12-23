#!/usr/bin/env python

import asyncio
from websockets.asyncio.server import serve
from websockets.exceptions import ConnectionClosedOK, ConnectionClosedError
from messaging.messaging_service import decodeMessage

async def handler(websocket):
    while True:
        try:
            data = await websocket.recv()

            # ab hier kommt dann komplette Logik
            await decodeMessage(data)

            reply = f"Daten erhalten als: {data}"
            await websocket.send(reply)
        except ConnectionClosedOK:
            print("Connection closed OK")
            break
        except ConnectionClosedError:
            print("Connection closed Error")
            break



async def startServer():
    async with serve(handler, "localhost", 8765):
        await asyncio.get_running_loop().create_future() # frun foreverr




if __name__== "__main__":
    asyncio.run(startServer())

