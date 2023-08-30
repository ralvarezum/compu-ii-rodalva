import socket
import multiprocessing as mp
import sys
import os


def connected_client(client):
    #Se inicia el proceso hijo
    print(f"Iniciando proceso hijo...{os.getpid()}")

    child_conn, child_addr = client

    while True:
        #Recibe datos del client
        data = child_conn.recv(1024)
        #Si el client envia exit, se cierra la conexion
        if data == b"exit":
            print(f"Conexion cerrada por {child_addr}")
            exit_c = "Cerrado."
            child_conn.send(exit_c.encode("ASCII"))
            break
        print(f"Datos recibidos desde {child_addr}: {data.decode('UTF-8')}")

        #Respuesta para el client
        response = f"Mensaje recibido. \r\n {data.decode('UTF-8').upper()}"
        child_conn.send(response.encode("ASCII"))

#Funcion main
def main():
    #Crea el socket del servidor
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    #Se setea el puerto
    port = sys.argv[1] if len(sys.argv) > 1 else 50050
    print(f"Waiting for connections...{os.getpid()}")

    #Se bindea/vincula el socket
    server_socket.bind(("0.0.0.0", port))
    server_socket.listen(5)

    #Para aceptar conexiones
    while True:
        client = server_socket.accept()
        connection, address = client
        #Nueva conexion al servidor
        print(f"Nueva conexion: {address}")
        welcome = "Bienvenido! " + "\r\n"
        connection.send(welcome.encode("ASCII"))

        #Nuevo proceso hijo
        child = mp.Process(target=connected_client, args=(client,))
        child.start()


if __name__ == "__main__":
    main()