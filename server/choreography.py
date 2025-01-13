from typing import List

from bolt import Bolt
from bolt_group import BoltGroup
from movement.movement_strategies.MoveForwardStrategy import MoveForwardStrategy
from server.choreographies.FlockChoreo import FlockChoreo
from server.choreographies.MixChoreo import MixChoreo
from server.led_control import LEDControl
from server.movement.movement_strategies.CirclingStrategy import CirclingStrategy

STRATEGIES = {
    "forward": MoveForwardStrategy,
    "circle": CirclingStrategy
}


# TODO: Strategien in Manager verwalten?
def _get_strategy_instance(strategy):
    strategy_class = STRATEGIES.get(strategy)
    if strategy_class:
        return strategy_class()
    else:
        raise ValueError("Unbekannte Strategie")


class Choreography:
    def __init__(self):
        self.bolt_group = BoltGroup()

    def start_choreography(self, robot_group: List[Bolt], choreography, strategy):
        """
        Initialer Start jeder Choreographie.

        :param robot_group: List[Bolt], BoltGroup
        :param choreography: str
        :param strategy: str
        :return:
        """

        self.create_bolt_group(robot_group)

        # choreo logik
        if choreography == "flock":
            flock = FlockChoreo(self.bolt_group)

            flock.start_choreo()

        elif choreography == "mix":
            mix = MixChoreo()

            mix.start_choreo(self.bolt_group, _get_strategy_instance(strategy))

        elif choreography == "color":
            ledcontrol = LEDControl()
            ledcontrol.show_grouping(self.bolt_group[0])

    def create_bolt_group(self, bolt_group):

        for bolt in bolt_group:
            self.bolt_group.assign_bolt(bolt)
