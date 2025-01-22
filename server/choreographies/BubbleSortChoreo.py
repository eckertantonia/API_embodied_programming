from server.boltgroup import BoltGroup
from server.choreographies.ChoreographyInterface import ChoreographyInterface
from server.ledcontrol import LEDControl
from server.movement.movement_strategies.CompareNoChange import CompareNoChangeStrategy
from server.movement.movement_strategies.CompareWithChange import CompareWithChangeStrategy
from server.movement.movement_strategies.DriveToCompare import DriveToCompareStrategy
from server.movement.movement_strategies.MoveForward import MoveForwardStrategy


class BubbleSortChoreo(ChoreographyInterface):
    def __init__(self):
        self.bolt_group = None
        self.compare_group = BoltGroup()
        self.ledcontrol = LEDControl()

    def start_choreo(self, robot_group, values):
        self.bolt_group = robot_group
        # algorithmus

        n = len(values)
        for i in range(n):
            swapped = False
            for j in range(n - i - 1):
                print(f"{values[j]} {values[j + 1]} ")
                # Gruppe erstellen von 2 Robotern mit den entsprechenden Values
                self.compare_group.assign_bolt(self.get_robot_with_value(values[j]))
                self.compare_group.assign_bolt(self.get_robot_with_value(values[j + 1]))
                # Roboter mit value j und j+1 bewegen
                starting_points = [self.compare_group[1].position, self.compare_group[0].position]
                self.compare_robots()

                if values[j] > values[j + 1]:
                    # Roboter tauschen Positionen
                    self.swap_robots(starting_points)
                    values[j], values[j + 1] = values[j + 1], values[j]
                    swapped = True
                else:
                    # Roboter tauschen nicht
                    self.not_swap_robots(starting_points)

                self.compare_group.clear_bolts()
            if not swapped:
                break

    def compare_robots(self):
        # nach vorne fahren -> drive to compare
        for bolt in self.compare_group:
            self.ledcontrol.highlight_character(bolt, bolt.value)

        drive_to_compare = DriveToCompareStrategy()
        drive_to_compare.drive(self.compare_group, [])

    def swap_robots(self, end_points):
        # compare with change
        compare_with_change = CompareWithChangeStrategy()
        compare_with_change.drive(self.compare_group, [])

        for bolt in self.compare_group:
            self.ledcontrol.show_character(bolt, bolt.value)

        # zurück fahren
        move_back = MoveForwardStrategy()
        move_back.drive(self.compare_group, end_points)

        for bolt in self.compare_group:
            self.ledcontrol.show_character(bolt, bolt.value)

    def not_swap_robots(self, end_points):
        # compare no change
        compare_no_change = CompareNoChangeStrategy()
        compare_no_change.drive(self.compare_group, [])
        for bolt in self.compare_group:
            self.ledcontrol.green_character(bolt, bolt.value)

        # zurück fahren
        move_back = MoveForwardStrategy()
        move_back.drive(self.compare_group, [end_points[-1], end_points[0]])

        for bolt in self.compare_group:
            self.ledcontrol.show_character(bolt, bolt.value)

    def get_robot_with_value(self, target_value):

        for bolt in self.bolt_group:
            if bolt.value == target_value:
                return bolt
        return None
