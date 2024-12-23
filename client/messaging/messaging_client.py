import json
import os


def codeMessage():
        # datei laden als zwischenlösung bis json gebaut wird
        exampleFilePath = os.path.join(os.path.dirname(__file__), "exampleMessage.json")
        with open(exampleFilePath, 'r', encoding='utf-8') as file:
                json_data = json.load(file) 

                json_string = json.dumps(json_data)

                return json_string