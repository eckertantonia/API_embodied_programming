import time

from spherov2.types import Color

from server.bolt import Bolt


class LEDControl:
    def __init__(self):
        self.main_color = Color(r=2, g=238, b=255)
        self.highlight_color = Color(r=255, g=0, b=0)

    def show_string(self, robot, string, color):
        pass

    def show_character(self, robot, character, color = None):
        robot.toy_api.set_matrix_character(character, self.main_color)
        pass

    def show_grouping(self, robot: Bolt, color = None):
        if color is None:
            robot.toy_api.set_matrix_line(0, 0, 7, 0, self.main_color)
        else:
            robot.toy_api.set_matrix_line(7, 0, 7, 7, color)
