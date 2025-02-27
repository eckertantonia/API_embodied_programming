import time

from spherov2.types import Color

from server.bolt import Bolt


class LEDControl:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:  # Wenn keine Instanz existiert, erstelle sie
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "_initialized"): # nur einmal initialisieren
            self.main_color = Color(r=2, g=238, b=255)
            self.highlight_color = Color(r=255, g=0, b=0)
            self.green = Color(r=0, g=255, b=0)
            self._initialized = True  # Markiert als instanziiert

    def show_string(self, robot, string, color=None):
        if color is None:
            robot.toy_api.scroll_matrix_text("Hi", self.main_color, fps=5, wait=False)
        else:
            robot.toy_api.scroll_matrix_text("Hi", color, fps=5, wait=False)

        time.sleep(5)

    def show_character(self, robot, character, color = None):
        robot.toy_api.set_matrix_character(str(character), self.main_color)


    def highlight_character(self, robot, character, color = None):
        robot.toy_api.set_matrix_character(str(character), self.highlight_color)

    def green_character(self, robot, character, color = None):
        robot.toy_api.set_matrix_character(str(character), self.green)

    def show_grouping(self, robot: Bolt, color = None):
        if color is None:
            robot.toy_api.set_matrix_line(0, 0, 7, 0, self.main_color)
        else:
            robot.toy_api.set_matrix_line(7, 0, 7, 7, color)

    def show_multiple_colored_pixel(self, robot: Bolt, color= None):
        if color is None:
            robot.toy_api.set_matrix_pixel(x=1, y=1, color=self.main_color)
            robot.toy_api.set_matrix_pixel(x=2, y=1, color=self.highlight_color)

    def clear_led(self, robot: Bolt, pixel = ()):
        if not pixel:
            robot.toy_api.clear_matrix()
        else:
            x, y = pixel
            robot.toy_api.set_matrix_pixel(x, y, color=Color(0, 0, 0))

