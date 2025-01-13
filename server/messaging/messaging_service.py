import json

from server.controller import Controller


def decode_message(json_data):
    controller = Controller()
    data = json.loads(json_data)
    response = ""

    choreography = data["choreography"]
    robots = data["robots"]
    strategy = data["strategy"]
    values = data["values"]
    message = data["message"]

    if choreography:
        response = controller.control_initial_connect(robots, choreography, strategy)

    if message == "los":
        controller.control_connected()

    elif message == "stopp":
        controller.control_disconnect()

    else:
        controller.control_initial_connect(robots, choreography, strategy)

    return code_response(response)


def code_response(response):
    data = {
        "message": response
    }
    return json.dumps(data)
