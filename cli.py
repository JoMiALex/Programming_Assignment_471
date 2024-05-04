import socket
import sys
import random

def generate_ephemeral_port():
    # Generate a random port number in the ephemeral port range (49152–65535)
    return random.randint(49152, 65535)

def receive_all(sock, num_bytes):
    recv_buff = b""
    while len(recv_buff) < num_bytes:
        tmp_buff = sock.recv(num_bytes - len(recv_buff))
        if not tmp_buff:
            return None
        recv_buff += tmp_buff
    return recv_buff

def send_file(sock, file_name):
    # Open the file in binary mode
    with open(file_name, "rb") as file_obj:
        # Read file data
        file_data = file_obj.read()
        # Calculate file size
        file_size = len(file_data)
        # Convert file size to fixed-length string
        file_size_str = str(file_size).zfill(10)
        # Send file size to server
        sock.sendall(file_size_str.encode())
        # Send file data to server
        sock.sendall(file_data)

# Command prompt
def ftp_prompt():
    print("ftp>", end=" ", flush=True)

# Command line argument check
if len(sys.argv) != 3:
    print("USAGE: python client.py <SERVER IP> <SERVER PORT>")
    sys.exit(1)

# Server IP and port
server_ip = sys.argv[1]
server_port = int(sys.argv[2])

# Create command channel socket
command_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
command_sock.connect((server_ip, server_port))

print("Connected to server.")

# Display initial prompt
ftp_prompt()

# Main loop to send commands to the server
while True:
    # Get user input
    user_input = input().strip()
    # Send command to server
    command_sock.sendall(user_input.encode())
    # Receive acknowledgment from server
    ack = command_sock.recv(1024).decode()
    if ack != "Recieved":
        print("Error: Acknowledgment not received from server.")
        break
    # Check if user wants to quit
    if user_input.lower() == "quit":
        print("Exiting...")
        break
    # Handle put command (upload file)
    elif user_input.startswith("put"):
        file_name = user_input.split()[1]
        # Create data channel socket
        data_port = generate_ephemeral_port()
        data_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        data_sock.bind(('localhost', data_port))
        data_sock.listen(1)
        # Send data channel port to server
        command_sock.sendall(str(data_port).encode())
        # Accept connection from server on data channel
        data_conn, _ = data_sock.accept()
        # Send file to server
        send_file(data_conn, file_name)
        # Close data channel connection
        data_conn.close()
        data_sock.close()
    # Display prompt for next command
    ftp_prompt()

# Close command channel connection
command_sock.close()
