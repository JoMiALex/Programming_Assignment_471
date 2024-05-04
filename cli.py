#python server side TCP
#
#@author John Michael Lott
#@author Mariah Salgado
#@author Tuan Nguyen
#@author Ibrahim Israr

import socket
import sys
from ephemeral import get_ephemeral_port

def send_command(sock, command):
    sock.sendall(command.encode())
    response = sock.recv(1024).decode()
    print("Server response:", response)

def receive_data(sock, filename, filesize):
    received_bytes = 0
    with open(filename, 'wb') as file:
        while received_bytes < filesize:
            data = sock.recv(1024)
            if not data:
                break
            file.write(data)
            received_bytes += len(data)
    print(f"Received {received_bytes} bytes for file {filename}")

# Control Channel
control_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 12345)
control_socket.connect(server_address)

# Setup Data Channel
data_port = get_ephemeral_port()
control_socket.sendall(str(data_port).encode())

data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
data_socket.bind(('localhost', data_port))
data_socket.listen(1)
data_connection, _ = data_socket.accept()

# Send command to server
send_command(control_socket, "get sample.txt")

# Receive file data
filesize = int(control_socket.recv(1024).decode())
receive_data(data_connection, "received_sample.txt", filesize)

# Close connections
control_socket.close()
data_connection.close()