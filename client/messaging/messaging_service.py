import json
import os
import random
from datetime import datetime

class MessagingService:

    def create_json_message(self, msg_type, payload):
        return json.dumps({
            "type": msg_type,
            "payload": payload
        })

    def create_hardcoded_message(self):
        exampleFilePath = os.path.join(os.path.dirname(__file__), "exampleMessage.json")
        with open(exampleFilePath, 'r', encoding='utf-8') as file:
            json_data = json.load(file)
        return self.create_json_message("command", json_data)


    def create_message(self, choreography="", values=[], message=""):
        payload = {
            "choreography": choreography,
            "values": values,
            "message": message
        }
        return self.create_json_message("command", payload)


    def create_disconnect_message(self):
        payload = {
            "robots": [],
            "choreography": "",
            "values": [],
            "message": "stopp"
        }
        return self.create_json_message("command", payload)


    def decode_message(self, json_message):
        data = json.loads(json_message)
        return data.get("payload", {}).get("message", "")
