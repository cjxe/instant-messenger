import socket
import threading

HEADER = 60 # 60 bytes
server_IP = '' # ipv4 10.249.212.98
server_port = 8091
server_address = (server_IP, server_port)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # INET for ipv4
print(f"Server socket is created.")
server_socket.bind(server_address)


def start_server(): # handle new connections and distribute where to go from here
    server_socket.listen()
    print(f"Listening on {server_IP, server_port}...")
    while True: # receive messages continuously
        client_socket, client_address = server_socket.accept() # waiting for new connection
        thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        thread.start()
        print(f"Active users: {threading.activeCount() - 1}") # start_server thread is always running so we don't want to count that as part of the connected clients/users
    

def handle_client(client_socket, client_address): # handles individual connection with the client and the server
    print(f"[SERVER] Connection from {client_address} has been establised.")
    client_username = client_socket.recv(HEADER).decode() ## handle error, same username kick
    if client_username == '':
        print(f"[SERVER] {client_address} has been kicked. Reason: Invalid username.")
        client_socket.close()
        exit()
    else:
        print(f"[SERVER] User {client_username} has joined the chat.") # to all
    
    connected = True
    while connected:        
        client_msg = client_socket.recv(HEADER).decode()

        if client_msg == '':
            continue

        if client_msg == "/disc": ## if client_msg == user_commands:
            print(f"[SERVER] User {client_username} has left the chat.") # to all
            connected = False

        #if client_msg == f"/pm {client_username}":
         #   print('test')            

        print(f"{client_username}: {client_msg}")

    client_socket.close()



print("Server is initialising...")
start_server()