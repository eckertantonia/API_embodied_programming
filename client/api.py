import client.messaging.messaging_service as MessagingService
from client.client_test import WebsocketClient


# Datei mit Funktionen, die von der API angeboten werden.
# Vorderste Schicht zur Nutzerin

class ClientAPI:
    def __init__(self):
        self.client = WebsocketClient()

    def start_choreography(self, choreography):
        """Choreographie starten."""
        message = MessagingService.continuing_message(choreography)

        print(self.client.communicate_with_server(message))

    def select_choreography(self, choreography, values):
        message = MessagingService.select_choreography_message(choreography, values)

        print(self.client.communicate_with_server(message))

    def send_custom_message(self, custom_data: dict):
        """Benutzerdefinierte Nachricht senden."""
        message = {
            "action": "custom",
            "data": custom_data
        }
        print(self.client.communicate_with_server(message))

    def connect_server(self):
        self.client.connect_to_server()

    def disconnect_server(self):
        self.client.disconnect_from_server()
