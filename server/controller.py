from manager import Manager
import asyncio

# brauch ich vielleicht gar nicht
managers = []


async def control_initial_connect(robots, choreography, strategy):
    manager = Manager()
    managers.append(manager)

    await manager.connect_bolts(robots, choreography, strategy)

def control_connected():
    manager = managers[0]

    manager.start_choreo()

def control_disconnect():
    manager = managers[0]

    manager.close_api()
    print("Apis closed.")