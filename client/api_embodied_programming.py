import time

from client.messaging.messaging_service import MessagingService
from client.socket_client import WebsocketClient


# Datei mit Funktionen, die von der API angeboten werden.
# Vorderste Schicht zur Nutzerin

class EmbodiedProgrammingAPI:
    def __init__(self):
        self.client = WebsocketClient()
        self.messaging = MessagingService()

    def connect_server(self):
        self.client.connect_to_server()

    def disconnect_server(self):
        self.client.disconnect_from_server()

    def start(self, values):
        message = self.messaging.create_message(values=values)
        print(self.client.communicate_with_server(message))

    def start_choreography(self):
        message = self.messaging.create_message(message="start")

        response = self.client.communicate_with_server(message)
        while "ToyNotFoundError" in response:
            response = self.client.communicate_with_server(message)
            print("Nochmal...")

        return response

    def select_choreography(self, choreography, values):
        message = self.messaging.create_message(choreography=choreography, values=values)

        print(self.client.communicate_with_server(message))
        print("Stelle die Roboter jetzt richtig hin!")
        time.sleep(20)

    def swap_positions(self, values):
        message = self.messaging.create_message(choreography="swap", values=values, message="custom")

        print(self.client.communicate_with_server(message))

    def dont_swap_positions(self, values):
        message = self.messaging.create_message( choreography="dont_swap", values=values, message="custom")

        print(self.client.communicate_with_server(message))
