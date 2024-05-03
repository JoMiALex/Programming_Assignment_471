#python client side TCP
#
#@author John Michael Lott
#@author Mariah Salgado
#@author Tuan Nguyen
#@author Ibrahim Israr

import socket

def send_command(sock, command):
    sock.sendall(command.encode())
    response = sock.recv(1024).decode()
    print("Server response:", response)

s = socket.socket()         

port = 12345               

s.connect(('127.0.0.1', port))

dSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
dSock.bind()

send_command(s, "get README.txt")

print (s.recv(1024).decode())

s.close()