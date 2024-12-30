from bolt import Bolt
from typing import List, Iterator
import uuid


class BoltGroup:
    def __init__(self):
        self.id = f"Group-{uuid.uuid4().int % 1000}"
        self.bolts: List[Bolt] = []

    def assign_bolt(self, bolt: Bolt):
        # TODO check ob Bolt schon in Gruppe
        self.bolts.append(bolt)

    def __iter__(self) -> Iterator[Bolt]:
        """Return an iterator over the bolts in the group."""
        return iter(self.bolts)
