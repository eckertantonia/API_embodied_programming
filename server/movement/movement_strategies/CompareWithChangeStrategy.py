import logging
import threading

import server.movement.basics as basic_moves
from server.bolt import Bolt
from server.bolt_group import BoltGroup
from server.movement.movement_strategies.MovementStrategy import MovementStrategy

logger = logging.getLogger(__name__)


class CompareNoChangeStrategy(MovementStrategy):
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

        final_pos_robot_1 = self.robot_2.position
        final_pos_robot_2 = self.robot_1.position

        # robot 1
        x1, y1 = self.robot_1.position
        p1_0 = (x1, y1)
        p1_1 = (x1, y1+1)
        p1_2 = (x1+1, y1+2)
        p1_3 = (x1+2, y1+2)
        p1_4 = (x1+3, y1+1)
        p1_5 = (x1+3, y1-1)
        p1_6 = (x1+2, y1-2)
        p1_7 = (x1+1, y1-2)
        p1_8 = (x1, y1-1)
        p1_9 = (x1, y1)
        p1_10 = (x1, y1 + 1)
        p1_11 = (x1+0.5, y1+2)
        p1_12 = (x1+1.5, y1+2)
        p1_13 = (x1+2, y1 + 1)
        p1_14 = final_pos_robot_1

        self.robot_1_coords = [p1_0, p1_1, p1_2, p1_3, p1_4, p1_5, p1_6, p1_7, p1_8, p1_9, p1_10, p1_11, p1_12, p1_13, p1_14]

        # robot 2
        x2, y2 = self.robot_1.position
        p2_0 = (x2, y2)
        p2_1 = (x2, y2 - 1)
        p2_2 = (x2 - 1, y2 -2)
        p2_3 = (x2 - 2, y2 -2)
        p2_4 = (x2-3, y2 - 1)
        p2_5 = (x2-3, y2+1)
        p2_6 = (x2-2, y2+2)
        p2_7 = (x2-1, y2+2)
        p2_8 = (x2, y2 + 1)
        p2_9 = (x2, y2 )
        p2_10 = (x2, y2-1)
        p2_11 = (x2 -0.5, y2-2)
        p2_12 = (x2 -1.5, y2 -2)
        p2_13 = (x2-2, y2 - 1)
        p2_14 = final_pos_robot_2

        self.robot_2_coords = [p2_0, p2_1, p2_2, p2_3,p2_4, p2_5, p2_6, p2_7, p2_8, p2_9, p2_10, p2_11, p2_12, p2_13, p2_14]

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
