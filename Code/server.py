from socket import *
import threading
from socket_lib import read_one_line


def start_server():
    #
    welcome_socket = socket(AF_INET, SOCK_STREAM)
    welcome_socket.bind(("", 5678))
    welcome_socket.listen(1)
    print("Server ready for client connections")
    client_id = 1

    need_to_run = True
    while need_to_run:
        connection_socket, client_address = welcome_socket.accept()
        print("Client #%i connected" % client_id)
        client_id +=1
        print("client connected from", client_address)
        client_thread = threading.Thread(target = handle_next_client, args = (connection_socket,client_id))
        client_thread.start()

    # Server shutdown
    welcome_socket.close()
    print("Server shutdown")


def handle_next_client(connection_socket, client_id):
    command = "Something"
    while command != "":
        command = read_one_line(connection_socket)
        print("Message from client #%i: %s" %(client_id, command))
        print("Message from client: ", command)
        if command == "ping":
            response = "PONG"
        else:
            response = command.upper()
        connection_socket.send(response.encode())
    connection_socket.close()


if __name__ == "__main__":
    start_server()
