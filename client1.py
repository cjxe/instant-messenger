import socket

def start_client():
    server_IP = ''
    server_port = 8090

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Client socket is created.")
    client_socket.connect((socket.gethostname(), server_port))


    while True:
        message = client_socket.recv(1024)
        print(message.decode())
        
        print("Client socket is terminating...")
        client_socket.close()


if __name__ == "__main__": 
    start_client()