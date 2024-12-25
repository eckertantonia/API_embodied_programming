import asyncio
from spherov2.sphero_edu import SpheroEduAPI
import logging


class Bolt:
    def __init__(self, toy):
        self.name = toy.name
        self.toy = toy
        self.toyApi = SpheroEduAPI

    def setBoltApi(self):
        print(f"setBoltAPI")
        self.toyApi = SpheroEduAPI(self.toy)
        print(f"Api gesetzt")

    def getApi(self) -> SpheroEduAPI:
        return self.toyApi

    