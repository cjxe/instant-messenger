import socket

def start_server():
    
    server_IP = ''
    server_port = 8090

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(f"Server socket is created.")
    server_socket.bind((server_IP, server_port))
    
    server_socket.listen(5)
    print(f"Listening...")
    
    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address} has been establised.")
        client_socket.send(bytes("Welcome to the server!", "utf-8"))


if __name__ == "__main__": 
    start_server()