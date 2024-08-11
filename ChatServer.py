import socket   
import threading

# Configuración del servidor
host = 'localhost' #Si se desea hacer desde varias computadoras aqui deberemos ingresar la direccion IP de la computadora que actuara como server.
port = 55555 #Si se desea hacer desde varias computadoras aqui deberemos ingresar el puerto de la computadora que actuara como server.

# Crear socket del servidor
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Enlazar socket a dirección y puerto
server.bind((host, port))
# Escuchar conexiones entrantes
server.listen()
# Imprimir mensaje de que el servidor está activo
print(f"Server abierto en {host}:{port}")

# Listas para almacenar clientes y nombres de usuario
clients = []
usernames = []

# Función para enviar un mensaje a todos los clientes excepto al que lo envió
def broadcast(message, _client):

    for client in clients:

        if client != _client:

            client.send(message)

# Función para manejar los mensajes de un cliente
def handle_messages(client):

    while True:

        try:
            # Recibir mensaje del cliente
            message = client.recv(1024)
            # Transmitir el mensaje a todos los clientes
            broadcast(message, client)

        except:
            # Manejar la desconexión del cliente
            index = clients.index(client)
            username = usernames[index]
            # Notificar a los demás clientes que este cliente se ha desconectado
            broadcast(f"ChatBot: {username} se ha desconectado".encode('utf-8'), client)
            # Eliminar al cliente de la lista de clientes y cerrar su conexión
            clients.remove(client)
            usernames.remove(username)
            client.close()
            break

# Función para recibir conexiones de clientes
def receive_connections():

    while True:
        # Aceptar la conexión entrante del cliente
        client, address = server.accept()
        # Solicitar al cliente su nombre de usuario
        client.send("@username".encode("utf-8"))
        username = client.recv(1024).decode('utf-8')
        # Agregar al cliente y su nombre de usuario a las listas respectivas
        clients.append(client)
        usernames.append(username)
        # Imprimir mensaje de que un nuevo cliente se ha conectado
        print(f"{username} se ha conectado desde {str(address)}")
        # Enviar mensaje de bienvenida a todos los clientes
        message = f"ChatBot: {username} se unio al chat!".encode("utf-8")
        broadcast(message, client)
        # Enviar mensaje de confirmación de conexión al cliente
        client.send("Conectado al server".encode("utf-8"))
        # Iniciar un hilo para manejar los mensajes del cliente
        thread = threading.Thread(target=handle_messages, args=(client,))
        thread.start()

# Iniciar la función para recibir conexiones de clientes
receive_connections()