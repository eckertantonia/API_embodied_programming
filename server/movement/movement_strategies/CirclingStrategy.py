import asyncio
from abc import ABC

from server.movement.movement_strategies.MoveForwardStrategy import MoveForwardStrategy
from server.movement.movement_strategies.MovementInterface import MovementInterface
from typing import Dict

class CirclingStrategy(MovementInterface, ABC):

    # 2 Bolts

    # einer x+1, y+1 -> x+1, y-1 # halber kreis

    # anderer x-1, y-1 -> x-1, y+1 #halber kreis

    async def drive(self, robots: Dict, points, initial_heading=None, offset=0):

        # robot sollte liste von 2 bolts sein
        if len(robots) == 2:
            robot_1 = list(robots.keys())[0]
            robot_2 = list(robots.keys())[1]
            tasks = [self.move_up(robot_1, robots[robot_1])] + [self.move_down(robot_2, robots[robot_2])]
            await asyncio.gather(*tasks)
        else:
            print(f"CirclingStrategy: falsche Anzahl robots")
            # raises error, weil liste falsche laenge

        # tasks für einzelne bolts erstellen



        return

    async def move_up(self, robot, robot_api):

        pass

    async def move_down(self, robot, robot_api):
        pass