import random
from concurrent.futures import ThreadPoolExecutor
from typing import List

from bleak.exc import BleakDeviceNotFoundError
from spherov2 import scanner
from spherov2.scanner import ToyNotFoundError

from bolt import Bolt
from server.choreographies.MainChoreography import MainChoreography
from server.ledcontrol import LEDControl

sphero_bolt_names = ["SB-8EA0", "SB-3DAB", "SB-22E4", "SB-231B", "SB-025F"]


class Manager:
    def __init__(self):
        self._bolts: List[Bolt] = []
        self._main_choreo = MainChoreography()
        self.choreo = None
        self.values = None
        self._led_control = LEDControl()

        self._executor = ThreadPoolExecutor()

    def _check_robot_in_list(self, name) -> Bolt:
        """
        Sucht in self.bolts nach Bolt mit bestimmtem Namen.

        :param name: string
        :return: Bolt
        """
        return next((bolt for bolt in self._bolts if bolt.name == name), None)

    def connect_bolts(self):

        try:
            robots = random.sample(sphero_bolt_names, len(self.values))
        except Exception:
            raise NotEnoughRobotsForValuesException(self.values)

        try:
            for i, bolt in enumerate(robots):
                response = self._set_robot(bolt, i, self.values[i])
                while "ToyNotFoundError" in response or "TimeOutError" in response:
                    response = self._set_robot(bolt, i, self.values[i])

            position_string = ""
            for i in range(0, len(robots)):
                position_string += f"{i}     "

            return position_string
        except ToyNotFoundError as e:
            return "ToyNotFoundError"

    def _set_robot(self, name: str, position, value):

        try:
            future = self._executor.submit(self._find_toy_blocking, name)

            toy = future.result()

            bolt = Bolt(toy)
            bolt.position = (position, 0)
            bolt.value = value
            self._open_api(bolt)

            self._bolts.append(bolt)  # fuer disconnect
            self._main_choreo.bolt_group.assign_bolt(bolt)
            return "ok"
        except ToyNotFoundError:
            print("Toy not found")
            return (f"ToyNotFoundError for {name}")

        except TimeoutError:
            return (f"TimeOutError")

        except Exception as e:
            print(f"manager: toy {name} not found")
            raise

    @staticmethod
    def _find_toy_blocking(name: str):
        return scanner.find_toy(toy_name=name)

    def _open_api(self, bolt: Bolt):
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
                self._led_control.show_string(bolt, "Hi")
                self._led_control.show_character(bolt, str(bolt.position[0]))
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

    def close_api(self):
        for bolt in self._bolts:
            bolt.toy_api.__exit__(None, None, None)

    def start(self, values=None, choreo=None):
        self._main_choreo.values = self.values
        if not values:
            values = self.values
        if not choreo:
            choreo = self.choreo
        self._main_choreo.start_choreography(values, choreo)
        return "ok"


class NotEnoughRobotsForValuesException(Exception):
    def __init__(self, values):
        self.len_values = len(values)
        self.len_robots = len(sphero_bolt_names)
        self.message = (f"NotEnoughRobotsForValuesException: "
                        f"There are not enough robots for the amount of "
                        f"values you chose. Amount Values: {self.len_values}, Amount Robots: {self.len_robots}.")
        super().__init__(self.message)
