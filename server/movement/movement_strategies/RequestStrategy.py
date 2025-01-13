import logging
import threading

import server.movement.basics as basic_moves
from server.bolt import Bolt
from server.bolt_group import BoltGroup
from server.movement.movement_strategies.MovementStrategy import MovementStrategy

logger = logging.getLogger(__name__)


class RequestStrategy(MovementStrategy):
    def __init__(self):
        self.requester_part_1 = []
        self.requester_part_2 = []
        self.requester_part_3 = []
        self.follower_part_2 = []
        self.follower_part_3 = []
        self.requester: Bolt = None
        self.follower: Bolt = None

    def drive(self, robots: BoltGroup, points: []):
        """
        Fuehrt die RequestStrategy aus, indem die Positionen fuer einen auffordernden Bolt und einen folgenden Bolt berechnet und anschliessend bewegt werden.

        :param robots: BoltGroup mit 2 Elementen. Erstes Element ist Aufforderer, zweites Element ist Folgender.
        :param points: int-Tupel mit Ziel-Positionen der 2 Elemente aus robots
        :raises Exception
        """

        if len(robots) != 2:
            print(f"Falsche Anzahl Roboter! Erwartet: 2, Erhalten: {len(robots)}.")
            return

        self.requester = robots[0]
        self.follower = robots[2]

        try:
            self._calculate_points()

            # part 1
            basic_moves.drive_hermite_curve(self.requester, self.requester_part_1)

            # part 2 und part 3
            self._execute_threads(basic_moves.drive_hermite_curve)

        except Exception as e:
            logger.exception(f"Exception in InLineXStrategy: {e}")
            raise

    def _calculate_points(self):
        """
        Berechnet die Positionen fuer einen auffordernden Bolt und einen folgenden Bolt.

        TODO: Berechnung

        :return:
        """

        xr, yr = self.requester.position
        xf, yf = self.follower.position

        # requester coords
        p_0 = (xr, yr)
        p_1 = (xf, yr)
        p_2 = (xf, yf + 1)
        self.requester_part_1 = [p_0, p_1, p_2]

        p_3 = (xf, yr)
        p_4 = (xr, yr)
        self.requester_part_2 = [p_2, p_3, p_4]

        diff_point_1_2 = xr - xf
        drive_len = diff_point_1_2 / 4

        p_5 = (xr + drive_len, yr)
        p_6 = (xr, yr)
        self.requester_part_3 = [p_4, p_5, p_6]

        # follower coords

        pf_0 = (xf, yf)
        pf_1 = (xf, yr)
        pf_2 = (xf - drive_len, yr)
        pf_3 = (xf, yr)

        self.follower_part_2 = [pf_0, pf_1, pf_2, pf_3]

    def _execute_threads(self, target_method):
        """
        Startet einen Thread fuer jedes Element aus robots, aktualisiert die Position fuer jedes Element aus robots
        TODO: richtige Punkte-Zuweisung

        :param target_method:
        :return:
        """

        threads_part_2 = []
        try:
            thread_r = threading.Thread(target=target_method, args=(self.requester, self.requester_part_2,))
            threads_part_2.append(thread_r)

            thread_f = threading.Thread(target=target_method, args=(self.follower, self.follower_part_2,))
            threads_part_2.append(thread_f)

            thread_r.start()
            thread_f.start()

        except Exception as e:
            logger.exception(f"RequestStrategy: Error in threads: {e}")

        for thread in threads_part_2:
            thread.join()

        threads_part_3 = []
        try:
            thread_r = threading.Thread(target=target_method, args=(self.requester, self.requester_part_3,))
            threads_part_3.append(thread_r)

            thread_f = threading.Thread(target=target_method, args=(self.follower, self.follower_part_3,))
            threads_part_3.append(thread_f)

            thread_r.start()
            thread_f.start()

        except Exception as e:
            logger.exception(f"RequestStrategy: Error in threads: {e}")

        for thread in threads_part_3:
            thread.join()
