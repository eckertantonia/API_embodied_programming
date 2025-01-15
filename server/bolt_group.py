from bolt import Bolt
from typing import List, Iterator
import uuid


class BoltGroup:
    def __init__(self, bolts=None):
        self.id = f"Group-{uuid.uuid4().int % 1000}"
        if bolts is None:
            bolts = []
        self.bolts: List[Bolt] = bolts

    def assign_bolt(self, bolt: Bolt):
        # TODO check ob Bolt schon in Gruppe
        self.bolts.append(bolt)

    def remove_bolt(self, bolt: Bolt):
        """Entfernt einen Bolt aus der Gruppe, falls vorhanden."""
        if bolt in self.bolts:
            self.bolts.remove(bolt)
            print(f"{bolt} wurde aus der Gruppe entfernt.")
        else:
            print(f"{bolt} ist nicht in der Gruppe und kann nicht entfernt werden.")

    def clear_bolts(self):
        """Leert die gesamte Liste der Bolts."""
        self.bolts.clear()
        print("Alle Bolts wurden aus der Gruppe entfernt.")

    def __iter__(self) -> Iterator[Bolt]:
        """Return an iterator over the bolts in the group."""
        return iter(self.bolts)

    def __getitem__(self, index: int) -> Bolt:
        """Retrieve a bolt by index."""
        return self.bolts[index]

    def __len__(self):
        return len(self.bolts)
