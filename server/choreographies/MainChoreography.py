from server.boltgroup import BoltGroup
from server.choreographies.BubbleSortChoreo import BubbleSortChoreo
from server.choreographies.DontSwapChoreo import DontSwapChoreo
from server.choreographies.SwapChoreo import SwapChoreo
from server.ledcontrol import LEDControl

CHOREOGRAPHIES = {
    "bubblesort": BubbleSortChoreo,
    "swap": SwapChoreo,
    "dont_swap": DontSwapChoreo
}


def _get_choreography_instance(choreography):
    choreography_class = CHOREOGRAPHIES.get(choreography)
    if choreography_class:
        return choreography_class()
    else:
        return None


class MainChoreography:
    def __init__(self):
        self.bolt_group = BoltGroup()
        self.ledcontrol = LEDControl()
        self.values = []
        self._initial = True

    def _set_bolt_group(self, robots):
        for bolt in robots:
            self.bolt_group.assign_bolt(bolt)

    def start_choreography(self, values, choreography):

        if self._initial:
            self._set_bolts_and_values()
            self._initial = False

        # roboter zu values identifizieren
        robot_group = BoltGroup()

        for value in values:
            robot = self._get_robot_with_value(value)
            robot_group.assign_bolt(robot)

        # bewegungen zu message finden
        _get_choreography_instance(choreography).start_choreo(robot_group, values)

    def _get_robot_with_value(self, target_value):

        for bolt in self.bolt_group:
            if bolt.value == target_value:
                return bolt
        return None

    def _set_bolts_and_values(self):
        for bolt in self.bolt_group:
            bolt.calibrate()
            self.ledcontrol.show_character(bolt, bolt.value)
