import threading
import time

from spherov2.types import Color

from server.bolt import Bolt
from server.boltgroup import BoltGroup
from server.choreographies.ChoreographyInterface import ChoreographyInterface
from server.movement.movement_strategies.CompareNoChange import CompareNoChangeStrategy
from server.movement.movement_strategies.DriveToCompare import DriveToCompareStrategy
from server.movement.movement_strategies.InLineX import InLineXStrategy
from server.movement.movement_strategies.MoveForward import MoveForwardStrategy
from server.movement.movement_strategies.MovementInterface import MovementStrategy
from server.ledcontrol import LEDControl
from server.movement.movement_strategies.Request import RequestStrategy
from server.movement.movement_strategies.CompareWithChange import CompareWithChangeStrategy


class MixChoreo(ChoreographyInterface):
    def __init__(self):
        self.move_forward_strategy = MoveForwardStrategy()
        self.in_line_strategy = InLineXStrategy()
        self.circle_group = BoltGroup()
        self.led_control = LEDControl()

    def start_choreo(self, robot_group, values):

        self.assign_start_pos(robot_group)
        self.circle_group.assign_bolt(robot_group[0])
        self.circle_group.assign_bolt(robot_group[1])

        drive_to_compare = DriveToCompareStrategy()
        drive_to_compare.drive(self.circle_group, [])

        compare_no_change = CompareNoChangeStrategy()
        compare_no_change.drive(self.circle_group, [])

        in_line_x = InLineXStrategy()
        in_line_x.drive(robot_group, [(0, 0)])

        group_2 = BoltGroup()
        group_2.assign_bolt(robot_group[0])
        target = [(robot_group[0].position[0], robot_group[0].position[1] + 2)]

        group_3 = BoltGroup()
        group_3.assign_bolt(robot_group[0])
        group_3.assign_bolt(robot_group[3])

        start_1 = robot_group[0].position
        start_2 = robot_group[3].position

        move_forward = MoveForwardStrategy()
        move_forward.drive(group_2, target)

        request_move = RequestStrategy()
        request_move.drive(group_3, [])

        compare_change = CompareWithChangeStrategy()
        compare_change.drive(group_3, [])

        target_points = [start_2, start_1]

        move_forward.drive(group_3, target_points)

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

        positions = [(0,0), (1,0), (2,0), (3,0), (4,0)]
        for bolt in bolt_group:
            bolt.calibrate()
            self.led_control.show_character(bolt, bolt.value)

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