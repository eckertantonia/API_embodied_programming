import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import List

from bleak.exc import BleakDeviceNotFoundError
from spherov2.sphero_edu import SpheroEduAPI
from spherov2.types import Color

from BoltGroup import BoltGroup
from bolt import Bolt
from movement.movement_strategies.MoveForwardStrategy import MoveForwardStrategy
from server.choreographies.FlockChoreo import FlockChoreo
from server.choreographies.MixChoreo import MixChoreo
from server.movement.movement_strategies.CirclingStrategy import CirclingStrategy

STRATEGIES = {
    "forward": MoveForwardStrategy,
    "circle": CirclingStrategy
}

# TODO: Strategien in Manager verwalten?
def _get_strategy_instance(strategy):
    strategy_class = STRATEGIES.get(strategy)
    if strategy_class:
        return strategy_class()
    else:
        raise ValueError("Unbekannte Strategie")


class Choreography:
    def __init__(self):
        self.movementStrategies = None
        self.boltGroup = BoltGroup()
        self.loop = asyncio.get_running_loop()

    async def start_choreography(self, bolt_group: List[Bolt], choreography, strategy):
        """
        Initialer Start jeder Choreographie.

        :param bolt_group: List[Bolt], BoltGroup
        :param choreography: string
        :param strategy: string
        :return:
        """

        self.create_bolt_group(bolt_group)
        await self.open_apis()

        # choreo logik
        if choreography == "flock":
            flock = FlockChoreo(self.boltGroup)

            await flock.start_choreo()

        elif choreography == "mix":
            mix = MixChoreo()

            await mix.start_choreo(self.boltGroup, _get_strategy_instance(strategy))

        await self.close_apis()

    def create_bolt_group(self, bolt_group):

        for bolt in bolt_group:
            bolt_api = SpheroEduAPI(bolt.toy)
            self.boltGroup.assign_bolt(bolt, bolt_api)

    async def open_apis(self):
        for api in self.boltGroup.bolts.values():
            try:
                api.__enter__()
                api.scroll_matrix_text("Hi", color=Color(r=100, g=0, b=100), fps=5, wait=False)
            except BleakDeviceNotFoundError as e:
                print(f"Error in open_apis for: {e}")
            except TimeoutError as e:
                print(f"Error in open_apis for: {e}")


    async def close_apis(self):
        for api in self.boltGroup.bolts.values():
            api.__exit__(None, None, None)