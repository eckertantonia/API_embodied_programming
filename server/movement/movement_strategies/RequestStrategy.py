import logging
import threading
from abc import ABC

import server.movement.basics as basic_moves
from server.bolt_group import BoltGroup
from server.movement.movement_strategies.MovementStrategy import MovementStrategy

logger = logging.getLogger(__name__)


class RequestStrategy(MovementStrategy, ABC):
    def __init__(self):
        self.requester_coords = []
        self.follower_coords = []

    def drive(self, robots: BoltGroup, points):
        """
        Fuehrt die RequestStrategy aus, indem die Positionen fuer einen auffordernden Bolt und einen folgenden Bolt berechnet und anschliessend bewegt werden.

        :param robots: BoltGroup mit 2 Elementen
        :param points: int-Tupel mit Ziel-Positionen der 2 Elemente aus robots
        :raises Exception
        """

        try:
            self._calculate_points(robots)

            self._execute_threads(robots, basic_moves.drive_hermite_curve)

        except Exception as e:
            logger.exception(f"Exception in InLineXStrategy: {e}")
            raise

    def _calculate_points(self, robots: BoltGroup):
        """
        Berechnet die Positionen fuer einen auffordernden Bolt und einen folgenden Bolt.

        TODO: Berechnung

        :param robots: BoltGroup
        :return:
        """
        pass

    def _execute_threads(self, robots, target_method):
        """
        Startet einen Thread fuer jedes Element aus robots, aktualisiert die Position fuer jedes Element aus robots
        TODO: richtige Punkte-Zuweisung

        :param robots: BoltGroup
        :param target_method:
        :return:
        """

        threads = []
        for i, robot in enumerate(robots):
            try:
                pass
                # thread = threading.Thread(target=target_method, args=(robot, self.points[i],))
                # threads.append(thread)
                #
                # robot.update_position(self.points[i])
                #
                # thread.start()

            except Exception as e:
                logger.exception(f"InLineXStrategy: Error in threads for robot {robot.name}: {e}")

        for thread in threads:
            thread.join()
