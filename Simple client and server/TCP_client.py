from time import sleep
from random import randint
from socket import *

HOST = "datakomm.work"
PORT = 1301

messages = ["Datakomm", "Hello from TCP", "Chuck is here", "xxx", "Deano", ""]


def choose_random_message():
    i = randint(0, len(messages)-1)
    return messages[i]
def start_client():
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    need_to_run = True
    while need_to_run:
        command_to_send = choose_random_message()
        command_to_send += "\n"
        client_socket.send(command_to_send.encode())
        server_response = client_socket.recv(100).decode()
        sleep(1)
        print("Servers response: ", server_response)
        if server_response == "":
            need_to_run = False

    client_socket.close()

def process_response(server_response):
    # Business logic for processing of one server response
    print("response from server:")
    print(server_response)

if __name__ == "__main__":
    start_client()
