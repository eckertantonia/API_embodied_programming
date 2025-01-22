import abc
from abc import abstractmethod

from server.boltgroup import BoltGroup


class MovementStrategy(metaclass=abc.ABCMeta):

    @classmethod
    def __subclasshook__(cls, subclass):
        return callable(subclass.drive)

    @abstractmethod
    def drive(self, robots: BoltGroup, points: []):
        raise NotImplementedError
