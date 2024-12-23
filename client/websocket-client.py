#!/usr/bin/env python

import asyncio
from websockets.asyncio.client import connect
from messaging.messaging_client import codeMessage


async def connectToServer():

    message_data = codeMessage()

    async with connect("ws://localhost:8765") as websocket:

        await websocket.send(message_data)
        response = await websocket.recv()
        print(response)

if __name__ == "__main__":
    asyncio.run(connectToServer())