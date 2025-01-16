from manager import Manager


class Controller:
    def __init__(self):
        self.manager = Manager()
        self.initial_connect = False

    def process_command(self, payload):
        choreography = payload.get("choreography")
        values = payload.get("values", [])
        message = payload.get("message", "")

        if not self.initial_connect:
            self.control_initial_connect(choreography, values)
            self.initial_connect = True

        if values and message:
            self.control_start(values, message)

        if message == "stopp":
            return self.control_disconnect()
        else:
            return "Unknown command"

    def control_initial_connect(self, choreography, values):
        self.manager.choreography = choreography
        self.manager.values = values
        position_string = self.manager.connect_bolts()

        return f"Ordne die Roboter in folgender Reihenfolge an: \n" + position_string

    def control_disconnect(self):
        self.manager.close_api()
        return "Apis closed."

    def control_start(self, values, message):
        self.manager.start(values, message)
