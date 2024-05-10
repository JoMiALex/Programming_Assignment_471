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
    #return response

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
        #while len(file_size_str) < 10:
            #file_size_str = "0" + file_size_str
        file_size_str = f"{file_size:010d}"  
        sock.sendall(file_size_str.encode())  
        sock.sendall(data)
    print(f"Sent {filename} with {file_size} bytes")

def list_files(sock):
    fileList = sock.recv(1024).decode()
    print(fileList)

def ftp_client_loop(sock):
    # Handles FTP client loop
    print("FTP client is ready. Type your commands.")
    while True:

        command = input("ftp> ").strip()

        if command.startswith("get "):
            _, filename = command.split(maxsplit=1)
            send_command(sock, command)
            find = sock.recv(1024).decode()
            print(find)
            if find.split()[1] != "not":
                receive_file(sock, filename)
        elif command.startswith("put "):
            _, filename = command.split(maxsplit=1)
            if os.path.exists(filename):
                send_command(sock, command)
                send_file(sock, filename)
            else:
                print(f"Error: File {filename} does not exist.")
        elif command == "ls":
            send_command(sock, command)
            list_files(sock)
        elif command == "quit":
            send_command(sock, command)
            break
        else:
            print("Unknown command")


if len(sys.argv) != 2:
    print("USAGE: python client.py <SERVER PORT>")
    sys.exit(1)

# The port on which to listen
port = int(sys.argv[1])

print("Starting FTP client...")
control_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', port)
try:
    control_socket.connect(server_address)
    print("Connected to the server.")
except socket.error as e:
    print(f"Connection failed: {e}")
    sys.exit(1)

ftp_client_loop(control_socket)


print("Closing connections...")
control_socket.close()