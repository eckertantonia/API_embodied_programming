from manager import Manager
import asyncio
manager = []

def control(connection, boltName):
    manager = Manager()

    manager.manageBolts([boltName])
    # manager.startApiForBolt(boltName)

