from datetime import datetime
import json
from server.controller import Controller


class MessagingService:
    def __init__(self):
        self.controller = Controller()

    def process_status_request(self,payload):
        status_type = payload.get("status_type", "general")

        if status_type == "general":
            # Allgemeine Informationen über das System
            return {
                "system_status": "online"
            }
        else:
            # Unbekannte Statusanfrage
            return {
                "error": f"Unknown status_type: {status_type}"
            }


    def handle_client_message(self, json_message):
        try:
            data = json.loads(json.loads(json_message))


            # Nachrichtentyp und Payload extrahieren
            msg_type = data.get("type")
            payload = data.get("payload", {})
            response = ""

            # Logik basierend auf dem Typ der Nachricht
            if msg_type == "command":
                response = self.controller.process_command(payload)
            elif msg_type == "status":
                response = self.process_status_request(payload)
            else:
                return self.create_error_response("Unknown message type", f"Type: {msg_type}")

            return self.create_response(response)
        except json.JSONDecodeError as e:
            return self.create_error_response("Invalid JSON format", str(e))
        except Exception as e:
            return self.create_error_response("Error", str(e))





    def create_response(self, response):
        """
        Erstellt eine Antwort-Nachricht.
        """
        return json.dumps({
            "type": "response",
            "payload": {
                "message": response
            }
        })


    def create_error_response(self, error_message, details):
        """
        Erstellt eine Fehlermeldung.
        """
        return json.dumps({
            "type": "error",
            "payload": {
                "error": error_message,
                "details": details
            }
        })
