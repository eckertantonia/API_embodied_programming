from manager import Manager
import asyncio
manager = []

def control(connection, boltName):
    manager = Manager()

    manager.setBoltApi(boltName)
    manager.startApiForBolt(boltName)

