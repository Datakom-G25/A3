#################################################################################
# A Chat Client application. Used in the course IELEx2001 Computer networks, NTNU
#################################################################################

from socket import *

# --------------------
# Constants
# --------------------
# The states that the application can be in
states = [
    "disconnected",  # Connection to a chat server is not established
    "connected",  # Connected to a chat server, but not authorized (not logged in)
    "authorized"  # Connected and authorized (logged in)
]
TCP_PORT = 1300  # TCP port used for communication
SERVER_HOST = "datakomm.work"  # Set this to either hostname (domain) or IP address of the chat server

# --------------------
# State variables
# --------------------
current_state = "disconnected"  # The current state of the system

must_run = True  # When this variable will be set to false, the application will stop

client_socket = None


def quit_application():
    global must_run
    must_run = False


def send_command(command, arguments):
    try:
        global client_socket
        request_to_send = command + " " + arguments + "\n"
        client_socket.send(request_to_send.encode())
        return True
    except IOError as e:
        print("Error happened: ", e)
        return False


def read_one_line(sock):
    newline_received = False
    message = ""
    while not newline_received:
        character = sock.recv(1).decode()
        if character == '\n':
            newline_received = True
        elif character == '\r':
            pass
        else:
            message += character
    return message


def get_servers_response():
    global client_socket
    server_response = read_one_line(client_socket)
    print(server_response)
    return server_response


def connect_to_server():
    global client_socket, current_state

    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((SERVER_HOST, TCP_PORT))
    current_state = "connected"

    send_command("sync", "")
    get_servers_response()


def disconnect_from_server():
    global client_socket, current_state
    client_socket.close()
    current_state = "disconnected"
    pass


def loginauth():
    global client_socket, current_state
    current_state = "authorized"
    username = input("Username:")
    send_command("login", username)
    get_servers_response()


def send_msg():
    global client_socket
    msg = input("Gimme the msg u wanna send: ")
    send_command("msg", msg)
    get_servers_response()


def send_pmsg():
    global client_socket
    msg = input("Gimme the msg u wanna send: ")
    recipient = input("Who u wanna send to?: ")
    send_command("privmsg", recipient + " " + msg)
    get_servers_response()


def get_inbox():
    try:
        send_command("inbox", "")
        response = get_servers_response()
        num_msg = int(response[6:])
        i = 1
        while i <= num_msg:
            get_servers_response()
            i += 1
        return True
    except IOError as e:
        print("Error happened: ", e)
        return False


def get_user_list():
    global client_socket
    send_command("users", "")
    get_servers_response()


def get_joke():
    global client_socket
    send_command("joke", "")
    get_servers_response()


available_actions = [
    {
        "description": "Connect to a chat server",
        "valid_states": ["disconnected"],
        "function": connect_to_server
    },
    {
        "description": "Disconnect from the server",
        "valid_states": ["connected", "authorized"],
        "function": disconnect_from_server
    },
    {
        "description": "Authorize (log in)",
        "valid_states": ["connected", "authorized"],
        "function": loginauth
    },

    {
        "description": "Send a public message",
        "valid_states": ["connected", "authorized"],
        "function": send_msg
    },
    {
        "description": "Send a private message",
        "valid_states": ["authorized"],
        "function": send_pmsg
    },
    {
        "description": "Read messages in the inbox",
        "valid_states": ["connected", "authorized"],
        # TODO Step 9 - implement reading messages from the inbox.
        # Hint: send the inbox command, find out how many messages there are. Then parse messages
        # one by one: find if it is a private or public message, who is the sender. Print this
        # information in a user friendly way
        "function": get_inbox
    },
    {
        "description": "See list of users",
        "valid_states": ["connected", "authorized"],
        "function": get_user_list
    },
    {
        "description": "Get a joke",
        "valid_states": ["connected", "authorized"],
        "function": get_joke
    },
    {
        "description": "Quit the application",
        "valid_states": ["disconnected", "connected", "authorized"],
        "function": quit_application
    },
]


def run_chat_client():
    try:
        while must_run:
            print_menu()
            action = select_user_action()
            perform_user_action(action)
        print("Thanks for watching. Like and subscribe! 👍")
    except IOError as e:
        print("Error happened: ", e)
        return False


def print_menu():
    """ Print the menu showing the available options """
    print("==============================================")
    print("What do you want to do now? ")
    print("==============================================")
    print("Available options:")
    i = 1
    for a in available_actions:
        if current_state in a["valid_states"]:
            # Only hint about the action if the current state allows it
            print("  %i) %s" % (i, a["description"]))
        i += 1
    print()


def select_user_action():
    number_of_actions = len(available_actions)
    hint = "Enter the number of your choice (1..%i):" % number_of_actions
    choice = input(hint)
    # Try to convert the input to an integer
    try:
        choice_int = int(choice)
    except ValueError:
        choice_int = -1

    if 1 <= choice_int <= number_of_actions:
        action = choice_int - 1
    else:
        action = None

    return action


def perform_user_action(action_index):
    if action_index is not None:
        print()
        action = available_actions[action_index]
        if current_state in action["valid_states"]:
            function_to_run = available_actions[action_index]["function"]
            if function_to_run is not None:
                function_to_run()
            else:
                print("Internal error: NOT IMPLEMENTED (no function assigned for the action)!")
        else:
            print("This function is not allowed in the current system state (%s)" % current_state)
    else:
        print("Invalid input, please choose a valid action")
    print()
    return None


# Entrypoint for the application.
if __name__ == '__main__':
    run_chat_client()
