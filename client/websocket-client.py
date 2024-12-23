#!/usr/bin/env python

import asyncio
from websockets.asyncio.client import connect

async def connectToServer():
    async with connect("ws://localhost:8765") as websocket:
        await websocket.send("Hello World!")
        response = await websocket.recv()
        print(response)

if __name__ == "__main__":
    asyncio.run(connectToServer())