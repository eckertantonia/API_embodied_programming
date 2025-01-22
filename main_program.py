from client.api_embodied_programming import EmbodiedProgrammingAPI

# Nutzerin

if __name__ == "__main__":

    embodied_programming_api = EmbodiedProgrammingAPI()
    embodied_programming_api.client.connect_to_server()

    # mit choreo
    choreo = "bubblesort"

    embodied_programming_api.select_choreography(choreo, [2, 6, 2, 5, 7]) # was passiert wenn 2 gleiche zahlen in liste?

    embodied_programming_api.start_choreography()

    # ohne choreo

    embodied_programming_api.start([3,2,5,6])
    embodied_programming_api.swap_positions([3, 2])

    embodied_programming_api.dont_swap_positions([5, 6])


    embodied_programming_api.client.disconnect_from_server()
