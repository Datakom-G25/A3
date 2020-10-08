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
