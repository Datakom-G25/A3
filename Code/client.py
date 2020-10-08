from socket import *

def read_one_line(client_socket):
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


def start_client():
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect(("localhost", 5678))
    command_to_send = input("message to send: ")
    cmd_as_bytes = command_to_send.encode()
    client_socket.send(cmd_as_bytes)
    server_response = client_socket.recv(100).decode()
    print("Servers response: ",server_response)

    client_socket.close()


def process_response(server_response):
    # Business logic for processing of one server response
    print("response from server:")
    print(server_response)


if __name__ == "__main__":
    start_client()

#WE MADE IT TO 6 MINUTES INTO PST5 CREATING A TCP SERVER