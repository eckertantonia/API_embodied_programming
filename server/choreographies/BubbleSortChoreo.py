from spherov2.types import Color

from server.bolt_group import BoltGroup


class BubbleSortChoreo:
    def __init__(self, bolts: [], values: []):
        self.bolt_group = BoltGroup(bolts)
        self.values = values

    def choreo(self):

        # algorithmus

        pass

    def positioning(self):
        for i, bolt in enumerate(self.bolt_group.bolts):
            bolt.calibrate()
            bolt.position = (0, i)
            bolt.value = self.values[i]
            bolt.toy_api.set_matrix_character(f"{i}", color=Color(r=100, g=0, b=100))
