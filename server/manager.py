import asyncio
import threading
from typing import List

from bleak.exc import BleakDeviceNotFoundError
from spherov2 import scanner

from bolt import Bolt
from choreography import Choreography


class Manager:
    def __init__(self):
        self.bolts: List[Bolt] = []
        self.choreography = None
        self.strategy = None

        # event um auf api verbindung zu warten
        self.connection_event = asyncio.Event()

    def _check_robot_in_list(self, name) -> Bolt:
        """
        Sucht in self.bolts nach Bolt mit bestimmtem Namen.

        :param name: string
        :return: Bolt
        """
        return next((bolt for bolt in self.bolts if bolt.name == name), None)

    def connect_bolts(self, bolts: List[str], choreography, strategy):
        """
        TODO: Fehlermanagement bei Verbindung
        Creates task in running loop, calls correlating async function.

        :param bolts:
        :param choreography:
        :param strategy:
        :return:
        """

        # TODO: bessere Loesung finden
        self.choreography = choreography
        self.strategy = strategy

        threads = []
        for bolt in bolts:
            thread = threading.Thread(target=self._set_robot, args=(bolt,))
            threads.append(thread)
            thread.start()

        # Wait for all threads to finish
        for thread in threads:
            thread.join()


    def _set_robot(self, name: str):

        try:
            toy = scanner.find_toy(toy_name=name)
            bolt = Bolt(toy)
            self._open_api(bolt)
            self.bolts.append(bolt)
        except Exception as e:
            print(f"manager: toy {name} not found")
            raise

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
