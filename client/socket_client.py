import json
import socket
from json import JSONDecodeError

import client.messaging.messaging_service as messaging
from client.messaging.messaging_service import MessagingService


class WebsocketClient:
    def __init__(self):
        self.server_ip = "127.0.0.1"
        self.server_port = 8765
        self.socket = None
        self.messaging = MessagingService()

    def connect_to_server(self):

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.server_ip, self.server_port))

        print(f"Verbunden mit Server.")

    def disconnect_from_server(self, message):
        self._send_message(message)
        if self.socket:
            self.socket.close()
            self.socket = None
            print("Verbindung mit Server getrennt.")

    def _send_message(self, message: dict):
        if not self.socket:
            raise ConnectionError("Keine aktive Verbindung zum Server.")

        json_message = json.dumps(message)
        self.socket.send(json_message.encode("utf-8")[:1024])
        print(f"gesendet: {json_message}")

    def _receive_message(self) -> dict:
        if not self.socket:
            raise ConnectionError("Keine aktive Verbindung zum Server.")
        try:
            response = (self.socket.recv(1024))
            print(f"empfangen: {response}")
            return response
        except JSONDecodeError as e:
            print(f"JSONDecodeError caused by response: {response}")

    def communicate_with_server(self, message):
        self._send_message(message)
        response = self._receive_message()
        return self.messaging.decode_message(response)
