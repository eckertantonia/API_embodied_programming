from client.api_embodied_programming import EmbodiedProgrammingAPI

# Nutzerin

if __name__ == "__main__":
    # ab hier dann api ansprechen :)
    embodied_programming_api = EmbodiedProgrammingAPI()
    embodied_programming_api.client.connect_to_server()

    # mit choreo

    choreo = "bubblesort"

    embodied_programming_api.select_choreography(choreo, [3, 6, 2, 5, 7])

    embodied_programming_api.start_choreography()

    # ohne choreo

    # embodied_programming_api.start([3,2,5,6])
    # embodied_programming_api.swap_positions([3, 2])
    #
    # embodied_programming_api.dont_swap_positions([5, 6])

    # start mit values übertragen
    # bewegungen anstoßen

    embodied_programming_api.client.disconnect_from_server()
