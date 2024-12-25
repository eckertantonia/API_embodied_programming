import json
from controller import control

def decodeMessage(jsonData):
    data = json.loads(jsonData)

    connect = data["connection"]
    boltName = data["bolt-name"]

    control(connection=connect, boltName=boltName)

