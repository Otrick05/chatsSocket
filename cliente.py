import socket
import threading


def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode("utf-8")
            print(message)
        except Exception as e:
            print(f"Error: {e}")
            break


def start_client():
    global client
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(
        ("192.168.74.248", 12345)
    )  # Ingresa la IP del servidor y el puerto correspondiente

    nickname = input("Ingresa tu nickname: ")
    client.send(nickname.encode("utf-8"))

    receive_thread = threading.Thread(target=receive_messages, args=(client,))
    receive_thread.start()

    while True:
    
        message = input(f"{nickname} :")
        client.send(message.encode("utf-8"))

if __name__ == "__main__":
    start_client()



