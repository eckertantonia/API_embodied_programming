from abc import ABC, abstractmethod


class MovementInterface(ABC):

    @abstractmethod
    async def drive(self, robots):
        return
