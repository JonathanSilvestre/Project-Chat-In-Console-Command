import socket   
import threading

# Solicitar al usuario que ingrese su nombre de usuario
username = input("Nombre de Usuario: ")

# Definir el host y el puerto al que el cliente se conectará
host = 'localhost' #Si se desea hacer desde varias computadoras aqui deberemos ingresar la direccion IP de la computadora que actuara como server.
port = 55555    #Si se desea hacer desde varias computadoras aqui deberemos ingresar el puerto de la computadora que actuara como server.

# Crear un objeto de socket TCP
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conectar el cliente al servidor
client.connect((host, port))

# Función para recibir mensajes del servidor
def receive_messages():

    while True:

        try:
            # Recibir mensajes del servidor
            message = client.recv(1024).decode('utf-8')

            # Si el servidor solicita el nombre de usuario, enviarlo
            if message == "@username":

                client.send(username.encode("utf-8"))

            else:
                # Imprimir el mensaje recibido
                print(message)

        except:
            # En caso de error, imprimir un mensaje y cerrar la conexión
            print("An error Ocurred")
            client.close
            break

# Función para escribir mensajes y enviarlos al servidor
def write_messages():

    while True:
        # Solicitar al usuario que ingrese un mensaje
        message = f"{username}: {input('')}"
        # Enviar el mensaje al servidor
        client.send(message.encode('utf-8'))

# Crear un hilo para recibir mensajes
receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

# Crear un hilo para escribir mensajes
write_thread = threading.Thread(target=write_messages)
write_thread.start()