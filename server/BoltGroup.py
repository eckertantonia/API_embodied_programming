from bolt import Bolt
from typing import List
import uuid
class BoltGroup:
    def __init__(self):
        self.id = f"Group-{uuid.uuid4().int % 1000}"
        self.bolts : List[Bolt] = []

    def assignBolt(self, bolt:Bolt):
        # TODO check ob Bolt schon in Gruppe
        self.bolts.append(bolt)
    