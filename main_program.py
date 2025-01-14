import time

from client.api import ClientAPI

if __name__ == "__main__":
    # ab hier dann api ansprechen :)
    embodied_programming_api = ClientAPI()
    embodied_programming_api.client.connect_to_server()

    embodied_programming_api.select_choreography("mix", [6,3,5,7,2])
    print("sleep 20")
    time.sleep(20)

    embodied_programming_api.start_choreography("mix")

    embodied_programming_api.client.disconnect_from_server()


