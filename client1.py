import socket

"""
HEADER = 10
server_IP = '' # ipv4 10.249.212.98
server_port = 8090
server_address = (server_IP, server_port)
"""

def start_client():
    server_IP = ''
    server_port = 8090

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Client socket is created.")
    client_socket.connect((socket.gethostname(), server_port))
    print("Client has conncted to the server.")

    #server_msg = client_socket.recv(1024)
    #print(server_msg.decode())
    while True:

        
        client_msg = input("Send a message to the server: ")
        client_socket.send(client_msg.encode())

        #print("Client socket is terminating...")
        #client_socket.close()


if __name__ == "__main__": 
    start_client()