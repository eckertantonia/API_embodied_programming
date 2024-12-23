import json
from controller import control

async def decodeMessage(jsonData):
    data = json.loads(jsonData)

    connect = data["connection"]
    boltName = data["bolt-name"]

    await control(connection=connect, boltName=boltName)

