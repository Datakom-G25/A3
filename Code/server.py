from socket import *

def start_server():
    welcome_socket = socket(AF_INET, SOCK_STREAM)
    welcome_socket.bind("",5678)
    welcome_socket.listen(1)
    welcome_socket.accept()
    connection_socket, client_address = welcome_socket.accept()
    print("client connected from", client_address)
    connection_socket.close()
    welcome_socket.close()
    print("Server shutdown")



if __name__ == "__main__":
    start_server()