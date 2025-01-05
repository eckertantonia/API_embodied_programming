import asyncio
import threading
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
        """
        Sucht in self.bolts nach Bolt mit bestimmtem Namen.

        :param name: string
        :return: Bolt
        """
        return next((bolt for bolt in self.bolts if bolt.name == name), None)

    def manage_bolts(self, bolts: List[str], choreography, strategy):
        """
        TODO: Fehlermanagement bei Verbindung
        Creates task in running loop, calls correlating async function.

        :param bolts:
        :param choreography:
        :param strategy:
        :return:
        """

        # tasks = [self._set_robot(bolt) for bolt in bolts]
        # await asyncio.gather(*tasks)
        # self.connection_event.set()

        threads = []
        for bolt in bolts:
            thread = threading.Thread(target=self._set_robot, args=(bolt,))
            threads.append(thread)
            thread.start()

        # Wait for all threads to finish
        for thread in threads:
            thread.join()

        self._start_choreo(self.bolts, choreography, strategy)


    def _set_robot(self, name: str):

        toy = scanner.find_toy(toy_name=name)
        bolt = Bolt(toy)
        self.bolts.append(bolt)


    def _start_choreo(self, robots, choreography, strategy):
        """

        :param robots: BoltGroup
        :param choreography: string
        :param strategy: string
        :return:
        """
        choreo = Choreography()
        choreo.start_choreography(robots, choreography, strategy)
