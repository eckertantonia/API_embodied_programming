from spherov2 import scanner
from bolt import Bolt
class Manager():
    def __init__(self):
        self.bolts = []

    async def connectBolt(self, boltName):
            toy = await scanner.find_toy(toy_name=boltName) #RuntimeError: asyncio.run() cannot be called from a running event loop
            bolt = Bolt(toy.name)
            self.bolts.append(bolt)
