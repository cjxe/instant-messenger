import socket
import sys

def set_username(username):
    if len(username) < HEADER:
        print(f"Username {username} created successfully.")
        client_socket.send(username.encode())
    else:
        print("ERROR: Username too long.")
        print("Client socket is terminating...")
        client_socket.close()

server_IP = ''              #argv[2]
server_port = 8091          #argv[3]
HEADER = 60
#server_address = (server_IP, server_port)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Client socket is created.")
client_socket.connect((socket.gethostname(), server_port))

## START OF trying to set a valid username ##
try:
    set_username(sys.argv[1])
except IndexError:
    print("ERROR: Username not set.")
    print("Client socket is terminating...")
    client_socket.close()
    exit()
## END OF trying to set a valid username ##


connected = True
while connected:
    print("You have conncted to the server.")
    client_msg = input("Send a message to the server: ")
    client_socket.send(client_msg.encode())

    if client_msg == "/disc": # disc for disconenct
        print(f"You have left the chat.")
        connected = False    

