import logging
import threading

import server.movement.basics as basic_moves
from server.bolt import Bolt
from server.bolt_group import BoltGroup
from server.movement.movement_strategies.MovementStrategy import MovementStrategy

logger = logging.getLogger(__name__)


class DriveToCompareStrategy(MovementStrategy):
    def __init__(self):
        self.points = []
        self.robot_1: Bolt
        self.robot_2: Bolt
        self.robot_1_coords = []
        self.robot_2_coords = []

    def drive(self, robots: BoltGroup, points):
        """
        Fuehrt die MoveForwardStrategy fuer alle Elemente aus robots aus.

        :param robots: BoltGroup
        :param points: int-Tupel, Ziel-Koordinaten der Elemente aus robots in Reihenfolge der Elemente
        :raises Exception
        """
        self.points = points

        if robots[0].position[0] < robots[1].position[0]:
            self.robot_1 = robots[0]
            self.robot_2 = robots[1]
        else:
            self.robot_1 = robots[1]
            self.robot_2 = robots[0]

        try:
            self._execute_threads(robots, basic_moves.drive_hermite_curve)

        except Exception as e:
            logger.exception(f"Exception in MoveForwardStrategy: {e}")
            raise

    def _calculate_points(self):

        x_0, y_0 = self.robot_1.position
        x_1, y_1 = self.robot_2.position

        y_final = y_0 + 2
        # robot 1
        p1_0 = (x_0, y_0)
        p1_1 = (x_0, y_final)
        p1_2 = (x_0 + ((x_1-x_0) / 4), y_final)
        p1_3 = p1_1

        self.robot_1_coords = [p1_0, p1_1,p1_2, p1_3]

        # robot 2
        p2_0 = (x_1, y_1)
        p2_1 = (x_1, y_final)
        p2_2 = (x_1 - ((x_1 - x_0) / 4), y_final)
        p2_3 = p2_1

        self.robot_2_coords = [p2_0, p2_1, p2_2, p2_3]

    def _execute_threads(self, robots, target_method):
        """
        Startet einen Thread fuer jedes Element aus robots, aktualisiert die Position fuer jedes Element aus robots

        :param robots: BoltGroup
        :param target_method:
        :raises Exception
        """

        threads_part_2 = []
        try:
            thread_r = threading.Thread(target=target_method, args=(self.robot_1, self.robot_1_coords,))
            threads_part_2.append(thread_r)

            thread_f = threading.Thread(target=target_method, args=(self.robot_2, self.robot_2_coords,))
            threads_part_2.append(thread_f)

            thread_r.start()
            thread_f.start()

        except Exception as e:
            logger.exception(f"RequestStrategy: Error in threads: {e}")

        for thread in threads_part_2:
            thread.join()
