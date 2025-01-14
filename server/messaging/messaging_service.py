import json

from server.controller import Controller

controller = Controller()
def decode_message(json_data):

    try:
        # Erster Schritt: Entferne äußere Anführungszeichen und parse den String
        data_as_string = json.loads(json_data)

        # Zweiter Schritt: Parse den inneren JSON-String
        data = json.loads(data_as_string)
    except json.JSONDecodeError as e:
        print(f"JSONDecodeError: {e}")  # Fehler debuggen
        return json.dumps({"error": "Invalid JSON format", "details": str(e)})
    response = ""

    choreography = data["choreography"]
    robots = data["robots"]
    strategy = data["strategy"]
    values = data["values"]
    message = data["message"]

    if choreography:
        response = controller.control_initial_connect(robots, choreography, values)

    elif message == "startchoreo":
        controller.control_choreography()

    elif message == "los":
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
