from server.bolt_group import BoltGroup
from server.choreographies.ChoreographyInterface import ChoreographyInterface
from server.led_control import LEDControl
from server.movement.movement_strategies.CompareNoChangeStrategy import CompareNoChangeStrategy
from server.movement.movement_strategies.CompareWithChangeStrategy import CompareWithChangeStrategy
from server.movement.movement_strategies.DriveToCompareStrategy import DriveToCompareStrategy
from server.movement.movement_strategies.MoveForwardStrategy import MoveForwardStrategy


class BubbleSortChoreo(ChoreographyInterface):
    def __init__(self):
        self.bolt_group = None
        self.values = None
        self.compare_group = BoltGroup()
        self.ledcontrol = LEDControl()

    def set_bolts_and_values(self, bolts: [], values: []):
        self.bolt_group = BoltGroup(bolts)
        self.values = values

        for bolt in self.bolt_group:
            bolt.calibrate()
            self.ledcontrol.show_character(bolt, bolt.value)

    def start_choreo(self, robot_group, values):
        self.set_bolts_and_values(robot_group, values)

        self.bubblesort_choreo()

    def bubblesort_choreo(self):
        # algorithmus

        n = len(self.values)
        for i in range(n):
            swapped = False
            for j in range(n - i - 1):
                print(f"{self.values[j]} {self.values[j + 1]} ")
                # Gruppe erstellen von 2 Robotern mit den entsprechenden Values
                self.compare_group.assign_bolt(self.get_robot_with_value(self.values[j]))
                self.compare_group.assign_bolt(self.get_robot_with_value(self.values[j + 1]))
                # Roboter mit value j und j+1 bewegen
                starting_points = [self.compare_group[1].position, self.compare_group[0].position]
                self.compare_robots()

                if self.values[j] > self.values[j + 1]:
                    # Roboter tauschen Positionen
                    self.swap_robots(starting_points)
                    self.values[j], self.values[j + 1] = self.values[j + 1], self.values[j]
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
