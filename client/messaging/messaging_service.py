import json
import os
import random

robots = ["SB-8EA0", "SB-51FA", "SB-231B", "SB-3DAB", "SB-025F"]


def hardcoded_message():
    # datei laden als zwischenlösung bis json gebaut wird
    exampleFilePath = os.path.join(os.path.dirname(__file__), "exampleMessage.json")
    with open(exampleFilePath, 'r', encoding='utf-8') as file:
        json_data = json.load(file)

        json_string = json.dumps(json_data)

        return json_string


def create_initial_json_message():
    """
    Nimmt Konsolen-Input und kodiert diesen als json-Nachricht.
    Wenn kein Input gegeben wurde, wird eine Default-Nachricht zurückgegeben.
    :return:
    """

    return hardcoded_message()


def continuing_message(message):
    # message = input("Nachricht an Server (\"los\" oder \"stopp\" oder \"try\"): ").strip()

    if not message:
        print("Eingabe war leer")
        return None
    elif message == "try":
        return hardcoded_message()
    else:
        data = {
            "robots": "",
            "choreography": "",
            "strategy": "",
            "message": message
        }

        return json.dumps(data)


def select_choreography_message(choreography, values):
    if len(values) > len(robots):
        raise
    choreo_robots = random.sample(robots, len(values))
    data = {
        "robots": choreo_robots,
        "choreography": choreography,
        "strategy": "",
        "values": values,
        "message": ""
    }

    return json.dumps(data)


def decode_message(message):
    data = json.loads(message)
    message = data["message"]
    return message


class NotEnoughRobotsForValuesException(Exception):
    def __init__(self, values):
        self.len_values = len(values)
        self.len_robots = len(robots)
        self.message = (f"NotEnoughRobotsForValuesException: "
                        f"There are not enough robots for the amount of "
                        f"values you chose. Amount Values: {self.len_values}, Amount Robots: {self.len_robots}.")
        super().__init__(self.message)
