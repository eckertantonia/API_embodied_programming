from abc import ABC, abstractmethod


class MovementInterface(ABC):

    @abstractmethod
    def drive(self, robot):
        return
