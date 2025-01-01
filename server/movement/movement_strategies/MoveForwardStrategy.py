import server.movement.basics as basic_moves
from server.movement.movement_strategies.MovementInterface import MovementInterface


class MoveForwardStrategy(MovementInterface):

    def drive(self, robot):
        points = [(0, 0), (1, 0), (0, 0)]  # [] von Punkten
        basic_moves.drive_hermite_curve(robot, points)

