import socket
import threading
import os
import struct

SERVER_HOST = 'localhost'
SERVER_PORT = 12345
BUFFER_SIZE = 4096


def send_message(client_socket, message):
    client_socket.send(message.encode('utf-8'))

def send_file(client_socket, file_name, file_type):
    file_path = os.path.join(os.path.dirname(__file__), file_name)
    try:
        with open(file_path, 'rb') as file:
            file_data = file.read()
    except FileNotFoundError:
        print(f"File '{file_name}' not found.")
        return

    file_size = len(file_data)

    message = f"UPLOAD:{file_type}:{file_name}"
    client_socket.send(message.encode('utf-8'))

    # Send the file size as a 4-byte integer
    client_socket.send(struct.pack('!I', file_size))

    # Send the file data in chunks
    offset = 0
    while offset < file_size:
        chunk = file_data[offset:offset+BUFFER_SIZE]
        client_socket.send(chunk)
        offset += len(chunk)

    print(f"File '{file_name}' sent successfully.")

def menu():
    print("Select an option:")
    print("1. Send Message")
    print("2. Send Image")
    print("3. Send Video")
    option = input("Enter option number: ")
    return option

def client_thread():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_HOST, SERVER_PORT))

    username = input("Enter your username: ")
    client_socket.send(username.encode('utf-8'))

    while True:
        option = menu()

        if option == '1':
            recipient = input("Enter recipient username (ALL for broadcast): ")
            message = input("Enter your message: ")
            send_message(client_socket, f"MESSAGE:{recipient}:{message}")
        elif option == '2':
            recipient = input("Enter recipient username (ALL for broadcast): ")
            file_name = input("Enter image file name: ")
            send_file(client_socket, file_name, "IMAGE")
        elif option == '3':
            recipient = input("Enter recipient username (ALL for broadcast): ")
            file_name = input("Enter video file name: ")
            send_file(client_socket, file_name, "VIDEO")
        else:
            print("Invalid option.")

if __name__ == "__main__":
    client_thread()
