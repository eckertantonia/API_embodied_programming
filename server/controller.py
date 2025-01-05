from manager import Manager
import asyncio

# brauch ich vielleicht gar nicht
manager = []


def control(robots, movement, strategy):
    manager = Manager()

    manager.manage_bolts(robots, movement, strategy)
