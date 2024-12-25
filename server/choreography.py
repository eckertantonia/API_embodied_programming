from BoltGroup import BoltGroup
from bolt import Bolt
from spherov2.types import Color
from typing import List
import time

class Choreography:
    def __init__(self):
        self.movementStrategies = None
        self.boltGroup = BoltGroup()

    def startChoreography(self, boltGroup:List[Bolt], choreography:str):
        # Bolts als Gruppe definieren
        for bolt in boltGroup:
            self.boltGroup.assignBolt(bolt)

        # Choreografie auswählen
        if choreography == "move":
            bolt = self.boltGroup.bolts[0]

            with bolt.getApi() as api:
                api.set_matrix_fill(x1=0, y1=0, x2=7, y2=7, color=Color(r=0, g=255, b=0))
                api.roll(0, 50, 5)
                time.sleep(10)
                print(f"{bolt.name} hat sich bewegt!")
