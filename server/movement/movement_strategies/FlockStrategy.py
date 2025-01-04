from abc import ABC

from server.movement.movement_strategies.MovementInterface import MovementInterface


class FlockStrategy(MovementInterface, ABC):
    def __init__(self):
        pass

    async def drive(self, robots):
        pass