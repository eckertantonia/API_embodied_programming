from manager import Manager
import asyncio

manager = []


def control(boltName, movement, strategy):
    manager = Manager()

    manager.manageBolts([boltName], movement, strategy)
