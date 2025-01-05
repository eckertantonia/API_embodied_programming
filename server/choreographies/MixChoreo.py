import threading
import time

from spherov2.types import Color

from server.BoltGroup import BoltGroup
from server.movement.movement_strategies.MovementInterface import MovementInterface
from server.movement.movement_strategies.MoveForwardStrategy import MoveForwardStrategy


class MixChoreo:

    def start_choreo(self, bolt_group, strategy:MovementInterface):

        # assignStartPositions
        self.assign_start_pos(bolt_group)
        time.sleep(30)

        # 2 bolts aus bolt_group fuer circle

        circle_group = BoltGroup()

        circle_group.assign_bolt(bolt_group.bolts[2])
        circle_group.assign_bolt(bolt_group.bolts[3])

        threads = []
        for bolt in circle_group:
            thread = threading.Thread(target=self.move_forward, args=(bolt,))
            threads.append(thread)
            thread.start()

        # Warten bis alle Threads ausgeführt wurden
        for thread in threads:
            thread.join()

        strategy.drive(circle_group, [])

        return

    def assign_start_pos(self, bolt_group: BoltGroup):
        for i in range(len(bolt_group.bolts)):
            bolt_group[i].calibrate()
            bolt_group[i].position = (0, i)
            bolt_group[i].toyApi.set_matrix_character(f"{i}", color=Color(r=100, g=0, b=100))

    def move_forward(self, bolt):
        move_forward = MoveForwardStrategy()

        points = [bolt.position, (bolt.position[0]+2, bolt.position[1])]

        move_forward.drive(bolt, points)

