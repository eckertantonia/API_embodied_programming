#!/usr/bin/env python

import asyncio
from websockets.asyncio.server import serve

async def echo(websocket):
    async for message in websocket:
        await websocket.send(message)


async def startServer():
    async with serve(echo, "localhost", 8765) as server:
        await server.serve_forever()


if __name__== "__main__":
    asyncio.run(startServer())

