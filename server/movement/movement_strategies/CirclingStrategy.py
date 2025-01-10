import threading
import time
from abc import ABC

from spherov2.types import Color

import server.movement.basics as basic_moves
from server.bolt_group import BoltGroup
from server.movement.movement_strategies.MovementStrategy import MovementStrategy


class CirclingStrategy(MovementStrategy, ABC):

    # 2 Bolts

    # einer x+1, y+1 -> x+1, y-1 # halber kreis

    # anderer x-1, y-1 -> x-1, y+1 #halber kreis

    def drive(self, robots: BoltGroup, points, initial_heading=None, offset=0):

        # robot sollte liste von 2 bolts sein
        if len(robots.bolts) == 2:

            # entscheidung, wer wie fährt: kleinerer x-Wert fährt move_down
            if robots.bolts[0].position[0] < robots.bolts[1].position[0]:
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

        time.sleep(1)
        return

    # TODO: Koordinatenberechnung!!!
    def move_up(self, robot):
        try:
            # robot.toy_api.set_matrix_character("0", color=Color(r=100, g=0, b=100))
            x, y = robot.position
            points = [(x, y), (x + 1, y + 1), (x + 2, y), (x + 1, y - 1), (x, y)]

            basic_moves.drive_hermite_curve(robot.toy_api, points, compass_offset=robot.offset)
            robot.update_position(points[-1])
        except RuntimeError as e:
            print(f"{e}")

    def move_down(self, robot):
        try:
            # robot.toy_api.set_matrix_character("1", color=Color(r=100, g=0, b=100))
            x, y = robot.position
            points = [(x, y), (x - 1, y - 1), (x - 2, y), (x - 1, y + 1), (x, y)]
            basic_moves.drive_hermite_curve(robot.toy_api, points, compass_offset=robot.offset)
            robot.update_position(points[-1])
        except RuntimeError as e:
            print(f"{e}")
