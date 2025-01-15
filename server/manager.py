from concurrent.futures import ThreadPoolExecutor
from typing import List

from bleak.exc import BleakDeviceNotFoundError
from spherov2 import scanner
from spherov2.scanner import ToyNotFoundError

from bolt import Bolt
from choreography import Choreography
from server.choreographies.BubbleSortChoreo import BubbleSortChoreo
from server.led_control import LEDControl

CHOREOGRAPHIES = {
    "bubblesort": BubbleSortChoreo
}


def _get_choreography_instance(choreography):
    choreography_class = CHOREOGRAPHIES.get(choreography)
    if choreography_class:
        return choreography_class()
    else:
        return None


class Manager:
    def __init__(self, choreography=None, values=[]):
        self.bolts: List[Bolt] = []
        self.choreography = choreography
        self.values = values
        self.led_control = LEDControl()

        # event um auf api verbindung zu warten
        # self.connection_event = asyncio.Event()
        self.executor = ThreadPoolExecutor()

    def _check_robot_in_list(self, name) -> Bolt:
        """
        Sucht in self.bolts nach Bolt mit bestimmtem Namen.

        :param name: string
        :return: Bolt
        """
        return next((bolt for bolt in self.bolts if bolt.name == name), None)

    def connect_bolts(self, robots):
        """
        TODO: Fehlermanagement bei Verbindung
        Creates task in running loop, calls correlating async function.

        :return:
        """
        if len(robots) != len(self.values):
            return f"Anzahl Robots und Anzahl Values passen nicht zusammen: robots:{len(robots)}, values: {len(self.values)}"

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
            future = self.executor.submit(self._find_toy_blocking, name)

            toy = future.result()

            bolt = Bolt(toy)
            bolt.position = (position, 0)
            bolt.value = value
            self._open_api(bolt)
            self.bolts.append(bolt)
            return "ok"
        except ToyNotFoundError:
            return (f"ToyNotFoundError for {name}")

        except TimeoutError:
            return (f"TimeOutError")

        except Exception as e:
            print(f"manager: toy {name} not found")
            raise

    def _find_toy_blocking(self, name: str):
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
                self.led_control.show_string(bolt, "Hi")
                self.led_control.show_character(bolt, str(bolt.position[0]))
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
        """
        Schließt die Verbindung zum Bolt-Roboter.

        :param bolt: Bolt Instanz, die Verbindung zum Roboter hält
        """

        for bolt in self.bolts:
            bolt.toy_api.__exit__(None, None, None)

    def start_choreo(self):
        """
        :return:
        """
        choreography = _get_choreography_instance(self.choreography)
        if not choreography:
            choreo = Choreography()
            choreo.start_choreography(self.bolts, self.choreography)
        else:
            choreography.set_bolts_and_values(self.bolts, self.values)
            choreography.start_choreo()
