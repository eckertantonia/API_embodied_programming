import time

from client.api import ClientAPI

# Nutzerin

if __name__ == "__main__":
    # ab hier dann api ansprechen :)
    embodied_programming_api = ClientAPI()
    embodied_programming_api.client.connect_to_server()

    # mit choreo

    choreo = "bubblesort"

    embodied_programming_api.select_choreography(choreo, [3,6,2,5,7])

    embodied_programming_api.start_choreography()

    embodied_programming_api.client.disconnect_from_server()

    # ohne choreo

    # start mit values übertragen
    # bewegungen anstoßen




