import asyncio
import threading
from concurrent.futures import ThreadPoolExecutor
from typing import List

from bleak.exc import BleakDeviceNotFoundError
from setuptools.unicode_utils import try_encode
from spherov2.sphero_edu import SpheroEduAPI
from spherov2.types import Color

from BoltGroup import BoltGroup
from bolt import Bolt
from movement.movement_strategies.MoveForwardStrategy import MoveForwardStrategy
from server.choreographies.FlockChoreo import FlockChoreo
from server.choreographies.MixChoreo import MixChoreo
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
        self.movementStrategies = None
        self.boltGroup = BoltGroup()
        self.loop = asyncio.get_running_loop()

    def start_choreography(self, bolt_group: List[Bolt], choreography, strategy):
        """
        Initialer Start jeder Choreographie.

        :param bolt_group: List[Bolt], BoltGroup
        :param choreography: str
        :param strategy: str
        :return:
        """

        self.create_bolt_group(bolt_group)

        try:
            threads = []
            for bolt in bolt_group:
                thread = threading.Thread(target=self.open_api, args=(bolt,))
                threads.append(thread)
                thread.start()

            # Warten bis alle Threads ausgeführt wurden
            for thread in threads:
                thread.join()


        # choreo logik
            if choreography == "flock":
                flock = FlockChoreo(self.boltGroup)

                flock.start_choreo()

            elif choreography == "mix":
                mix = MixChoreo()

                mix.start_choreo(self.boltGroup, _get_strategy_instance(strategy))
        finally:
            for bolt in bolt_group:
                self.close_api(bolt)


    def create_bolt_group(self, bolt_group):

        for bolt in bolt_group:
            self.boltGroup.assign_bolt(bolt)

    def open_api(self, bolt: Bolt):
        """
        Funktion zum Öffnen der dauerhaften Bluetooth-Verbindung zum Bolt-Roboter.
        Wenn die Verbindung nicht funktioniert, wird der Verbindungs-Versuch 3 mal wiederholt.

        :param bolt: Bolt Instanz, die Verbindung zum Roboter hält
        """
        retries = 0
        max_retries = 3
        for attempt in range(max_retries):
            try:
                bolt.toyApi.__enter__()
                # bolt.calibrate()
                bolt.toyApi.scroll_matrix_text("Hi", color=Color(r=100, g=0, b=100), fps=5, wait=True)
                # Wenn erfolgreich, Schleife verlassen
                print(f"{bolt.name} erfolgreich verbunden!")
                break
            except TimeoutError as e:
                retries += 1
                print(f"TimeoutError für {bolt.name}. Versuch {retries} von {max_retries}: {e}")
                if retries >= max_retries:
                    print(f"Maximale Anzahl von Versuchen für {bolt.name} erreicht. Abbruch.")
                    raise
            except BleakDeviceNotFoundError as e:
                print(f"BleakDeviceNotFoundError in open_apis für {bolt.name}: {e}")
                if retries >= max_retries:
                    print(f"Maximale Anzahl von Versuchen für {bolt.name} erreicht. Abbruch.")
                    raise
            except Exception as e:
                print(f"Anderer Fehler in open_apis für {bolt.name}: {e}")
                if retries >= max_retries:
                    print(f"Maximale Anzahl von Versuchen für {bolt.name} erreicht. Abbruch.")
                    raise


    def close_api(self, bolt: Bolt):
        """
        Schließt die Verbindung zum Bolt-Roboter.

        :param bolt: Bolt Instanz, die Verbindung zum Roboter hält
        """
        bolt.toyApi.__exit__(None, None, None)