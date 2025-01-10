import json
import os


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


def continuing_message():
        message = input("Nachricht an Server (\"los\" oder \"stopp\" oder \"try\"): ").strip()

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

