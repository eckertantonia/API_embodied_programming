from manager import Manager


class Controller:
    def __init__(self):
        self.manager = None

    def control_initial_connect(self, robots, choreography, strategy):
        self.manager = Manager(choreography, strategy)

        position_string = self.manager.connect_bolts(robots)

        return f"Ordne die Roboter in folgender Reihenfolge an: \n" + position_string

    def control_disconnect(self):
        self.manager.close_api()
        return "Apis closed."

    def control_choreography(self):
        self.manager.start_choreo()

    def control_connected(self):
        pass
