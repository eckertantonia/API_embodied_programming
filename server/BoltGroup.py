from bolt import Bolt
from spherov2.sphero_edu import SpheroEduAPI
from typing import List, Iterator, Dict
import uuid


class BoltGroup:
    def __init__(self):
        self.id = f"Group-{uuid.uuid4().int % 1000}"
        self.bolts: Dict["Bolt", "SpheroEduAPI"] = {}  # Map Bolt zu API

    def assign_bolt(self, bolt: "Bolt", api: "SpheroEduAPI"):
        """Fügt einen Bolt und dessen API der Gruppe hinzu."""
        if bolt in self.bolts:
            raise ValueError(f"Bolt {bolt} ist bereits in der Gruppe.")
        self.bolts[bolt] = api

    def get_api(self, bolt: "Bolt") -> "SpheroEduAPI":
        """Gibt die API zurück, die einem bestimmten Bolt zugeordnet ist."""
        return self.bolts.get(bolt)

    def __iter__(self) -> Iterator[Bolt]:
        """Return an iterator over the bolts in the group."""
        return iter(self.bolts)

    def __getitem__(self, index: int) -> Bolt:
        """Retrieve a bolt by index."""
        return list(self.bolts.keys())[index]
