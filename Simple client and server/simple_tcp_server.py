from socket import *
import threading


def run_server():
    # TODO - implement the logic of the server, according to the protocol.
    # Take a look at the tutorial to understand the basic blocks: creating a listening socket,
    # accepting the next client connection, sending and receiving messages and closing the connection
    print("Starting TCP server...")

    welcome_socket = socket(AF_INET, SOCK_STREAM)
    welcome_socket.bind(("",5678))
    welcome_socket.listen(1)
    print("Server is ready for clients")
    client_id = 1

    need_to_run = True
    while need_to_run:
        connection_socket, client_address = welcome_socket.accept()
        print("Client #%i connected" % client_id)
        client_id += 1
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

# Main entrypoint of the script
if __name__ == '__main__':
    run_server()


def read_one_line(welcome_socket):
    newline_received = False
    message = ""
    while not newline_received:
        character = client_socket.recv(1).decode()
        if (character == "\n"):
            newline_received = True
        elif character == "\r":
            pass
        else:
            message += character
    return message
