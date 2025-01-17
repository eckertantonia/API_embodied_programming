from manager import Manager


class Controller:
    def __init__(self):
        self.manager = Manager()
        self.initial_connect = False

    def process_command(self, payload):
        choreography = payload.get("choreography")
        values = payload.get("values", [])
        message = payload.get("message", "")
        response = ""

        if not self.initial_connect:
            self.initial_connect = True
            response = self.control_initial_connect(values, choreography)

        elif message == "start":
            response = self.control_start()

        elif message == "stopp":
            return self.control_disconnect()

        elif message == "custom":
            return self.control_custom_start(values, choreography)
        else:
            return "Unknown command"

        return response

    def control_initial_connect(self, values, choreography):
        self.manager.values = values
        self.manager.choreo = choreography
        position_string = self.manager.connect_bolts()

        return f"Ordne die Roboter in folgender Reihenfolge an: \n" + position_string

    def control_disconnect(self):
        self.manager.close_api()
        return "Apis closed."

    def control_start(self):
        return self.manager.start()

    def control_custom_start(self, values, choreography):
        return self.manager.start(values, choreography)
