import logging
import threading

import server.movement.basics as basic_moves
from server.bolt_group import BoltGroup
from server.movement.movement_strategies.MovementStrategy import MovementStrategy

logger = logging.getLogger(__name__)


class MoveForwardStrategy(MovementStrategy):
    def __init__(self):
        self.points = []

    def drive(self, robots: BoltGroup, points: []):
        """
        Fuehrt die MoveForwardStrategy fuer alle Elemente aus robots aus.

        :param robots: BoltGroup
        :param points: int-Tupel, Ziel-Koordinaten der Elemente aus robots in Reihenfolge der Elemente
        :raises Exception
        """
        if len(robots) != len(points):
            logger.exception(f"Exception in MoveForwardStrategy: len(robots) != len(points): {len(robots)} != {len(points)}")
            return

        self.points = points

        try:
            self._execute_threads(robots, basic_moves.drive_hermite_curve)

        except Exception as e:
            logger.exception(f"Exception in MoveForwardStrategy: {e}")
            raise

    def _execute_threads(self, robots, target_method):
        """
        Startet einen Thread fuer jedes Element aus robots, aktualisiert die Position fuer jedes Element aus robots

        :param robots: BoltGroup
        :param target_method:
        :raises Exception
        """

        threads = []

        for i, robot in enumerate(robots):
            try:

                thread = threading.Thread(target=target_method, args=(robot, [robot.position, self.points[i]]))
                threads.append(thread)

                robot.update_position(self.points[i])

                thread.start()

            except Exception as e:
                logger.exception(f"MoveForwardStrategy: Error in threads for robot {robot.name}: {e}")

        for thread in threads:
            thread.join()
