from manager import Manager
import asyncio

# brauch ich vielleicht gar nicht
manager = []


async def control(robots, movement, strategy):
    manager = Manager()

    await manager.manage_bolts(robots, movement, strategy)
