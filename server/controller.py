from manager import Manager
manager = []

async def control(connection, boltName):
    manager = Manager()

    await manager.connectBolt(boltName=boltName)