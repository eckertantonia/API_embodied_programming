import json
from server.controller import control

def decodeMessage(jsonData):
    data = json.loads(jsonData)

    movement = data["movement"]
    boltName = data["bolt-name"]
    strategy = data["strategy"]

    control(movement=movement, boltName=boltName, strategy=strategy )

