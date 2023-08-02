import socket
import threading
import base64
import os


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



def handle_client(client_socket, client_address, clients):
    username = client_socket.recv(1024).decode()
    clients[username] = client_socket
    print(f"[INFO] {username} connected.")
    

    while True:
        try:
            
            data = client_socket.recv(1024).decode()
            recipient = data.split("|")[0]
            # if recipient start [ and end with ] then it is a list
            if recipient[0] == "[" and recipient[-1] == "]":
                recipient = recipient[1:-1].split(",")
                recipient = [r.strip() for r in recipient]
            
            elif recipient == "all":
                recipient = list(clients.keys())
                recipient.remove(username)

            # jika recipient bukan list, maka jadikan list
            recipient = recipient if isinstance(recipient, list) else [recipient]


            

            
            msg_type = data.split("|")[1]

            if msg_type == "message":
                content = data.split("|")[2]
                send_message(client_socket, username, recipient, content)
            elif msg_type == "image" or msg_type == "video":
                content = data.split("|")[2]
                send_file(client_socket, username, recipient, content, msg_type)
            else:
                print("Invalid message type!")


            print(recipient,msg_type,content)

            

            
            
        except OSError:
            break


def send_message(client_socket,username,recipient,content):
    for recipient in recipient:
        if recipient in username:
            client_socket.send(f"[{username}] sent a message: {content}".encode())
        else:
            client_socket.send(f"Recipient '{recipient}' not found.".encode())

def send_file(client_socket,username,recipient,content,msg_type):
     # content is path to file
    # content = "C:\\Users\\ASUS\\Desktop\\test.png"

    # check if file exists and upload to asset folder
    if os.path.isfile(content):
        file_name = os.path.basename(content)
        # if ASSET folder does not exist, create one
        os.makedirs('ASSET', exist_ok=True)
        # upload file to ASSET folder
        with open(content, 'rb') as file:  # Open the file in binary mode to read its content as bytes
            file_content = file.read()
        with open(os.path.join('ASSET', file_name), 'wb') as destination_file:
            destination_file.write(file_content)

        # send file to recipient
        for rcpnt in recipient:
            if rcpnt == username:  # Check if the recipient is the same as the sender
                client_socket.send(f"[{username}] sent a {msg_type}: {file_name}".encode())
            else:
                client_socket.send(f"Recipient '{rcpnt}' not found.".encode())

    else:
        client_socket.send(f"File '{content}' not found.".encode())
    # if msg_type == "image":


    




        
        

        

    # elif msg_type == "video":


        



    

if __name__ == "__main__":
    main()