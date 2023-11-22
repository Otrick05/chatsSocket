import socket
import threading
import os
# Lista para almacenar las conexiones de clientes
clients = []

# Lista para almacenar el historial de chat
chat_history = []

# Ruta del archivo para guardar el historial del chat
chat_history_file=""

controlsala=""
controlsalagb=""

# Función para manejar las conexiones de los clientes
def handle_client(client_socket, client_address):
    print(f"[NUEVA CONEXIÓN] {client_address} se ha conectado")

    # Solicitar el nickname al cliente
    #client_socket.send("Ingresa tu nickname: ".encode("utf-8"))
    nickname = client_socket.recv(1024).decode("utf-8")

    # Si la sala de chat está vacía, enviar un mensaje al cliente para crear la sala
    if len(clients) == 0:
        
        client_socket.send(f"Sala de chat creada. #{controlsalagb} ¡Bienvenido!".encode("utf-8"))

    else:
        # Mostrar historial del chat al cliente
        for message in chat_history:
         
            espacio="   "
            client_socket.send(espacio.encode("utf-8"))
            client_socket.send(message.encode("utf-8"))

    # Notificar a todos los clientes la entrada de un nuevo usuario
    for c in clients:
        c.send(f"{nickname} se ha unido al chat".encode("utf-8"))

    # Agregar al cliente a la lista de clientes
    clients.append(client_socket)

    # Escuchar mensajes del cliente y difundirlos a todos los clientes
    while True:
        try:
            message = client_socket.recv(1024).decode("utf-8")
            if message:
                chat_history.append(f"{nickname}: {message}")
                for c in clients:
                    if c != client_socket:
                        c.send(f"{nickname}: {message}".encode("utf-8"))
                print(
                    f"{nickname}: {message}"
                )  # Mostrar el mensaje y el remitente en el servidor
        except Exception as e:
            # Manejar desconexiones de clientes
            print(f"[DESCONEXIÓN] {client_address} se ha desconectado ({e})")
            clients.remove(client_socket)
            for c in clients:
                c.send(f"{nickname} se ha desconectado del chat".encode("utf-8"))
            print(
                f"{nickname} se ha desconectado del chat"
            )  # Mostrar en el servidor cuando un usuario se desconecta
            save_chat_history()  # Guardar el historial del chat al desconectarse un cliente
            break


# Función para guardar el historial del chat en un archivo TXT
def save_chat_history():
    with open(chat_history_file, "w", encoding="utf-8") as file:
        for message in chat_history:
            file.write(message + "\n")


# Función para iniciar el servidor
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
    server.bind(("192.168.0.2", 12345))  # Puedes cambiar el puerto según tus necesidades
    server.listen(5)
    print("El servidor está escuchando en el puerto 12345...")

    while True:
        client_socket, addr = server.accept()
        client_handler = threading.Thread(
            target=handle_client, args=(client_socket, addr)
        )
        client_handler.start()


if __name__ == "__main__":
    if os.path.exists("controlsala.txt"):
             controlsala=open("controlsala.txt","r")
             controlsalagb=controlsala.read()
             #temporal=int(controlsalagb)
             temporal=(f"{controlsalagb}")
             controlsala.close()
             controlsala= open("controlsala.txt","w")
             temporal2=int(temporal,10)
             temporal2+=1
             controlsalagb=temporal2
             controlsala.write(str(temporal2))
             controlsala.close()
             
    else:
        controlsala= open("controlsala.txt","w")
        controlsala.write("1")
        controlsalagb=1
        controlsala.close()

chat_history_file = (f"chat_history{controlsalagb}.txt")
start_server_thread = threading.Thread(target=start_server)
start_server_thread.start()

try:
    start_server_thread.join()
except KeyboardInterrupt:
        # Guardar el historial del chat al cerrar el servidor
    save_chat_history()
    
def controlchat():
    controlsala=open("controlsala.txt","r")
    controlsalagb=controlsala.read()
    #temporal=int(controlsalagb)
    temporal=(f"{controlsalagb}")
    controlsala.close()
    controlsala= open("controlsala.txt","w")
    temporal2=int(temporal,10)
    temporal2+=1
    controlsalagb=temporal2
    controlsala.write(str(temporal2))
    controlsala.close()        