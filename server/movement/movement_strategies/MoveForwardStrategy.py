import server.movement.basics as basic_moves
from server.movement.movement_strategies.MovementInterface import MovementInterface


class MoveForwardStrategy(MovementInterface):

    def drive(self, robot, points, initial_heading=None):
        # points = [(0, 0), (1, 0), (0, 0)]  # [] von Punkten
        # basic_moves.plotSpline(points, initial_heading=initial_heading)
        try:
            basic_moves.drive_hermite_curve(robot, points, initial_heading=initial_heading)
        except Exception as e:
            print(f"Exception in MoveForwardStrategy: {e}")
            raise


