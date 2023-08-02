import socket
import threading
import os
import struct

SERVER_HOST = 'localhost'
SERVER_PORT = 12345
BUFFER_SIZE = 4096

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen(5)

clients = {}

def handle_client(client_socket, client_address):
    print(f"Accepted connection from {client_address}")
    
    client_socket.send("Enter your username: ".encode('utf-8'))
    username = client_socket.recv(BUFFER_SIZE).decode('utf-8')
    clients[username] = client_socket

    while True:
        data = client_socket.recv(BUFFER_SIZE)
        if not data:
            break

        parts = data.split(b':')
        if parts[0] == b'MESSAGE':
            recipient = parts[1].decode('utf-8')
            actual_message = b':'.join(parts[2:])
            
            if recipient == 'ALL':
                for client in clients.values():
                    client.send(data)
                client_socket.send(f"Message sent to {recipient}".encode('utf-8'))  # Send confirmation to sender
            elif recipient in clients:
                client = clients[recipient]
                client.send(data)
                client_socket.send(f"Message sent to {recipient}".encode('utf-8'))  # Send confirmation to sender
        elif parts[0] == b'UPLOAD':
            _, file_type, file_name = parts
            file_data = b''

            # Receive the file size as a 4-byte integer
            file_size = struct.unpack('!I', client_socket.recv(4))[0]

            while file_size > 0:
                chunk = client_socket.recv(min(BUFFER_SIZE, file_size))
                if not chunk:
                    break
                file_data += chunk
                file_size -= len(chunk)

            file_path = os.path.join('ASSET', file_name.decode('utf-8'))
            with open(file_path, 'wb') as file:
                file.write(file_data)

            print(f"Uploaded {file_type.decode('utf-8')} to {file_path}")

    del clients[username]
    client_socket.close()
    print(f"Connection from {client_address} closed")
    print(f"Accepted connection from {client_socket}{client_address}")
    
    client_socket.send("Enter your username: ".encode('utf-8'))
    username = client_socket.recv(BUFFER_SIZE).decode('utf-8')
    clients[username] = client_socket

    while True:
        data = client_socket.recv(BUFFER_SIZE)
        if not data:
            break

        parts = data.split(b':')
        if parts[0] == b'MESSAGE':
            recipient = parts[1].decode('utf-8')
            actual_message = b':'.join(parts[2:])
            
            if recipient == 'ALL':
                for client in clients.values():
                    client.send(data)
                client_socket.send(f"Message sent to {recipient}".encode('utf-8'))  # Send confirmation to sender
            elif recipient in clients:
                client = clients[recipient]
                client.send(data)
                client_socket.send(f"Message sent to {recipient}".encode('utf-8'))  # Send confirmation to sender
        elif parts[0] == b'UPLOAD':
            _, file_type, file_name = parts
            file_data = b''

            while True:
                chunk = client_socket.recv(BUFFER_SIZE)
                if not chunk:
                    break
                file_data += chunk

            file_path = os.path.join('ASSET', file_name.decode('utf-8'))
            with open(file_path, 'wb') as file:
                file.write(file_data)

            print(f"Uploaded {file_type.decode('utf-8')} to {file_path}")

    del clients[username]
    client_socket.close()
    print(f"Connection from {client_address} closed")

if __name__ == "__main__":
    os.makedirs('ASSET', exist_ok=True)
    
    print("Server is listening...")
    while True:
        client_socket, client_address = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()
