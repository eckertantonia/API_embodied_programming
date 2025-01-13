import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import List

from bleak.exc import BleakDeviceNotFoundError
from spherov2 import scanner
from spherov2.scanner import ToyNotFoundError

from bolt import Bolt
from choreography import Choreography
from server.led_control import LEDControl


class Manager:
    def __init__(self, choreography=None, strategy=None):
        self.bolts: List[Bolt] = []
        self.choreography = None
        self.strategy = None
        self.led_control = LEDControl()

        # event um auf api verbindung zu warten
        self.connection_event = asyncio.Event()
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
        for i, bolt in enumerate(robots):
            self._set_robot(bolt, i)

        position_string = ""
        for i in range(0, len(robots)):
            position_string += f"{i}     "

        return position_string

    def _set_robot(self, name: str, position):

        try:
            future = self.executor.submit(self._find_toy_blocking, name)

            toy = future.result()

            bolt = Bolt(toy)
            bolt.position = (position, 0)
            self._open_api(bolt)
            self.bolts.append(bolt)
        except ToyNotFoundError as e:
            print(f"ToyNotFoundError for {name}")
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
                self.led_control.show_grouping(bolt)
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

        :param robots: BoltGroup
        :param choreography: string
        :param strategy: string
        :return:
        """
        choreo = Choreography()
        choreo.start_choreography(self.bolts, self.choreography, self.strategy)
