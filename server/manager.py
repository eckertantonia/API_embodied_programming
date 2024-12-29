import asyncio
from spherov2 import scanner
from spherov2.sphero_edu import SpheroEduAPI
from spherov2.types import Color
from bolt import Bolt
from choreography import Choreography
from typing import List
import logging
import time


class Manager:
    def __init__(self):
        self.bolts: List[Bolt] = []
        self.loop = self._getRunningLoop()

        # event um auf api verbindung zu warten
        self.connection_event = asyncio.Event()

    def _getRunningLoop(self):
        return asyncio.get_running_loop()

    def _getBoltFromList(self, name) -> Bolt:
        return next((bolt for bolt in self.bolts if bolt.name == name), None)

    def manageBolts(self, bolts: List[str], movement, strategy):
        self.loop.create_task(self._manageBoltsAsync(bolts, movement, strategy))

    async def _manageBoltsAsync(self, bolts: List[str], movement, strategy):
        tasks = [self.setBoltApi(bolt) for bolt in bolts]
        await asyncio.gather(*tasks)
        self.connection_event.set()

        await self.startChoreo(self.bolts, movement, strategy)

    async def setBoltApi(self, boltname):

        # Bolt schon in bolts[], dann verbindungsprozess abbrechen
        if self._getBoltFromList(boltname):
            print(f"{boltname} existiert schon!")
            return

        bolt = await self._createBolt(boltname)
        self.bolts.append(bolt)

    async def _createBolt(self, boltname) -> Bolt:
        toy = await asyncio.get_event_loop().run_in_executor(None, lambda: scanner.find_toy(toy_name=boltname))
        if not toy:
            raise RuntimeError(f"Kein Bolt mit Namen '{boltname}' gefunden.")

        print(f"Gefunden: {toy.name} ({toy.address})")

        bolt = Bolt(toy)
        bolt.setBoltApi()

        return bolt

    async def startChoreo(self, boltGroup, movement, strategy):
        await self.connection_event.wait()
        choreo = Choreography()
        # TODO hardcodierte Choreografie austauschen
        choreo.startChoreography(boltGroup, movement, strategy)

    def startApiForBolt(self, boltname):
        self.loop.create_task(self.startApiHelper(boltname))

    async def startApiHelper(self, boltname):
        await self.connection_event.wait()
        bolt = self._getBoltFromList(boltname)
        print(f"fertig gewartet auf event")

        with bolt.getApi() as api:
            api.set_matrix_fill(x1=0, y1=0, x2=7, y2=7, color=Color(r=0, g=255, b=0))
            time.sleep(10)
            print(f"disconnected {bolt.name}")
