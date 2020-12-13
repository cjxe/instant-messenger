import socket
import select
import threading
import sys, os, json, time
from time import gmtime, strftime
import logging
from termcolor import colored, cprint
import colorama


# Constants
SERVER_IP = socket.gethostname()    # ipv4
SERVER_PORT = int(sys.argv[1])      # default = 8092 
SERVER_ADDRESS = (SERVER_IP, SERVER_PORT)


# Functions
def create_socket():
    """Returns the created socket"""
    cprint('Server initialising...', 'yellow')
    try:
        logging.info('SERVER Server initialising...')
        return socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except Exception as e:
        logging.error('SERVER Can not create a socket!')
        cprint('Can not create a socket!', 'red')
        print(e)

def bind_socket(socket, ip, port):
    """Bind server ip and port to already created socket."""
    address = (ip, port)
    try:
        socket.bind(address)
        logging.info(f'SERVER Listening on {ip, port}')
        cprint(f'Listening on {ip, port}', 'green')
    except Exception as e:
        logging.error(f'SERVER Can not bind {address} to {socket}! Reason: PORT\
         might be occupied')
        cprint(f'Can not bind {address} to {socket}!\nReason: PORT might be\
         occupied.', 'red')
        #print(e)
        try: # Necessary in order to shut down.
            exit()
        except SystemExit:
            os._exit(0)
        
def receive_message(socket):
    """Decodes the incoming message from the client and loads it as a JSON file
    """
    try:
        message_str = socket.recv(1024).decode('utf-8')
        message = json.loads(message_str)
        return message
    except:
        return False

def broadcast_message(message):
    """Broadcast message from one client to everyone"""
    sender = message['sender']
    data = message['data']

    for socket in clients:
        clients[socket].send(f'{sender}: {data}'.encode('utf-8'))
    logging.info(f'MESSAGE {message["sender"]} \"{message["data"]}\"')

def broadcast_message_but_sender(message, incoming_socket):
    """Broadcast message from one client to everyone but the sender"""
    sender = message['sender']
    data = message['data']

    for socket in clients:
        if incoming_socket != clients[socket]: # everyone excluding the sender
            clients[socket].send(f'{sender}: {data}'.encode('utf-8'))
    logging.info(f'MESSAGE {message["sender"]} \"{message["data"]}\"')

def broadcast(string):
    """Broadcast message from the server to everyone"""
    for socket in clients:
        try:
            clients[socket].send(f'{string}'.encode('utf-8'))
        except ConnectionResetError or Exception as e:
            continue

def send_pm(message):
    """Whispers to a user"""
    sender = message['sender']
    receiver = message['to']
    data = message['data']

    if receiver in clients:
        if sender == receiver:
            # If sender and receiver is the same client
            logging.error(f'fCOMMAND {sender} \"/{message["command"]} {receiver} {data}\"')
            clients[sender].send(f'You can not pm yourself!'.encode('utf-8'))
        else:
            logging.info(f'COMMAND {sender} \"/{message["command"]} {receiver} {data}\"')
            clients[sender].send(f'To {receiver}: {data}'.encode('utf-8'))
            clients[receiver].send(f'From {sender}: {data}'.encode('utf-8'))
    else:
        # If receiver does not exist
        logging.info(f'fCOMMAND {sender} \"/{message["command"]} {receiver} {data}\"')
        clients[sender].send(f'User "{receiver}" not found!'.encode('utf-8'))

def rename(message):
    """Changes clients username"""
    sender = message['sender']
    new_name = message['data']
    
    if new_name in clients:
        # If wanted username is already taken
        logging.error(f'fCOMMAND {sender} \"/{message["command"]} {new_name}\"')
        clients[sender].send(f'Username "{new_name}" arleady taken!'.encode('utf-8'))
    elif sender in clients:
        clients[new_name] = clients[sender]  # Swaps new username with current
        del clients[sender] # Deletes current/old username
        logging.info(f'COMMAND {sender} \"/{message["command"]} {new_name}\"')
        clients[new_name].send(f'Username successfully changed from "{sender}" -> "{new_name}"'.encode('utf-8'))
        broadcast(f'"{sender}" has changed their name to "{new_name}"!')

def who(message):
    """Return the list of all online users."""
    sender = message['sender']

    online_users = []
    for online_user in clients: 
        online_users.append(online_user)
    logging.info(f'COMMAND {sender} \"/{message["command"]}\"')
    clients[sender].send(f'All online users {online_users}'.encode('utf-8'))

def kick(message, incoming_socket):
    """Kicks the user"""
    sender = message['sender']

    cprint(f'Closed connection from {incoming_socket} aka "{sender}"! Reason: User input.', 'red')
    logging.info(f'COMMAND {sender} \"/{message["command"]}\"')
    logging.info(f'LEAVE {sender} {incoming_socket.getpeername()}')
    broadcast(f'"{sender}" has left the server!')
    #clients[sender].close()
    r_list.remove(clients[sender])
    del clients[sender]

def help_client(socket, message):
    """Returns the list of all available commands"""
    sender = message['sender']
    
    logging.info(f'COMMAND {sender} \"/{message["command"]}\"')
    clients[sender].send(f'Available commands:'.encode('utf-8'))
    time.sleep(0.1) # Necessary for debugging because curses cannot receive rapid messages
    clients[sender].send(f'/who               | List of online users.'.encode('utf-8'))
    time.sleep(0.1)
    clients[sender].send(f'/pm <to> <message> | Whisper to a user.'.encode('utf-8'))
    time.sleep(0.1)
    clients[sender].send(f'/rename <new_name> | Change your username.'.encode('utf-8'))
    time.sleep(0.1)
    clients[sender].send(f'/leave             | Leave the server.'.encode('utf-8'))
    time.sleep(0.1)
    clients[sender].send(f'/help              | All commands.'.encode('utf-8'))

def receive_unknown_command(socket, message):
    """Informs the user when they send an invalid command"""
    sender = message['sender']
    data = message['data']

    logging.error(f'fCOMMAND {sender} \"/{message["data"]}\"')
    clients[sender].send(f'Invalid command "/{data}"! Type "/help" for more.'.encode('utf-8'))

def send_message():
    """Send message from the server"""
    while True:
        try:
            message = input('')
            if message[0] == '/':
                if message.startswith('/all'):
                    data = message[5:].split(' ', 0)[0]
                    
                    logging.info(f'MESSAGE SERVER "/all {data}"')
                    try:
                        broadcast(f'SERVER: {data}')
                        cprint('Message sent.','green')
                    except Exception as e:
                        cprint('Failed to send the message!','red')
                        print(e)
                        continue
                elif message.startswith('/pm'):
                    receiver = message[4:].split(' ', 1)[0]
                    data = message[4:].split(' ', 1)[1]
                    if 'SERVER' == receiver:
                    # If sender is the SERVER
                        logging.error(f'fCOMMAND SERVER \"/pm {receiver} {data}\"')
                        cprint('You can not pm yourself!', 'red')
                        continue
                    if receiver in clients:
                        logging.info(f'COMMAND SERVER \"/pm {receiver} {data}\"')
                        clients[receiver].send(f'From SERVER: {data}'.encode('utf-8'))
                        cprint('PM sent.', 'green')
                    else:
                        # If receiver does not exist
                        logging.error(f'fCOMMAND SERVER \"/pm {receiver} {data}\"')
                        cprint(f'User "{receiver}" not found!', 'red')
                elif message.startswith('/who'):
                    online_users = []
                    for online_user in clients:
                        online_users.append(online_user)
                    logging.info(f'COMMAND SERVER "/who"')
                    if online_users == []:
                        cprint(f'All users are offline!', 'magenta')
                    else:
                        cprint(f'All online users {online_users}', 'magenta')
                        cprint(f'Clients = {clients}', 'magenta')
                elif message.startswith('/stop'):
                    logging.info('COMMAND SERVER "/stop"')
                    broadcast('SERVER: Server shutting down in 3..2..1..')
                    cprint('Server shutting down in 3..2..1..', 'red')
                    try:
                        server_socket.close()
                        sys.exit(0)
                    except SystemExit:
                        os._exit(0)
                elif message.startswith('/help'):
                    logging.info(f'COMMAND SERVER "/help"')
                    cprint('Available commands:\n\
    /who               | List of online users.\n\
    /all <message>     | Message all users.\n\
    /pm <to> <message> | Whisper to a user.\n\
    /stop              | Stop the server.\n\
    /help              | All commands.\n\
        ', 'magenta')
                else:
                    # If an unkown command is sent:
                    logging.error(f'fCOMMAND SERVER "/{message}')
                    cprint(f'Unkown command "{message}"! Type "/help" for more.', 'red')
        except IndexError: # User input is blank
            cprint('Please type something!', 'red')
        except Exception: # EOFError or KeyboardInterrupt or ConnectionLost
            logging.error(f'cSHUTDOWN SERVER') # cSHUTDOWN for crash shut down
            broadcast('Server has unexpectedly shut down!')
            cprint('Server has unexpectedly shut down. Reason: Crashed', 'red')
            try:
                server_socket.close()
                sys.exit(0)
            except SystemExit:
                os._exit(0)

def handle_incoming_connections():
    server_socket.listen(16)  # max 16 connections
    while True: # Run as long as server.py is running
        r_sock, w_sock, e_sock = select.select(r_list, w_list, []) 
        for incoming_socket in r_sock:
            if incoming_socket == server_socket:
                # If server socket ready, then => 
                client_socket, client_address = server_socket.accept() 
                # accept new connection.
                user = receive_message(client_socket)

                # First message to receive is the username
                username = user['sender']
                if username in clients: 
                    # If same username is online:
                    client_socket.send('Username already exists!'.encode('utf-8'))
                    break
                else:
                    client_socket.send('Username accepted.'.encode('utf-8'))


                clients[username] = client_socket
                logging.info(f'JOIN {username} {client_address}')
                clients[username].send(f'Welcome to the server {username}!\n'.
                encode('utf-8'))
                time.sleep(1) # Bugfix for client receiving messages too fast
                clients[username].send(f'To see the list of commands: type "/help"\n'.encode('utf-8'))
                if user:
                # if a user with a username connets
                    r_list.append(client_socket)
                    cprint(f'Connection from {client_address} as {username} has been establised.', 'green')
                    broadcast(f'"{username}" has joined the server.') # Letting know everyone someone has joined
                
                elif user is False: 
                    # if user leaves (or send nothing)
                    cprint(f'Connection from {client_address} as {username} has been lost!', 'red')
                    logging.info(f'LEAVE {username}')
                    broadcast(f'{username} has left the server!')
                    continue
            else:
                message = receive_message(incoming_socket)
                if message:
                    # If received data from connected socket
                    cprint(f'Received {message} from {incoming_socket}.', 'white')

                    if 'command' in message:
                        if message['command'] == 'pm':
                            send_pm(message)
                        elif message['command'] == 'who':
                            who(message)
                        elif message['command'] == 'rename':
                            rename(message)
                        elif message['command'] == 'leave':
                            kick(message, incoming_socket)
                        elif message['command'] == 'help':
                            help_client(client_socket, message)
                        elif message['command'] == 'unknown':
                            receive_unknown_command(client_socket, message)
                    else:
                        # If not a command, broadcast the incoming message
                        broadcast_message(message)

                elif message is False:
                    # If EOF (ctrl + c OR from X) is received: 
                    # remove the client from clients{}.
                    for usern in clients:
                        if incoming_socket == clients[usern]:
                            cprint(f'Closed connection from {incoming_socket} aka "{usern}"! Reason: User crashed.', 'red')    
                            logging.info(f'cLEAVE {usern} {incoming_socket.getpeername()}') #cLEAVE is for crashing
                            broadcast(f'{usern} has suddenly left the server!')
                            r_list.remove(incoming_socket)
                            del clients[usern]  # Delete username + socket from clients{}
                            break


# Main
if __name__ == '__main__':
    colorama.init() # Bugfixing colours on Windows
    logging.basicConfig(filename='server.log', level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%H:%M:%S')
    current_date = strftime(strftime("%Y-%m-%d", gmtime())) # YYYY-MM-DD
    logging.info(f'============================={current_date}==============================')
    server_socket = create_socket()
    bind_socket(server_socket, SERVER_IP, SERVER_PORT)
    cprint('To see the list of commands: type "/help"\n')

    r_list = [server_socket]
    clients = {} # Storing clients in a dictionary as {username:socket}
    w_list = []

    send_thread = threading.Thread(target=send_message)
    send_thread.start()
    handle_incoming_connections()
