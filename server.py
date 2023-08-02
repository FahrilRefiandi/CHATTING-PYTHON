import socket
import threading



def handle_client(client_socket, client_address, clients):
    username = client_socket.recv(1024).decode()
    clients[username] = client_socket

    print(f"[INFO] {username} connected from {client_address}")

    while True:
        data = client_socket.recv(1024)
        if not data:
            break

        message = data.decode("utf-8")
        recipient, msg_type, content = message.split("|")
        
        if recipient.startswith("[") and recipient.endswith("]"):
            recipient = recipient[1:-1].split(",")
            recipient = [name.strip() for name in recipient]
        
        else:
            if recipient == "all":
                recipient = list(clients.keys())
                recipient.remove(username)

        
        


        print("Recipient:", recipient)
        print("Message Type:", msg_type)
        print("Content:", content)
        

        if msg_type == "message":
            print(f"[{username} -> {recipient}]: {content}")
            # if recipient is array
            if isinstance(recipient, list):
                for recipient in recipient:
                    if recipient in clients:
                        recipient_socket = clients[recipient]
                        recipient_socket.send(f"[{username}]: {content}".encode())
                    else:
                        client_socket.send(f"Recipient '{recipient}' not found.".encode())
            # if recipient is string
            else:
                # if recipient == all
                if recipient == "all":
                    for recipient in clients:
                        recipient_socket = clients[recipient]
                        recipient_socket.send(f"[{username}]: {content}".encode())
                # if recipient is a single user
                else:
                    if recipient in clients:
                        recipient_socket = clients[recipient]
                        recipient_socket.send(f"[{username}]: {content}".encode())
                    else:
                        client_socket.send(f"Recipient '{recipient}' not found.".encode())


        elif msg_type == "image":
            img_name, img_data = content.split("?data=")
            save_image(img_name, img_data)

            print(f"[{username} -> {recipient}]: {img_name} (Image)")
            if isinstance(recipient, list):
                for recipient in recipient:
                    if recipient in clients:
                        recipient_socket = clients[recipient]
                        recipient_socket.send(f"[{username}] sent an image: {img_name}".encode())
                    else:
                        client_socket.send(f"Recipient '{recipient}' not found.".encode())

            else:
                if recipient in clients:
                    recipient_socket = clients[recipient]
                    recipient_socket.send(f"[{username}] sent an image: {img_name}".encode())
                else:
                    client_socket.send(f"Recipient '{recipient}' not found.".encode())


        elif msg_type == "video":
            video_name, video_data = content.split("?data=")
            save_video(video_name, video_data)

            print(f"[{username} -> {recipient}]: {video_name} (Video)")
            if recipient in clients:
                recipient_socket = clients[recipient]
                recipient_socket.send(f"[{username}] sent a video: {video_name}".encode())
            else:
                client_socket.send(f"Recipient '{recipient}' not found.".encode())

    # exit();

    del clients[username]
    client_socket.close()
    print(f"[INFO] {username} disconnected.")

def save_image(img_name, img_data):
    with open(f"received_{img_name}", "wb") as f:
        f.write(img_data.encode())

def save_video(video_name, video_data):
    with open(f"received_{video_name}", "wb") as f:
        f.write(video_data.encode())

def main():
    host = 'localhost'
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

if __name__ == "__main__":
    main()