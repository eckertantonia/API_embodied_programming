#!/usr/bin/env python3.8

import socket
import threading

import server.messaging.messaging_service as messaging


def handle_client(client_socket, addr):
    try:
        while True:
            # receive and print client messages
            request = client_socket.recv(1024).decode("utf-8").strip()
            if not request:
                continue
            elif request.lower() == "close":
                client_socket.send("closed".encode("utf-8"))
                break
            else:
                # TODO: messaging_service richtig einbinden, am liebsten ohne async :)
                response = messaging.decode_message(request)
            print(f"Received: {request}")

            # convert and send accept response to the client
            client_socket.send(response.encode("utf-8"))
    except Exception as e:
        print(f"Error when handling client: {e}")
    finally:
        client_socket.close()
        print(f"Connection to client ({addr[0]}:{addr[1]}) closed")


def run_server():
    server_ip = "127.0.0.1"
    port = 8765
    # create a socket object
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # bind the socket to a specific address and port
    server.bind((server_ip, port))

    try:
        # listen for incoming connections
        server.listen(0)
        print(f"Listening on {server_ip}:{port}")

        # accept incoming connections
        client_socket, client_address = server.accept()
        print(f"Accepted connection from {client_address[0]}:{client_address[1]}")

        # threading um mehrere clients zu akzeptieren
        thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        thread.start()

    except Exception as e:
        print(f"Error: {e}")
    finally:
        server.close()


if __name__ == "__main__":
    run_server()
