import asyncio
from typing import List

from spherov2 import scanner

from bolt import Bolt
from choreography import Choreography


class Manager:
    def __init__(self):
        self.bolts: List[Bolt] = []
        self.loop = asyncio.get_running_loop()

        # event um auf api verbindung zu warten
        self.connection_event = asyncio.Event()

    def _check_robot_in_list(self, name) -> Bolt:
        return next((bolt for bolt in self.bolts if bolt.name == name), None)

    async def manage_bolts(self, bolts, choreography, strategy):
        """
        Creates task in running loop, calls correlating async function.

        :param bolts:
        :param choreography:
        :param strategy:
        :return:
        """

        tasks = [self._set_robot(bolt) for bolt in bolts]
        await asyncio.gather(*tasks)
        self.connection_event.set()

        await self._start_choreo(self.bolts, choreography, strategy)
        # await self._manage_bolts_async(bolts, choreography, strategy)

    # brauch ich die methode noch?
    async def _manage_bolts_async(self, bolts, choreography, strategy):
        tasks = [self._set_robot(bolt) for bolt in bolts]
        await asyncio.gather(*tasks)
        self.connection_event.set()

        await self._start_choreo(self.bolts, choreography, strategy)

    async def _set_robot(self, name):

        # Bolt schon in bolts[], dann verbindungsprozess abbrechen
        # TODO check ob das wirklich funktioniert
        if self._check_robot_in_list(name):
            print(f"{name} existiert schon!")
            return

        bolt = await self._create_bolt(name)
        self.bolts.append(bolt)

    async def _create_bolt(self, name) -> Bolt:

        toy = await self.find_toy_with_retry(name)
        if toy is None:
            raise ValueError(f"Spielzeug '{name}' konnte nach zwei Versuchen nicht gefunden werden.")

        print(f"Gefunden: {toy.name} ({toy.address})")
        bolt = Bolt(toy)

        return bolt

    async def find_toy_with_retry(self, name):
        for attempt in range(2):  # Maximal zwei Versuche
            try:
                toy = await asyncio.get_event_loop().run_in_executor(
                    None, lambda: scanner.find_toy(toy_name=name)
                )
                if toy:
                    return toy
                print(f"Versuch {attempt + 1}: Kein Spielzeug gefunden. Wiederholen...")
            except scanner.ToyNotFoundError as e:
                print(f"Fehler bei Versuch {attempt + 1}: \"{e}\" für Spielzeug \"{name}\"")
                raise
            await asyncio.sleep(1)  # Kurze Pause vor erneutem Versuch
        return None

    async def _start_choreo(self, robots, choreography, strategy):
        await self.connection_event.wait()
        choreo = Choreography()
        await choreo.start_choreography(robots, choreography, strategy)
