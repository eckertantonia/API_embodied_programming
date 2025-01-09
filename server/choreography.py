import threading
from typing import List

from bleak.exc import BleakDeviceNotFoundError
from spherov2.types import Color

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

        try:
            for bolt in robot_group:
                self.open_api(bolt)

            print("apis opened")

        except Exception as e:
            for bolt in robot_group:
                self.close_api(bolt)
            print("Apis closed")
            raise e

            return

        try:
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
        finally:
            for bolt in robot_group:
                self.close_api(bolt)
            print("Apis closed")

            return

    def create_bolt_group(self, bolt_group):

        for bolt in bolt_group:
            self.bolt_group.assign_bolt(bolt)

    def open_api(self, bolt: Bolt):
        """
        Funktion zum Öffnen der dauerhaften Bluetooth-Verbindung zum Bolt-Roboter.
        Wenn die Verbindung nicht funktioniert, wird der Verbindungs-Versuch 3 mal wiederholt.

        :param bolt: Bolt Instanz, die Verbindung zum Roboter hält
        """
        retries = 0
        max_retries = 4
        for attempt in range(max_retries):
            try:
                retries += 1
                bolt.toy_api.__enter__()
                # bolt.calibrate()
                bolt.toy_api.scroll_matrix_text("Hi", color=Color(r=100, g=0, b=100), fps=5, wait=True)
                # Wenn erfolgreich, Schleife verlassen
                print(f"{bolt.name} erfolgreich verbunden!")
                break
            except TimeoutError as e:
                print(f"TimeoutError für {bolt.name}. Versuch {retries} von {max_retries}: {e}")
                if retries == max_retries:
                    print(f"Maximale Anzahl von Versuchen für {bolt.name} erreicht. Abbruch.")
                    raise
            except BleakDeviceNotFoundError as e:
                print(f"BleakDeviceNotFoundError in open_apis für {bolt.name}: {e}")
                if retries == max_retries:
                    print(f"Maximale Anzahl von Versuchen für {bolt.name} erreicht. Abbruch.")
                    raise
            except Exception as e:
                print(f"Exception in open_apis für {bolt.name}: {e}")
                if retries == max_retries:
                    print(f"Maximale Anzahl von Versuchen für {bolt.name} erreicht. Abbruch.")
                    raise

    def close_api(self, bolt: Bolt):
        """
        Schließt die Verbindung zum Bolt-Roboter.

        :param bolt: Bolt Instanz, die Verbindung zum Roboter hält
        """
        bolt.toy_api.__exit__(None, None, None)
