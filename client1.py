import socket
import sys, json
import threading
from termcolor import colored, cprint
import colorama

# Constants
SERVER_IP = socket.gethostname()        #argv[2]
SERVER_PORT = 8092                      #argv[3]
#HEADER = 5
SERVER_ADDRESS = (SERVER_IP, SERVER_PORT)


# Functions
def create_socket():
    """Returns the created socket"""
    try:
        return socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as e:
        cprint('Can not create a socket!', 'red')
        print(e)

def connect_to_server(client_socket, ip, port):
    """Connecting to the server"""
    try:
        client_socket.connect((ip, port))
        cprint('You have conncted to the server.', 'green')
    except socket.error as e:
        cprint(f'Can not connect to {SERVER_ADDRESS}!', 'red')
        print(e)

def set_username(username):
    """This function is mostly for error correcting and then
    sending the username to the server."""
    if len(username) <= 12:
        cprint(f'Username {username} created successfully.', 'green')
        connect_to_server(client_socket, SERVER_IP, SERVER_PORT) # Connect to the server
        packet = {'sender':username, 'command':'join'} #test
        packet_str = json.dumps(packet) #test
        client_socket.send(packet_str.encode('utf-8')) # send username
        return username 
    elif len(username) > 12:
        cprint('Username too long.', 'red')
        cprint('Client socket is terminating...', 'magenta')
        client_socket.close()
        exit()

def send_message():
    """Send message to the server"""
    while True:
        message = input("Send a message to the server: ")
        if message[0] == '/': # make exception, if message blank -> skip !!
            if message.startswith('/pm'):
                receiver = message[4:].split(' ', 1)[0]
                data = message[4:].split(' ', 1)[1]
                packet = {'sender':username, 'to':receiver, 'command':'pm', 'data':data}
            elif message.startswith('/who'):
                packet = {'sender':username, 'command':'who'}
            elif message.startswith('/rename'):
                new_username = message[8:].split(' ', 1)[0]
                packet = {'sender':username, 'command':'rename', 'data':new_username}
            elif message.startswith('/leave'):
                packet = {'sender':username, 'command':'leave'}
                packet_str = json.dumps(packet)
                client_socket.send(packet_str.encode('utf-8'))
                cprint('You have left the chat.', 'green')  # force to close from server !!!
                #client_socket.close()
                exit()
            elif message.startswith('/help'):
                packet = {'sender':username, 'command':'help'}

            packet_str = json.dumps(packet)
            client_socket.send(packet_str.encode('utf-8'))
        else:
            packet = {'sender':username, 'data':message}
            packet_str = json.dumps(packet)
            client_socket.send(packet_str.encode('utf-8'))


def receive_message():
    """Receive message from the server"""
    while True:
        message_str = client_socket.recv(1024).decode('utf-8')
        print(message_str)


# Main
if __name__ == '__main__':
    colorama.init() # Bugfixing colours on Windows
    client_socket = create_socket()
    try:
        username = set_username(sys.argv[1])
    except IndexError:
        cprint('Username not set.', 'red')
        cprint('Client socket is terminating...', 'magenta')
        client_socket.close()
        exit()
        

    
send_thread = threading.Thread(target=send_message)
send_thread.start()


receive_thread = threading.Thread(target=receive_message)
receive_thread.start() 
        
        
        
        
        
    
    





