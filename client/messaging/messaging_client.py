import json
import os


def hardcodedMessage():
        # datei laden als zwischenlösung bis json gebaut wird
        exampleFilePath = os.path.join(os.path.dirname(__file__), "exampleMessage.json")
        with open(exampleFilePath, 'r', encoding='utf-8') as file:
                json_data = json.load(file) 

                json_string = json.dumps(json_data)

                return json_string

def create_json_message():
        """
        Nimmt Konsolen-Input und kodiert diesen als json-Nachricht.
        Wenn kein Input gegeben wurde, wird eine Default-Nachricht zurückgegeben.
        :return:
        """
        robots = input("Gib eine Liste von Robotern ein: ").strip()
        choreography = input("Gib die Choreografie ein: ").strip()
        strategy = input("Gib eine Strategie ein: ").strip()

        if not robots:
            print("Eingabe war leer, also Default Nachricht an Server.")
            return hardcodedMessage()

        data = {
                "robots": [robot.strip() for robot in robots.split(",")],
                "choreography": choreography.strip(),
                "strategy": strategy.strip(),
                "message": ""
        }

        return json.dumps(data)

def continuing_message():
        message = input("Nachricht an Server (\"exit\" schließt Verbindung): ").strip()

        if not message:
                print("Eingabe war leer")
                return None

        data = {
                "robots": "",
                "choreography": "",
                "strategy": "",
                "message": message
        }

        return json.dumps(data)

