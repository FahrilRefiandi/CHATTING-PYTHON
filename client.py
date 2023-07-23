import socket
import threading
import os
from PIL import Image
import base64

def receive_data(sock):
    while True:
        data = sock.recv(1024).decode()
        print("\n")
        print(data)

def send_image(sock, recipient, img_path):
    img_name = os.path.basename(img_path)
    with open(img_path, "rb") as f:
        img_data = f.read()
    img_data_b64 = base64.b64encode(img_data).decode()
    message = f"{recipient}|image|{img_name}|{img_data_b64}"
    sock.send(message.encode())

def send_video(sock, recipient, video_path):
    video_name = os.path.basename(video_path)
    with open(video_path, "rb") as f:
        video_data = f.read()
    video_data_b64 = base64.b64encode(video_data).decode()
    message = f"{recipient}|video|{video_name}|{video_data_b64}"
    sock.send(message.encode())

def main():
    host = '192.168.1.10'
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
            recipient = input("Enter recipient's username ('all',[username1,username2]) :")
            message = input("Enter your message: ")
            client_socket.send(f"{recipient}|message|{message}".encode())

        elif choice == "2":
            recipient = input("Enter recipient's username: ")
            img_path = input("Enter the image file path: ")
            if os.path.exists(img_path):
                send_image(client_socket, recipient, img_path)
            else:
                print("File not found!")

        elif choice == "3":
            recipient = input("Enter recipient's username: ")
            video_path = input("Enter the video file path: ")
            if os.path.exists(video_path):
                send_video(client_socket, recipient, video_path)
            else:
                print("File not found!")

        elif choice == "4":
            client_socket.close()
            exit()

if __name__ == "__main__":
    main()
