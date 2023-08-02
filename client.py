import socket
import threading
import os
import base64

def receive_data(sock):
    while True:
        data = sock.recv(1024).decode("utf-8")
        print("\n")
        print(data)

def send_message(sock, recipient, content):
    message = f"{recipient}|message|{content}"
    sock.send(message.encode())

def send_file(sock, recipient, file_path, msg_type):
    file_name = os.path.basename(file_path)
    with open(file_path, "rb") as f:
        file_data = f.read()
    file_data_b64 = base64.b64encode(file_data).decode()
    message = f"{recipient}|{msg_type}|{file_name}?data={file_data_b64}"
    sock.send(message.encode())

def main():
    host = 'localhost'
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
            video_path = input("Enter the video file path: ")
            if os.path.exists(video_path):
                send_file(client_socket, recipient, video_path, "video")
            else:
                print("File not found!")

        elif choice == "4":
            client_socket.close()
            exit()

if __name__ == "__main__":
    main()
