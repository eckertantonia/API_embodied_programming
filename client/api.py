import client.messaging.messaging_client as MessagingClient
from client.client_test import WebsocketClient


# Datei mit Funktionen, die von der API angeboten werden.
# Vorderste Schicht zur Nutzerin

class ClientAPI:
    def __init__(self):
        self.client = WebsocketClient()

    def start_choreography(self, choreography):
        """Choreographie starten."""
        message = MessagingClient.continuing_message(choreography)

        return self.client.communicate_with_server(message)

    def send_custom_message(self, custom_data: dict):
        """Benutzerdefinierte Nachricht senden."""
        message = {
            "action": "custom",
            "data": custom_data
        }
        return self.client.communicate_with_server(message)

    def connect_server(self):
        self.client.connect_to_server()

    def disconnect_server(self):
        self.client.disconnect_from_server()
