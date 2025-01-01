from manager import Manager
import asyncio

manager = []


def control(robots, movement, strategy):
    manager = Manager()

    manager.manage_bolts(robots, movement, strategy)
