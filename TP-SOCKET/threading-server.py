import socket
import threading as th
import sys

#Funcion que sera ejecutada en cada hilo
def thread_client(client):
    print("Iniciando proceso hijo...")

    thread_conn, thread_addr = client

    while True:
        #Recibe datos del client
        data = thread_conn.recv(1024)
        #Si el client envia exit, se cierra la conexion
        if data == b"exit":
            print(f"Conexion cerrada por {thread_addr}")
            exit_c = "Cerrado."
            thread_conn.send(exit_c.encode("ASCII"))
            break
        print(f"Datos recibidos desde {thread_addr}: {data.decode('UTF-8')}")

        #Respuesta para el client
        response = f"Mensaje recibido. \r\n {data.decode('UTF-8').upper()}"
        thread_conn.send(response.encode("ASCII"))

#Funcion main
def main():
    #Crea el socket del servidor
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    #Se setea el puerto
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 50050
    print("Esperando conexiones")

    #Se bindea/vincula el socket
    server_socket.bind(("0.0.0.0", port))
    server_socket.listen(5)

    threads = []

    #Para aceptar conexiones
    while True:
        client = server_socket.accept()
        connection, address = client
        #Nueva conexion al servidor
        print(f"Nueva conexion: {address}")
        welcome = "Bienvenido! " + "\r\n"
        connection.send(welcome.encode("ASCII"))

        #Nuevo hilo
        t = th.Thread(target=thread_client, args=(client,))
        threads.append(t)
        t.start()

        #for t in threads:
        #    t.join()


if __name__ == "__main__":
    main()