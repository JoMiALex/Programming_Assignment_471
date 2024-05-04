#python server side TCP
#
#@author John Michael Lott
#@author Mariah Salgado
#@author Tuan Nguyen
#@author Ibrahim Israr

import socket
import sys
import os

def send_command(sock, command):
    
    sock.sendall(command.encode())
    response = sock.recv(1024).decode()
    print("Server response:", response)
    return response

def receive_file(sock, filename):
    # Receives a file from the server
    file_size_str = sock.recv(10).decode()
    file_size = int(file_size_str.strip())
    received_bytes = 0
    with open(filename, 'wb') as file:
        while received_bytes < file_size:
            data = sock.recv(1024)
            if not data:
                break
            file.write(data)
            received_bytes += len(data)
    print(f"Received {filename} with {received_bytes} bytes")

def send_file(sock, filename):
    # Send file to the server
    with open(filename, 'rb') as file:
        data = file.read()
        file_size = len(data)
        file_size_str = f"{file_size:010d}"  
        sock.sendall(file_size_str.encode())  
        sock.sendall(data)  
    print(f"Sent {filename} with {file_size} bytes")

def ftp_client_loop(sock):
    # Handles FTP client loop
    print("FTP client is ready. Type your commands.")
    while True:

        dataSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)         
        print ("Data socket successfully created")
        
        dataSock.bind(('localhost', 45123))         
        print ("Data socket binded to port:", dataSock.getsockname()[1])

        dataSock.listen(1)     
        print ("Data socket is listening")

        command = input("ftp> ").strip()

        if command.startswith("get "):
            _, filename = command.split(maxsplit=1)
            send_command(dataSock, command)
            receive_file(dataSock, filename)
        elif command.startswith("put "):
            _, filename = command.split(maxsplit=1)
            if os.path.exists(filename):
                send_command(dataSock, command)
                send_file(dataSock, filename)
            else:
                print(f"Error: File {filename} does not exist.")
        elif command == "ls":
            send_command(dataSock, command)
        elif command == "quit":
            send_command(dataSock, command)
            break
        else:
            print("Unknown command")
        dataSock.close()


print("Starting FTP client...")
control_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 45321)
try:
    control_socket.connect(server_address)
    print("Connected to the server.")
except socket.error as e:
    print(f"Connection failed: {e}")
    sys.exit(1)

ftp_client_loop(control_socket)


print("Closing connections...")
control_socket.close()