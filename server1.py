import socket
import select
import sys, json
from termcolor import colored, cprint
import colorama


# Constants
HEADER = 1024
SERVER_IP = '' # ipv4 10.249.212.98
SERVER_PORT = 8092
SERVER_ADDRESS = (SERVER_IP, SERVER_PORT)


# Functions
def create_socket():
    """Returns the created socket"""
    cprint('Server initialising...', 'yellow')
    try:
        return socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as e:
        cprint('Can not create a socket!', 'red')
        print(e)

def bind_socket(socket, ip, port):
    """Bind server ip and port to already created socket."""
    address = (ip, port)
    try:
        socket.bind(address)
        cprint(f'Listening on {ip, port}', 'green')
    except socket.error as e:
        cprint(f'Can not bind {address} to {socket}!', 'red')
        print(e)

def receive_message(client_socket):
    """Receive a message form the client"""
    try:
        message_str = client_socket.recv(1024).decode('utf-8')
        message = json.loads(message_str)
        return message
    except: # if client crashes
        return False


def broadcast(client_socket, message, incoming_socket):
    """Broadcast message from one client to others"""
    sender = message['sender']
    data = message['data']

    for socket in clients:
        if socket != incoming_socket: # everyone excluding the sender
            clients[socket].send(f'{sender}: {data}'.encode('utf-8'))


def send_pm(client_socket, message):  # do i need client_socket ??
    """Whispers to a user"""
    sender = message['sender']
    receiver = message['to']
    data = message['data']

    if receiver in clients:
        client_socket.send(f'To {receiver}: {data}'.encode('utf-8'))
        clients[receiver].send(f'From {sender}: {data}'.encode('utf-8'))
    #else:
    #    client_socket.send(f'User "{sender}" not found!'.encode('utf-8'))


def rename(client_socket, message):
    """Changes username of a client
    
    Fix:
    - [ ] Client address name doesn't change
    """
    sender = message['sender']
    new_name = message['data']
    
    if new_name in clients:
        # if wanted username already taken
        clients[sender].send(f'Username {new_name} arleady taken!'.encode('utf-8'))
    elif sender in clients:
        clients[new_name] = clients[sender]  # swaps new username with current
        del clients[sender] # deletes current
        clients[new_name].send(f'Username successfully changed {sender} -> {new_name}'.encode('utf-8'))
    
def who(client_socket, message):
    """Sends a list to the client who asked who is currently online"""
    online_users = []
    for online_user in clients: 
        online_users.append(online_user)
        client_socket.send(f'All online users {online_users}'.encode('utf-8'))


def handle_incoming_connections():
    server_socket.listen(16)  # max 16 connections
    while True: # Run as long as server.py is running
        r_sock, w_sock, e_sock = select.select(r_list, w_list, []) 
        for incoming_socket in r_sock:
            if incoming_socket == server_socket:
                # Server socket ready => Accept new connection
                client_socket, client_address = server_socket.accept()
                
                user = receive_message(client_socket) # first message to receive is the username
                username = user['sender']
                clients[username] = client_socket
                print(clients) #debug
                if user:
                # if a user with a username connets
                    r_list.append(client_socket)
                    #clients[client_socket] = {"data": user} # ???
                    cprint(f'Connection from {client_address} as {username} has been establised.', 'green') # on server only
                elif user is False: # if user leaves (or send nothing)
                    cprint(f'Connection from {client_address} as {username} has been lost!', 'red')
                    continue
            else:
                message = receive_message(incoming_socket)
                if message:
                    # Received data from connected socket. Send to all
                    cprint(f'Received {message} from {incoming_socket}.', 'white') # only server

                    
                    if 'command' in message:
                        if message['command'] == 'pm':
                            send_pm(client_socket, message)
                        elif message['command'] == 'who':
                            who(client_socket, message)
                        elif message['command'] == 'rename':
                            rename(client_socket, message)
                    else:
                        broadcast(client_socket, message, incoming_socket)

                elif message is False:
                    # Got end of file (this client closed). Remove client from list
                    cprint(f'Closed connection from {incoming_socket} aka {username}!', 'red')
                    r_list.remove(incoming_socket)
                    del clients[username]  # delete the socket instead of the username ???
                    continue


if __name__ == '__main__':
    colorama.init() # Bugfixing colours on Windows
    server_socket = create_socket()
    bind_socket(server_socket, SERVER_IP, SERVER_PORT)

    r_list = [server_socket]
    clients = {} 
    w_list = []
    handle_incoming_connections()

