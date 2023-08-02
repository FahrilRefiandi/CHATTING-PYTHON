import socket
import threading
import os
import base64

# Dictionary to store connected clients and their usernames
connected_clients = {}

def broadcast_message(sender, message):
    for client, _ in connected_clients.items():
        if client != sender:
            client.send(message.encode())

def handle_client(client_socket, address):
    username = client_socket.recv(1024).decode("utf-8")
    connected_clients[client_socket] = username
    print(f"{username} connected from {address}.")

    while True:
        try:
            data = client_socket.recv(1024).decode("utf-8")
            if not data:
                break

            recipient, msg_type, payload = data.split("|", 2)

            if msg_type == "message":
                message = f"{connected_clients[client_socket]}: {payload}"
                if recipient == "all":
                    broadcast_message(client_socket, message)
                else:
                    for client, user in connected_clients.items():
                        if user == recipient:
                            client.send(message.encode())
                            break

            elif msg_type in ["image", "video"]:
                file_name, file_data_b64 = payload.split("?data=")
                file_data = base64.b64decode(file_data_b64)

                # save file and send path to recipient
                file_path = os.path.join("files", file_name)
                with open(file_path, "wb") as f:
                    f.write(file_data)

                message = f"{connected_clients[client_socket]}: {file_path}"
                if recipient == "all":
                    broadcast_message(client_socket, message)
                else:
                    for client, user in connected_clients.items():
                        if user == recipient:
                            client.send(message.encode())
                            break


                
                # print(f"Received {msg_type} from {connected_clients[client_socket]}")
                # print(f"File Name: {file_name}")
                # print(f"File Size: {len(file_data)} bytes")

        except Exception as e:
            print(f"Error while handling client {connected_clients[client_socket]}: {e}")
            break

    print(f"{connected_clients[client_socket]} disconnected.")
    del connected_clients[client_socket]
    client_socket.close()

def main():
    host = 'localhost'
    port = 12345

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print("Server is listening...")

    while True:
        client_socket, address = server_socket.accept()
        client_handler = threading.Thread(target=handle_client, args=(client_socket, address))
        client_handler.start()

if __name__ == "__main__":
    main()
