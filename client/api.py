import time

import client.messaging.messaging_service as MessagingService
from client.client_test import WebsocketClient


# Datei mit Funktionen, die von der API angeboten werden.
# Vorderste Schicht zur Nutzerin

class ClientAPI:
    def __init__(self):
        self.client = WebsocketClient()

    def connect_server(self):
        self.client.connect_to_server()

    def disconnect_server(self):
        self.client.disconnect_from_server()

    def start_choreography(self):
        """Choreographie starten."""
        message = MessagingService.continuing_message("startchoreo")

        response = self.client.communicate_with_server(message)
        while "ToyNotFoundError" in response:
            response = self.client.communicate_with_server(message)
            print("Nochmal...")

        return response

    def select_choreography(self, choreography, values):
        message = MessagingService.select_choreography_message(choreography, values)

        print(self.client.communicate_with_server(message))
        print("Stelle die Roboter jetzt richtig hin!")
        time.sleep(20)

    def swap_positions(self):
        pass

    def dont_swap_positions(self):
        pass
