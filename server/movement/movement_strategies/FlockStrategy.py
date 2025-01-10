from abc import ABC

from server.movement.movement_strategies.MovementStrategy import MovementStrategy


class FlockStrategy(MovementStrategy, ABC):
    def __init__(self):
        pass

    async def drive(self, robots):
        pass