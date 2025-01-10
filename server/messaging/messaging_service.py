import json
from server.controller import control_initial_connect, control_connected, control_disconnect


def decode_message(json_data):
    data = json.loads(json_data)

    choreography = data["choreography"]
    robots = data["robots"]
    strategy = data["strategy"]
    message = data["message"]

    if message == "los":
        control_connected()

    elif message == "stopp":
        control_disconnect()

    else:
        control_initial_connect(robots, choreography, strategy)
