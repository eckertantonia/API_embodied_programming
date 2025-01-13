import threading
import time

from spherov2.types import Color

from server.bolt import Bolt
from server.bolt_group import BoltGroup
from server.movement.movement_strategies.InLineXStrategy import InLineXStrategy
from server.movement.movement_strategies.MoveForwardStrategy import MoveForwardStrategy
from server.movement.movement_strategies.MovementStrategy import MovementStrategy
from server.led_control import LEDControl

class MixChoreo:
    def __init__(self):
        self.move_forward_strategy = MoveForwardStrategy()
        self.in_line_strategy = InLineXStrategy()
        self.circle_group = BoltGroup()
        self.led_control = LEDControl()

    def start_choreo(self, bolt_group, strategy: MovementStrategy):

        # assignStartPositions
        self.assign_start_pos(bolt_group)
        time.sleep(1)


        # self.execute_threads(circle_group, self.set_color)

        #self.execute_threads(self.circle_group, self.move_forward)
        self.move_forward(self.circle_group[0])
        self.move_forward(self.circle_group[1])

        strategy.drive(self.circle_group, [])

        self.execute_threads(self.circle_group, self.move_back)

        # self.execute_threads(bolt_group, self.move_in_line)


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
        # for i in range(len(bolt_group.bolts)):
        #     bolt_group[i].calibrate()
        #     bolt_group[i].position = (0, i)
        #     bolt_group[i].toy_api.set_matrix_character(f"{i}", color=Color(r=100, g=0, b=100))

        positions = [(0,0), (1,0), (2,0), (3,0), (4,0)]
        for bolt in bolt_group:
            bolt.calibrate()
            if bolt.name == "SB-8EA0":
                bolt.update_position(positions[0])
                self.led_control.show_character(bolt, "0")
            elif bolt.name == "SB-51FA":
                bolt.update_position(positions[1])
                self.led_control.show_character(bolt, "1")
                self.circle_group.assign_bolt(bolt)
            elif bolt.name == "SB-231B":
                bolt.update_position(positions[2])
                self.led_control.show_character(bolt, "2")
                self.circle_group.assign_bolt(bolt)
            elif bolt.name == "SB-3DAB":
                bolt.update_position(positions[3])
                self.led_control.show_character(bolt, "3")
                # self.circle_group.assign_bolt(bolt)
            elif bolt.name == "SB-025F":
                bolt.update_position(positions[4])
                self.led_control.show_character(bolt, "4")

    def move_forward(self, bolt:Bolt):

        points = [bolt.position, (bolt.position[0], bolt.position[1]+3)]
        print(f"{bolt.name}: ")
        group = BoltGroup()
        group.assign_bolt(bolt)
        self.move_forward_strategy.drive(group, points)

        print(f"velocity: {bolt.toy_api.get_velocity()}")
        print(f"acceleration: {bolt.toy_api.get_acceleration()}")

    def move_back(self, bolt):

        points = [bolt.position, (bolt.position[0], bolt.position[1]-3 )]

        self.move_forward_strategy.drive(bolt, points)

    def move_in_line(self, bolt):
        line_points=[0, 1]

        self.in_line_strategy.drive(bolt, line_points)

    def set_color(self, bolt):
        ledcontrol = LEDControl()

        ledcontrol.show_grouping(bolt)