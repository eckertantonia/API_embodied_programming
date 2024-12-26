from BoltGroup import BoltGroup
from bolt import Bolt
from spherov2.types import Color
from typing import List
import movement.basics as basicmoves
import time
import asyncio

class Choreography:
    def __init__(self):
        self.movementStrategies = None
        self.boltGroup = BoltGroup()
        self.loop = asyncio.get_running_loop()

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

        if choreography == "kurve":
            # Hermitesche Kurve definieren
            p0, p1 = (0, 0), (1, 1)    # Start- und Endpunkt
            m0, m1 = (3, 0), (0, 1)    # Tangenten
            num_points = 10            # Punkte auf der Kurve
            curve = basicmoves.hermiteCurve(p0, p1, m0, m1, num_points)

            # Bewegungsbefehle generieren
            commands = basicmoves.calculate_commands(curve)

            p1, p2 = (1, 1), (0, 2)    # Start- und Endpunkt
            m1, m2 = (0, 1), (-3, 0)    # Tangenten
            num_points = 10            # Punkte auf der Kurve
            curve = basicmoves.hermiteCurve(p1, p2, m1, m2, num_points)

            # Bewegungsbefehle generieren
            commands2 = basicmoves.calculate_commands(curve)

            # Bolt die Kurve fahren lassen
            # basicmoves.drive_hermite_curve(bolt,commands,70)
            # kreis fahren = 4x drive hermite curve wiederholen
            # TODO irgendwas stimmt mit winkel und geschwindigkeit noch nicht!!
            # TODO Collision Error fangen
            try:
                with bolt.getApi() as robot:
                    basicmoves.drive_hermite_curve(robot,commands,80)
                    basicmoves.drive_hermite_curve(robot, commands2, 80)
            except Exception as e:
                print(f"Exception {e} aufgetreten. \n Stracktrace: \n {e.with_traceback}")
                
