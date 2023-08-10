import socket
import threading



def main():
    # host = 'localhost'
    host = '10.217.19.120'
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
            data = client_socket.recv(100000000)
            
            if not data:
                break

            file_data += data

            if file_data.count(b"||") < 2:
                continue

            recipient, rest_data = file_data.split(b"||", 1)
            recipient = recipient.decode()
            
            
            if len(recipient) > 0 and recipient[0] == "[" and recipient[-1] == "]" and "," in recipient:
                recipient = recipient[1:-1].split(",")
                recipient = [rcpnt.strip() for rcpnt in recipient]
            elif recipient == "all":
                recipient = list(clients.keys())
                recipient.remove(username)
            else:
                recipient = [recipient]

            
            

            msg_type = rest_data.split(b"||", 1)[0]
            content = rest_data.split(b"||", 2)[1]
            
            file_path = rest_data.split(b"||")[-1]
            
            

            if msg_type == b"message":
                content = content.strip().decode()
                msg_type = msg_type.decode()

                send_message(clients, username, recipient, content,msg_type,file_path)
            elif msg_type == b"image" or msg_type == b"video" or msg_type == b"file":
                content = content.decode()
                msg_type = msg_type.decode()
                send_file(clients, username, recipient, content, msg_type, file_path)
            
        except OSError:
            break

    file_data = b""


def send_message(clients,username,recipient,content,msg_type,file_path):
    for rcpnt in recipient:
        if rcpnt in clients.keys():
            if rcpnt == username:
                clients[rcpnt].send(f"{username}||{content}||{msg_type}||null".encode())
            else:
                clients[rcpnt].send(f"{username}||{content}||{msg_type}||null".encode())
        else:
            clients[rcpnt].send(f"{username}||{content}||{msg_type}".encode())
    


def send_file(clients, username, recipient, content, msg_type, file_path):
    for rcpnt in recipient:
        if rcpnt in clients.keys():
            if rcpnt == username:
                clients[rcpnt].send(f"{username}||{content}||{msg_type}||{file_path}".encode())
            else:
                clients[rcpnt].send(f"{username}||{content}||{msg_type}||{file_path}".encode())
        else:
            clients[username].send(f"Recipient '{rcpnt}' not found.".encode())
    
 
if __name__ == "__main__":
    main()