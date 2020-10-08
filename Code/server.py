from socket import *


def start_server():
    welcome_socket = socket(AF_INET, SOCK_STREAM)
    welcome_socket.bind(("", 5678))
    welcome_socket.listen(1)
    print("Server ready for client connections")
    connection_socket, client_address = welcome_socket.accept()
    print("client connected from", client_address)
    message = connection_socket.recv(100).decode()
    print("message recieved from client: ", message)
    response = message.upper()
    connection_socket.send(response.encode())
    connection_socket.close()
    welcome_socket.close()
    print("Server shutdown")


if __name__ == "__main__":
    start_server()
