import random

from spherov2.sphero_edu import SpheroEduAPI


class Bolt:
    def __init__(self, toy):
        self.name = toy.name
        self.toy = toy
        self.toy_api = SpheroEduAPI(self.toy)  # API für den Sphero Toy initialisieren
        self.position = (0, 0)  # Standard-Startposition
        self.offset = 0 # Default 0, TODO berechnen
        self.value = random.randint(0, 5)

    def update_position(self, new_pos):
        """
        Aktualisiert Position des Bolts.

        :param new_pos: Tupel (x, y) mit neuen Positionen
        """
        self.position = new_pos

    def get_spheroeduapi(self) -> SpheroEduAPI:
        """
        :return: SpheroEduApi-Instanz für den Bolt
        """
        try:
            return self.toy_api
        except Exception as e:
            print(f"Exception in Bolt.get_spheroeduapi: {e}")
            raise

    def calibrate(self):
        """
        Kalibriert Kompass des Bolts, setzt den Winkel-Offset-Wert zu Norden bzw. 0°.
        """
        self.toy_api.calibrate_compass()
        offset1 = self.toy_api._SpheroEduAPI__compass_zero
        print(f"offset {offset1}")
        self.toy_api.calibrate_compass()
        offset2 = self.toy_api._SpheroEduAPI__compass_zero
        print(f"offset {offset2}")
        self.toy_api.calibrate_compass()
        offset3 = self.toy_api._SpheroEduAPI__compass_zero
        print(f"offset {offset3}")
        self.toy_api.calibrate_compass()
        offset4 = self.toy_api._SpheroEduAPI__compass_zero
        print(f"offset {offset4}")

        # TODO: gewichteter Mittelwert?
        # ausblick kalibrierung von außen unterstützt
        self.offset = (offset4+offset3+offset2+offset1)/4
        print(f"offset final: {self.offset}")
