import socket
import threading
import os
import base64



def receive_data(sock):
    buffer = b""  # Buffer to accumulate received data

    while True:
        try:
            data = sock.recv(100000000)
            
            # exit()
            if not data:
                break 

            buffer += data

            buffer = buffer.split(b"||")

            
            sender = buffer[0].decode()
            
            msg_type = buffer[2].decode()
            
            if msg_type == "message":
                content = buffer[1].decode()
                print(f"\n{sender}: {content}")
            elif msg_type == "image":
                file_path = buffer[3].decode()
                file_name = os.path.basename(file_path)
                content = buffer[1]
                # print(content)
                
                file=generateFile(file_name, content)
                print(f"\n{sender}: {file}")
                
                
                # print(f"\n{sender}: {content}")

                

        except OSError:
            break
        buffer = b""

def generateFile(file_name, file_data):
    # Convert file_data to bytes if it's a string
    if isinstance(file_data, str):
        file_data = file_data.encode()
    
    with open(file_name, 'wb') as destination_file:
        destination_file.write(file_data)
    return file_name


def main():

    host = '192.168.1.27'
    port = 12345
    
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    username = input("Enter your username: ")
    client_socket.send(username.encode())

    receive_thread = threading.Thread(target=receive_data, args=(client_socket,))
    receive_thread.start()

    while True:
        print("\nMenu:")
        print("1. Send Message")
        print("2. Send Image")
        print("3. Send Video")
        print("4. Exit")

        choice = input("Your choice: ")

        if choice == "1":
            recipient = input("Enter recipient's username ('all',[username1,username2] for all users): ")
            message = input("Enter your message: ")
            send_message(client_socket, recipient, message)

        elif choice == "2":
            recipient = input("Enter recipient's username ('all',[username1,username2] for all users): ")
            img_path = input("Enter the image file path: ")
            if os.path.exists(img_path):
                send_file(client_socket, recipient, img_path, "image")
            else:
                print("File not found!")

        elif choice == "3":
            recipient = input("Enter recipient's username ('all',[username1,username2] for all users): ")
            vid_path = input("Enter the video file path: ")
            if os.path.exists(vid_path):
                send_file(client_socket, recipient, vid_path, "video")
            else:
                print("File not found!")

        elif choice == "4":
            client_socket.close()
            break

        else:
            print("Invalid choice!")

def send_message(sock, recipient, message):
    message = f"{recipient}|message|{message}|null"
    sock.send(message.encode())

# def send_file(sock, recipient, file_path, msg_type):
#     message = f"{recipient}|{msg_type}|{file_path}"
#     sock.send(message.encode())

def send_file(sock, recipient, file_path, msg_type):
     with open(file_path, 'rb') as file:
        image_data = file.read()

     print(file_path)
     message = f"{recipient}|{msg_type}|{image_data}|{file_path}"
     print(message)
     sock.send(message.encode())


if __name__ == "__main__":
    main()

    
