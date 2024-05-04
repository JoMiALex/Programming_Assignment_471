#python server side TCP
#
#@author John Michael Lott
#@author Mariah Salgado
#@author Tuan Nguyen
#@author Ibrahim Israr

import socket
import os

def get_ephemeral_port():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('localhost', 0))
    port = s.getsockname()[1]
    s.close()
    return port

def send_command(sock, command):
    sock.sendall(command.encode())
    response = sock.recv(1024).decode()
    return response

def receive_file(sock, filename):
    filesize = int(sock.recv(1024).decode())
    received_bytes = 0
    with open(filename, 'wb') as file:
        while received_bytes < filesize:
            data = sock.recv(1024)
            if not data:
                break
            file.write(data)
            received_bytes += len(data)
    print(f"Received {received_bytes} bytes for file {filename}")

def send_file(sock, filename):
    filesize = os.path.getsize(filename)
    sock.sendall(str(filesize).encode())
    with open(filename, 'rb') as file:
        data = file.read(1024)
        while data:
            sock.sendall(data)
            data = file.read(1024)

# client loop
def ftp_client():
    control_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 12345)
    control_socket.connect(server_address)
    data_port = get_ephemeral_port()
    control_socket.sendall(f'DATAPORT {data_port}'.encode())

    data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    data_socket.bind(('localhost', data_port))
    data_socket.listen(1)
    data_connection, _ = data_socket.accept()

    while True:
        command = input('ftp> ').strip()
        if command.startswith('get'):
            _, filename = command.split()
            response = send_command(control_socket, f'GET {filename}')
            if response == 'OK':
                receive_file(data_connection, filename)
            else:
                print(response)
        elif command.startswith('put'):
            _, filename = command.split()
            if os.path.exists(filename):
                response = send_command(control_socket, f'PUT {filename}')
                if response == 'OK':
                    send_file(data_connection, filename)
                else:
                    print(response)
            else:
                print(f"Error: {filename} does not exist.")
        elif command.startswith('ls'):
            response = send_command(control_socket, 'LS')
            print(response)
        elif command == 'quit':
            send_command(control_socket, 'QUIT')
            break
        else:
            print("Unknown command")

    control_socket.close()
    data_connection.close()

if __name__ == '__main__':
    ftp_client()
