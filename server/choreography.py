from BoltGroup import BoltGroup
from bolt import Bolt
from spherov2.types import Color
from typing import List
import movement.basics as basicmoves
from movement.movement_strategies.MoveForwardStrategy import MoveForwardStrategy
import time
import asyncio

STRATEGIES = {
    "forward": MoveForwardStrategy
}


class Choreography:
    def __init__(self):
        self.movementStrategies = None
        self.boltGroup = BoltGroup()
        self.loop = asyncio.get_running_loop()

    def _get_strategy_instance(self, strategy):
        strategy_class = STRATEGIES.get(strategy)
        if strategy_class:
            return strategy_class()
        else:
            raise ValueError("Unbekannte Strategie")

    def startChoreography(self, boltGroup: List[Bolt], movement,  strategy: str):

        strategy_instance = self._get_strategy_instance(strategy)

        # Bolts als Gruppe definieren
        for bolt in boltGroup:
            self.boltGroup.assignBolt(bolt)

        # Choreografie auswählen
        if movement == "move":
            bolt = self.boltGroup.bolts[0]



            with bolt.getApi() as robot:
                strategy_instance.drive(robot)

        if movement == "kurve":
            # Hermitesche Kurve definieren
            points = [(0, 0), (0, 1), (0, 0)]  # [] von punkten

            # points = [(0, 0), (0.25, 0.25), (0.5, 0), (0.75, -0.25), (1, 0)] # kreis

            # basicmoves.plotSpline(points)

            # Bolt die Kurve fahren lassen
            # basicmoves.drive_hermite_curve(bolt,commands,70)
            # kreis fahren = 4x drive hermite curve wiederholen
            # TODO irgendwas stimmt mit winkel und geschwindigkeit noch nicht!!
            # TODO Collision Error fangen

            with bolt.getApi() as robot:
                basicmoves.drive_hermite_curve(robot, points, 80)

    # # Mapping für Strategien
    # STRATEGIES = {
    #     "forward": move_forward_strategy,
    #     "backward": move_backward_strategy,
    # }
    #
    # # Strategie auswählen
    # selected_strategy = STRATEGIES["forward"]
