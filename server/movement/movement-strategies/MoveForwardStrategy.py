import MovementInterface

class MoveForwardStrategy(MovementInterface):
    def __call__(self, *args, **kwds):
        print("move forward")

    def move(self):
        print("move methode")
        return