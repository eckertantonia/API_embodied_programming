import time

import server.movement.basics as basic_moves
from server.bolt_group import BoltGroup
from server.bolt import Bolt
from server.movement.movement_strategies.MovementStrategy import MovementStrategy


class MoveForwardStrategy(MovementStrategy):

    def drive(self, robots: Bolt, points, offset=0):
        # points = [(0, 0), (1, 0), (0, 0)]  # [] von Punkten
        # basic_moves.plotSpline(points, initial_heading=initial_heading)

        try:
            basic_moves.drive_hermite_curve(robots.toy_api, points, compass_offset=robots.offset)
            robots.update_position(points[-1])
            time.sleep(1)
        except Exception as e:
            print(f"Exception in MoveForwardStrategy: {e}")
            raise


