from server.movement.movement_strategies.MovementInterface import MovementInterface

import server.movement.basics as basic_moves


class MoveForwardStrategy(MovementInterface):
    def __call__(self, *args, **kwds):
        print("move forward")

    def drive(self, robot):
        print("move methode")
        points = [(0, 0), (1, 0)]  # [] von punkten

        basic_moves.drive_hermite_curve(robot, points)
