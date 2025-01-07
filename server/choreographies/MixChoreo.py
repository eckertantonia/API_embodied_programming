import threading
import time

from spherov2.types import Color

from server.bolt_group import BoltGroup
from server.movement.movement_strategies.InLineStrategy import InLineStrategy
from server.movement.movement_strategies.MoveForwardStrategy import MoveForwardStrategy
from server.movement.movement_strategies.MovementStrategy import MovementStrategy


class MixChoreo:
    def __init__(self):
        self.move_forward_strategy = MoveForwardStrategy()
        self.in_line_strategy = InLineStrategy()

    def start_choreo(self, bolt_group, strategy: MovementStrategy):

        # assignStartPositions
        self.assign_start_pos(bolt_group)
        time.sleep(30)

        # 2 bolts aus bolt_group fuer circle

        circle_group = BoltGroup()

        circle_group.assign_bolt(bolt_group.bolts[2])
        circle_group.assign_bolt(bolt_group.bolts[3])

        self.execute_threads(circle_group, self.move_forward)

        strategy.drive(circle_group, [])

        self.execute_threads(circle_group, self.move_back)

        self.execute_threads(bolt_group, self.move_in_line)


        return

    def execute_threads(self, group, target_method):

        threads = []
        for bolt in group:
            thread = threading.Thread(target=target_method, args=(bolt,))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

    def assign_start_pos(self, bolt_group: BoltGroup):
        for i in range(len(bolt_group.bolts)):
            bolt_group[i].calibrate()
            bolt_group[i].position = (0, i)
            bolt_group[i].toy_api.set_matrix_character(f"{i}", color=Color(r=100, g=0, b=100))

    def move_forward(self, bolt):

        points = [bolt.position, (bolt.position[0], bolt.position[1] + 2)]

        self.move_forward_strategy.drive(bolt, points)

    def move_back(self, bolt):
        move_forward = MoveForwardStrategy()

        points = [bolt.position, (bolt.position[0], bolt.position[1] - 2)]

        self.move_forward_strategy.drive(bolt, points)

    def move_in_line(self, bolt):
        line_points=[0, 1]

        self.in_line_strategy.drive(bolt, line_points)