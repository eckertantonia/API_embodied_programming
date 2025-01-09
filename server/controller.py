from manager import Manager
import asyncio

# brauch ich vielleicht gar nicht
managers = []


async def control(robots, movement, strategy):
    manager = Manager()
    managers.append(manager)

    await manager.manage_bolts(robots, movement, strategy)

def control_connected():
    manager = managers[0]

    # manager funktionen zum connecten und disconnecten der bolts
    # methode um choreo zu starten