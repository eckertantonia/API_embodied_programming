from abc import ABC, abstractmethod


class MovementInterface(ABC):

    @abstractmethod
    async def drive(self, robot, robot_api, points, initial_heading=None, offset=0):
        return
