import socket
import threading
import sys, os, json, time
import curses
from curses.textpad import Textbox, rectangle
from termcolor import colored, cprint
import colorama


# Constants
SERVER_IP = sys.argv[2]             # default = socket.gethostname()
SERVER_PORT =  int(sys.argv[3])     # default = 8092 
SERVER_ADDRESS = (SERVER_IP, SERVER_PORT)
lines = ['Hi! Start typing messages for them to appear here.']


# Functions
def create_socket():
    """Returns the created socket"""
    try:
        return socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except Exception as e:
        cprint('Can not create a socket!', 'red')
        print(e)

def connect_to_server(socket, ip, port):
    """Connecting to the server"""
    try:
        socket.connect((ip, port))
    except Exception as e:
        cprint(f'Can not connect to {SERVER_ADDRESS}!\n\
Reason: IP/PORT might be wrong OR the server might be closed.', 'red')
        #print(e)
        exit()

def set_username(username):
    """This function is mostly for error correcting and then sending the
    username to the server."""
    if len(username) <= 12:
        connect_to_server(client_socket, SERVER_IP, SERVER_PORT)
        packet = {'sender':username, 'command':'join'}
        packet_str = json.dumps(packet) # The reason why we stringified (or
        # dumped) the JSON object into a string is that we can not send JSON
        # objects to the server and have to convert it to a string first.
        client_socket.send(packet_str.encode('utf-8')) # Send the username
        confirmation = client_socket.recv(24).decode('utf-8')
        # Checking if the same username exists
        if confirmation == 'Username already exists!':
            cprint('Username already exists!','red')
            client_socket.close()
            exit()
        elif confirmation == 'Username accepted.':
            cprint(f'Username "{username}" created successfully.', 'green')
            return username 
    elif len(username) > 12:
        cprint('Username too long, should be less than 12 characters!', 'red')
        cprint('Client socket is terminating...', 'magenta')
        client_socket.close()
        exit()

def main(stdscr):
    """Creating GUI with curses (library)"""
    y_max, x_max = stdscr.getmaxyx()
    stdscr.leaveok(True)
    def redraw(): 
        for i, line in enumerate(lines[-y_max+3:]):
            stdscr.addstr(1+i, 1, line)
            stdscr.clrtoeol()
        rectangle(stdscr, 0, 0, y_max-2, x_max-2)
        stdscr.refresh()
    def receive_message():
        """Receive message from the server"""
        while True:
            try:
                message_str = client_socket.recv(1024).decode('utf-8')
                lines.append(message_str)
                redraw()
            except Exception: # Necessary when killing the tread
                break
    threading.Thread(target=receive_message).start()       
    
    def send_message(username):
        """Send message to the server"""
        while True:
            try:
                redraw()
                message = Textbox(curses.newwin(1, x_max-2, y_max-1, 1)).edit()
                message = message[:-1] # For debugging, curses senda the last char as blank
                if message[0] == '/':
                    if message.startswith('/pm'):
                        receiver = message[4:].split(' ', 1)[0]
                        data = message[4:].split(' ', 1)[1]
                        packet = {'sender':username, 'to':receiver, 'command':'pm', 'data':data}
                    elif message.startswith('/who'):
                        packet = {'sender':username, 'command':'who'}
                    elif message.startswith('/rename'):
                        new_username = message[8:].split(' ', 1)[0]
                        packet = {'sender':username, 'command':'rename', 'data':new_username}
                        username = new_username
                    elif message.startswith('/leave'):
                        packet = {'sender':username, 'command':'leave'}
                        packet_str = json.dumps(packet)
                        client_socket.send(packet_str.encode('utf-8'))
                        cprint('You have left the chat.', 'red')
                        client_socket.close()
                        exit()
                    elif message.startswith('/help'):
                        packet = {'sender':username, 'command':'help'}
                    else:
                        # If an unkown command is sent:
                        data = message[1:].split(' ', 1)[0]
                        packet = {'sender':username, 'command':'unknown', 'data':data}
                    
                    packet_str = json.dumps(packet)
                    client_socket.send(packet_str.encode('utf-8'))

                else:
                    # If the message is not a command:
                    packet = {'sender':username, 'data':message}
                    packet_str = json.dumps(packet)
                    client_socket.send(packet_str.encode('utf-8'))
            except IndexError: # User input is blank
                lines.append('Please type something!')
            except Exception: # EOFError or KeyboardInterrupt or ConnectionLost
                cprint('You have left the chat. Reason: Connection lost to the server', 'red')
                try:
                    client_socket.close()
                    sys.exit(0)
                except SystemExit:
                    os._exit(0)
    send_message(username)


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
    time.sleep(0.2)
    cprint('Joining the chat...','yellow')
    time.sleep(0.5)
    curses.wrapper(main)

        
        
        
        
        
    
    





