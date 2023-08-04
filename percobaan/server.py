import socket
import threading
import base64
import os
from io import BytesIO
from PIL import Image
import magic

def main():
    host = '192.168.1.84'
    port = 12345

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)

    print("[INFO] Server listening on port", port)

    clients = {}

    while True:
        client_socket, client_address = server.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address, clients))
        client_thread.start()

def handle_client(client_socket, client_address, clients):
    username = client_socket.recv(1024).decode()
    clients[username] = client_socket
    print(f"[INFO] {username} connected.")
    
    file_data = b""
    while True:
        try:
            data = client_socket.recv(1024)
            
            if not data:
                break

            file_data += data
            print(file_data)
            print(data)

            # Process only if the data contains at least two '|' characters
            if file_data.count(b"|") < 2:
                continue

            recipient, rest_data = file_data.split(b"|", 1)
            recipient = recipient.decode()

            if recipient[0] == "[" and recipient[-1] == "]":
                recipient = recipient[1:-1].split(",")
                recipient = [r.strip() for r in recipient]
            elif recipient == "all":
                recipient = list(clients.keys())
                recipient.remove(username)
            else:
                recipient = [recipient]

            # rest of your code ...

            msg_type, content = rest_data.split(b"|", 1)
            msg_type = msg_type.strip()

            if msg_type == b"message":
                content = content.strip().decode()
                send_message(clients, username, recipient, content)
            elif msg_type in (b"image", b"video"):
                # content = content.strip().decode()
                # print(content);
                # padding = b"=" * (4 - (len(content) % 4))
                # content = content + padding
                # content = base64.b64decode(content)
                send_file(clients, username, recipient, content, msg_type)
            else:
                print("Invalid message type!")

        except OSError:
            break

        # Clear the file data before the next iteration
        file_data = b""


def send_message(clients,username,recipient,content):
    # send message to recipient
    for rcpnt in recipient:
        if rcpnt in clients.keys():
            if rcpnt == username:
                clients[rcpnt].send(f"[{username}] {content}".encode())
            else:
                clients[rcpnt].send(f"[{username}] {content}".encode())
        else:
            clients[username].send(f"Recipient '{rcpnt}' not found.".encode())

        


def send_file(clients, username, recipient, content, msg_type):
    print(content)
 
if __name__ == "__main__":
    main()