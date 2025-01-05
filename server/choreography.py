import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import List

from spherov2.sphero_edu import SpheroEduAPI
from spherov2.types import Color

from BoltGroup import BoltGroup
from bolt import Bolt
from movement.movement_strategies.MoveForwardStrategy import MoveForwardStrategy
from server.choreographies.FlockChoreo import FlockChoreo
# from server.choreographies.MixChoreo import MixChoreo

STRATEGIES = {
    "forward": MoveForwardStrategy
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

        # Bolts als Gruppe definieren
        for bolt in bolt_group:
            self.boltGroup.assign_bolt(bolt)

        if choreography == "move":

            self.loop.create_task(self.choreo_async(strategy))

        elif choreography == "flock":
            flock = FlockChoreo(self.boltGroup)

            await flock.start_choreo()

        elif choreography == "mix":
            mix = MixChoreo()

            await mix.start_choreo()


    # TODO in choreography part auslagern?
    async def choreo_async(self, strategy):
        """

        :param strategy: MovementStrategy
        :return:
        """
        tasks = [self.task(strategy, bolt) for bolt in self.boltGroup]
        await asyncio.gather(*tasks)

    async def task(self, strategy, bolt):
        print("task")
        points = [(0, 1), (0, 0)]  # [] von Punkten
        with ThreadPoolExecutor() as executor:
            def sync_task():
                try:
                    with SpheroEduAPI(bolt.toy) as bolt_api:
                        bolt.calibrate(bolt_api)
                        bolt_api.set_matrix_character("|", color=Color(r=100, g=0, b=100))
                        strategy_instance = _get_strategy_instance(strategy)
                        strategy_instance.drive(bolt_api, points, offset=bolt.offset)

                except Exception as e:
                    print(f"Error in sync_taks: {e}")
                    raise

            await self.loop.run_in_executor(executor, sync_task)
