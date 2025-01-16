import abc
from abc import abstractmethod

class ChoreographyInterface(metaclass=abc.ABCMeta):

    @classmethod
    def __subclasshook__(cls, subclass):
        return callable(subclass.start_choreo)

    @abstractmethod
    def start_choreo(self,  robot_group, values):
        raise NotImplementedError
