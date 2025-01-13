from client.api import ClientAPI

if __name__ == "__main__":
    # ab hier dann api ansprechen :)
    embodied_programming_api = ClientAPI()
    embodied_programming_api.client.connect_to_server()

    embodied_programming_api.start_choreography("try")

    embodied_programming_api.client.disconnect_from_server()


