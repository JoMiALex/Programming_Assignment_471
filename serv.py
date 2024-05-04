#python server side TCP
#
#@author John Michael Lott
#@author Mariah Salgado
#@author Tuan Nguyen
#@author Ibrahim Israr

import socket
import os
import sys

def receive_all(sock, num_bytes):
  sock.sendall("Recieved".encode())
  # Buffer to store received data
  recv_buff = ""
  tmp_buff = ""
    
  # Keep receiving until all data is received
  while len(recv_buff) < num_bytes:
    # Attempt to receive bytes
    tmp_buff =  sock.recv(num_bytes)
        
    # Break if the other side has closed the socket
    if not tmp_buff:
      break
        
    # Add the received bytes to the buffer
    recv_buff += tmp_buff.decode()
    
    return recv_buff

def handle_get_command(client_socket, command):
    client_socket.sendall("Recieved".encode())
    # Extract the filename from the command
    file_name = command[4:]
    try:
        # Open the file in binary mode
        with open(file_name, "rb") as file_obj:
            file_data = file_obj.read()
            file_size_str = str(len(file_data))
            
            # Prepend 0's to the size string until it is 10 bytes long
            while len(file_size_str) < 10:
                file_size_str = "0" + file_size_str
            
            # Prepend the size of the data to the file data
            file_data = file_size_str.encode() + file_data
            
            # Send the data to the client
            num_sent = 0
            while len(file_data) > num_sent:
                num_sent += client_socket.send(file_data[num_sent:])
            print(f"Sent {num_sent} bytes for file {file_name}")
            print("Get command success")
    except FileNotFoundError:
        client_socket.send("File not found".encode())

def handle_ls_command(client_socket):
    client_socket.sendall("Recieved".encode())
    try:
        # Get the list of files in the current directory
        files = os.listdir('.')
        files_list = "\n".join(files)
        
        # Send the list of files to the client
        client_socket.sendall(files_list.encode())
        print('List command success')
    except FileNotFoundError:
        client_socket.send("Directory not found".encode())

def handle_put_command(client_socket, command):
    # Send acknowledgment to start data transfer
    client_socket.sendall("Recieved".encode())

    # Receive the file size from the client
    file_size = int(client_socket.recv(1024).decode())

    # Receive the file data
    file_data = receive_all(client_socket, file_size)
    
    # Extract the filename from the command
    file_name = command.split()[-1]
    
    # Write the received data to a new file
    with open(file_name, "wb") as file_out:
        file_out.write(file_data)
    print(f"Received {len(file_data)} bytes for file {file_name}")
    print("Put command success")

command_handlers = {
  "get": handle_get_command,
  "ls": handle_ls_command,
  "put": handle_put_command,
}

# Command line argument check
if len(sys.argv) != 2:
    print("USAGE: python server.py <SERVER PORT>")
    sys.exit(1)

# The port on which to listen
port = int(sys.argv[1])

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)         
print ("Socket successfully created")
 
#port = 12345               

s.bind(('', port))         
print ("socket binded to %s" %(port)) 

s.listen(1)     
print ("socket is listening")            

while True: 
 
  c, addr = s.accept()     
  print ('Got connection from', addr )

  while True:
    port = s.recv(1024).decode()               

    dataSock = socket.socket()

    dataSock.connect(('localhost', port))
    # Receive the command from the client
    command = s.recv(1024).decode()
    
    # Handle the command using the command handlers dictionary
    handler = command_handlers.get(command.split()[0])
    if handler:
      handler(dataSock, command)
      continue
    else:
      # Exit the loop if the client disconnects
      print(f"Client: {addr} disconnected")
      dataSock.close()
      break
  break

c.close()