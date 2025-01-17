import logging
import threading

import server.movement.basics as basic_moves
from server.boltgroup import BoltGroup
from server.movement.movement_strategies.MovementStrategy import MovementStrategy

logger = logging.getLogger(__name__)


class InLineXStrategy(MovementStrategy):
    def __init__(self):
        self.x_line = 0
        self.points = []

    def drive(self, robots: BoltGroup, points: []):
        """
        Fuehrt die InLineXStrategy aus, indem die Positionen der robots auf der X-Achse berechnet werden und die robots anschließend auf diese Position bewegt werden.

        :param robots: BoltGroup
        :param points: int-Tupel, Wert der X-Koordinate
        :raises Exception
        """

        self.x_line = points[0][0]
        try:
            self._calculate_points(robots)

            self._execute_threads(robots, basic_moves.drive_hermite_curve)

        except Exception as e:
            logger.exception(f"Exception in InLineXStrategy: {e}")
            raise

    def _calculate_points(self, robots: BoltGroup):
        """
        Berechnet die Position auf der x-Achse fuer jedes Element aus robots.

        :param robots: BoltGroup
        :return:
        """

        for robot in robots:
            print(f"{robot.name}")
            print(f"{robot.value}")

            new_pos = (robot.position[0], self.x_line)
            print(f"new_pos {new_pos}")

            if new_pos in self.points:
                new_pos = (self.points[-1][0] +1, self.x_line)
                print(f"new_pos {new_pos}")

            self.points.append(new_pos)

    def _execute_threads(self, robots, target_method):
        """
        Startet einen Thread fuer jedes Element aus robots, aktualisiert die Position fuer jedes Element aus robots

        :param robots: BoltGroup
        :param target_method:
        :return:
        """

        threads = []

        for i, robot in enumerate(robots):
            try:

                thread = threading.Thread(target=target_method, args=(robot, [robot.position, self.points[i]]))
                threads.append(thread)

                robot.update_position(self.points[i])

                thread.start()

            except Exception as e:
                logger.exception(f"InLineXStrategy: Error in threads for robot {robot.name}: {e}")

        for thread in threads:
            thread.join()
