import json
import os
import random
from datetime import datetime


def create_json_message(msg_type, payload):
    return json.dumps({
        "type": msg_type,
        "payload": payload,
        "metadata": {
            "timestamp": datetime.now(),
            "request_id": generate_request_id()
        }
    })


def generate_request_id():
    return f"{random.randint(100000, 999999)}"


def create_hardcoded_message():
    exampleFilePath = os.path.join(os.path.dirname(__file__), "exampleMessage.json")
    with open(exampleFilePath, 'r', encoding='utf-8') as file:
        json_data = json.load(file)
    return create_json_message("command", json_data)


def create_message(choreography="", values=[], message=""):
    payload = {
        "choreography": choreography,
        "values": values,
        "message": message
    }
    return create_json_message("command", payload)


def create_disconnect_message():
    payload = {
        "robots": [],
        "choreography": "",
        "values": [],
        "message": "stopp"
    }
    return create_json_message("command", payload)


def decode_message(json_message):
    data = json.loads(json_message)
    return data.get("payload", {}).get("message", "")
