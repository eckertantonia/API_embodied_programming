import abc
from abc import abstractmethod

from server.bolt_group import BoltGroup


class MovementStrategy(metaclass=abc.ABCMeta):

    @classmethod
    def __subclasshook__(cls, subclass):
        return callable(subclass.drive)

    @abstractmethod
    def drive(self, robots: BoltGroup, points: []):
        raise NotImplementedError
