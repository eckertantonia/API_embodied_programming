from abc import ABC, abstractmethod


class MovementStrategy(ABC):

    @abstractmethod
    async def drive(self, robots, points, offset=0):
        #TODO: brauch ich offset wenn ich robots uebergebe?
        return
