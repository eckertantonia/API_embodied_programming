import json
from server.controller import control


async def decode_message(json_data):
    data = json.loads(json_data)

    choreography = data["choreography"]
    robots = data["robots"]
    strategy = data["strategy"]

    control(robots, choreography, strategy)
