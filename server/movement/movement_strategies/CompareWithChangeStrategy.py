import logging
import threading

import server.movement.basics as basic_moves
from server.bolt import Bolt
from server.bolt_group import BoltGroup
from server.movement.movement_strategies.MovementStrategy import MovementStrategy

logger = logging.getLogger(__name__)


class CompareWithChangeStrategy(MovementStrategy):
    def __init__(self):
        self.points = []
        self.robot_1: Bolt = None
        self.robot_2: Bolt = None
        self.robot_1_coords = []
        self.robot_2_coords = []

    def drive(self, robots: BoltGroup, points: []):
        """
        Fuehrt die MoveForwardStrategy fuer alle Elemente aus robots aus.

        :param robots: BoltGroup
        :param points: int-Tupel, Ziel-Koordinaten der Elemente aus robots in Reihenfolge der Elemente
        :raises Exception
        """
        self.points = points

        sorted_robots = sorted(robots, key=lambda r: r.position[0])
        self.robot_1, self.robot_2 = sorted_robots

        try:
            self._calculate_points()
            self._execute_threads(robots, basic_moves.drive_hermite_curve)

        except Exception as e:
            logger.exception(f"Exception in MoveForwardStrategy: {e}")
            raise

    def _calculate_points(self):

        final_pos_robot_1 = self.robot_2.position
        final_pos_robot_2 = self.robot_1.position

        x1, y1 = self.robot_1.position
        x2, y2 = self.robot_2.position

        distance_x1_x2 = abs(x2 -x1)

        # robot 1

        p1_0 = (x1, y1)
        p1_1 = (x1, y1+1)
        p1_2 = (x1+distance_x1_x2, y1+1)
        p1_3 = (x1+distance_x1_x2, y1-1)
        p1_4 = (x1, y1-1)
        p1_5 = p1_1
        p1_6 = p1_2
        p1_7 = final_pos_robot_1

        self.robot_1_coords = [p1_0, p1_1, p1_2, p1_3, p1_4, p1_5, p1_6, p1_7]

        # robot 2

        p2_0 = (x2, y2)
        p2_1 = (x2, y2 - 1)
        p2_2 = (x2 - distance_x1_x2, y2 -1)
        p2_3 = (x2 - distance_x1_x2, y2 + 1)
        p2_4 = (x2, y2 + 1)
        p2_5 = p2_1
        p2_6 = p2_2
        p2_7 = final_pos_robot_2

        self.robot_2_coords = [p2_0, p2_1, p2_2, p2_3, p2_4, p2_5, p2_6, p2_7]

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

            for thread in threads_part_2:
                thread.join()

        except Exception as e:
            logger.exception(f"RequestStrategy: Error in threads: {e}")
