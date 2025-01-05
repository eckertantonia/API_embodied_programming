from spherov2.sphero_edu import SpheroEduAPI


class Bolt:
    def __init__(self, toy):
        self.name = toy.name
        self.toy = toy
        # self.toyApi = SpheroEduAPI(self.toy)  # API für den Sphero Toy initialisieren
        self.position = (0, 0)  # Standard-Startposition
        self.offset = 0 # Default 0, TODO berechnen

    def update_position(self, new_pos):
        """
        Aktualisiert Position des Bolts.

        :param new_pos: Tupel (x, y) mit neuen Positionen
        """
        self.position = new_pos

    # def get_spheroeduapi(self) -> SpheroEduAPI:
    #     """
    #     :return: SpheroEduApi-Instanz für den Bolt
    #     """
    #     try:
    #         return self.toyApi
    #     except Exception as e:
    #         print(f"Exception in Bolt.get_spheroeduapi: {e}")
    #         raise

    def calibrate(self):
        """
        Kalibriert Kompass des Bolts, setzt den Winkel-Offset-Wert zu Norden bzw. 0°.

        """
        self.toyApi.calibrate_compass()
        self.offset = self.toyApi._SpheroEduAPI__compass_zero
