import asyncio
import threading
from abc import ABC
from concurrent.futures.process import ProcessPoolExecutor
from idlelib.debugobj_r import remote_object_tree_item

from spherov2.types import Color

from server.BoltGroup import BoltGroup
from server.movement.movement_strategies.MoveForwardStrategy import MoveForwardStrategy
from server.movement.movement_strategies.MovementInterface import MovementInterface
import server.movement.basics as basic_moves
from typing import Dict

class CirclingStrategy(MovementInterface, ABC):

    # 2 Bolts

    # einer x+1, y+1 -> x+1, y-1 # halber kreis

    # anderer x-1, y-1 -> x-1, y+1 #halber kreis

    def drive(self, robots: BoltGroup, points, initial_heading=None, offset=0):

        # robot sollte liste von 2 bolts sein
        if len(robots.bolts) == 2:

            # entscheidung, wer wie fährt: kleinerer y-Wert fährt move_down
            if robots.bolts[0].position[1] < robots.bolts[1].position[1]:
                robot_down = robots.bolts[1]
                robot_up = robots.bolts[0]
            else:
                robot_down = robots.bolts[0]
                robot_up = robots.bolts[1]

            methods_to_run = [
                (self.move_up, (robot_up,)),
                (self.move_down, (robot_down,))
            ]
            self.run_methods_in_threads_with_params(methods_to_run)
        else:
            print(f"CirclingStrategy: falsche Anzahl robots")
            # raises error, weil liste falsche laenge

        # tasks für einzelne bolts erstellen
        return

    def run_methods_in_threads_with_params(self, methods_with_args):
        """
        TODO: variablen benennnung, docstings
        """
        threads = []
        for method, args in methods_with_args:
            thread = threading.Thread(target=method, args=args)
            threads.append(thread)
            thread.start()

        # Wait for all threads to finish
        for thread in threads:
            thread.join()

        return

# TODO: Koordinatenberechnung!!!
    def move_up(self, robot):
        try:
            robot.toyApi.set_matrix_character("0", color=Color(r=100, g=0, b=100))
            x, y = robot.position
            points = [(x,y), (x+2,y+2), (x+4,y), (x+2, y-2), (x,y)]

            basic_moves.drive_hermite_curve(robot.toyApi, points, compass_offset=robot.offset)
            robot.update_position(points[-1])
        except RuntimeError as e:
            print(f"{e}")

    def move_down(self, robot):
        try:
            robot.toyApi.set_matrix_character("1", color=Color(r=100, g=0, b=100))
            x,y = robot.position
            points = [(x,y), (x-2,y-2), (x-4,y), (x-2,y+2), (x,y)]
            basic_moves.drive_hermite_curve(robot.toyApi, points, compass_offset=robot.offset)
            robot.update_position(points[-1])
        except RuntimeError as e:
            print(f"{e}")


