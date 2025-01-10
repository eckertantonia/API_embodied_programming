from abc import ABC

import server.movement.basics as basic_moves
from server.bolt import Bolt
from server.movement.movement_strategies.MovementStrategy import MovementStrategy


class InLineStrategy(MovementStrategy, ABC):

    def drive(self, robots: Bolt, points, initial_heading=None, offset=0):
        # TODO: wie mache ich klar, ob Linie auf x oder y Achse?
        x, y = points[0]
        try:
            line_points = [robots.position, (robots.position[0], y)]

            basic_moves.drive_hermite_curve(robots, line_points, compass_offset=robots.offset)

            robots.update_position((robots.position[0], y))


        except Exception as e:
            print(f"Exception in InLineStrategy: {e}")
            raise
