import socket
import threading
import os




def receive_data(sock):
    buffer = b""  # Buffer to accumulate received data

    try:
        while True:
            data = sock.recv(100000000)
            if not data:  # Check if no more data is being received
                break
            
            buffer += data  # Accumulate received data

            process_message(buffer)
            
    except Exception as e:
        print("Error:", e)
    buffer = b""

def process_message(message):
    
    parts = message.split(b"||")
    
    sender = parts[0].decode()
    msg_type = parts[2].decode()
    content = parts[1]

    if msg_type == "message":
        print(f"\n{sender}: {content.decode()}")
    elif msg_type == "image" or msg_type == "video" or msg_type == "file":
        file_path = parts[3].decode()
        file_name = os.path.basename(file_path)
        content = content.decode()
        
        generateFile(file_name, content)
        print(f"\n{sender}: {file_name}")

def generateFile(file_name, file_data):
    file_name = file_name[:-1]
    if isinstance(file_data, str):
        file_data = file_data.encode()
    
    
    os.makedirs('ASSET', exist_ok=True)
    
    
    
    path=os.path.join('ASSET', file_name)
    print(path)
    

    with open(path, 'wb') as destination_file:
        destination_file.write(file_data)

    


    
    return path

def main():

    # host = 'localhost'
    host = '10.217.19.120'
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
        print("4. Send File")
        print("5. Exit")

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
            recipient = input("Enter recipient's username ('all',[username1,username2] for all users): ")
            vidPath = input("Enter the video file path: ")
            if os.path.exists(vidPath):
                send_file(client_socket, recipient, vidPath, "file")
            else:
                print("File not found!")

        elif choice == "5":
            client_socket.close()
            break

        else:
            print("Invalid choice!")

def send_message(sock, recipient, message):
    message = f"{recipient}||message||{message}||null"
    sock.send(message.encode())

def send_file(sock, recipient, file_path, msg_type):
    with open(file_path, 'rb') as file:
        image_data = file.read()
     

    message = f"{recipient}||{msg_type}||{image_data}||{file_path}"
    sock.send(message.encode())


if __name__ == "__main__":
    main()

    
