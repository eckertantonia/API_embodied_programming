from abc import ABC, abstractmethod

class MovementInterface(ABC):

    @abstractmethod
    def move(self):
        return

