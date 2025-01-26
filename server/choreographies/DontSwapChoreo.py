from server.choreographies.ChoreographyInterface import ChoreographyInterface
from server.choreographies.SwapChoreo import TooManyRobotsForChoreoException
from server.ledcontrol import LEDControl
from server.movement.movement_strategies.CompareNoChange import CompareNoChangeStrategy
from server.movement.movement_strategies.DriveToCompare import DriveToCompareStrategy
from server.movement.movement_strategies.MoveForward import MoveForwardStrategy


class DontSwapChoreo(ChoreographyInterface):
    def __init__(self):
        self.ledcontrol = LEDControl()

    def start_choreo(self, robot_group, values):

        if len(robot_group) != 2:
            raise TooManyRobotsForChoreoException(robot_group)

        end_points = [robot_group[1].position, robot_group[0].position]

        # nach vorne fahren -> drive to compare
        for bolt in robot_group:
            self.ledcontrol.highlight_character(bolt, bolt.value)

        drive_to_compare = DriveToCompareStrategy()
        drive_to_compare.drive(robot_group, [])

        # compare no change
        compare_no_change = CompareNoChangeStrategy()
        compare_no_change.drive(robot_group, [])
        for bolt in robot_group:
            self.ledcontrol.green_character(bolt, bolt.value)

        # zurück fahren
        move_back = MoveForwardStrategy()
        move_back.drive(robot_group, [end_points[-1], end_points[0]])

        for bolt in robot_group:
            self.ledcontrol.show_character(bolt, bolt.value)