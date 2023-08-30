import socket
import sys

#Creo un objeto del socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Obtengo el hostname local
host = socket.gethostname()

#Si se proporciona un argumento en la línea de comandos, usarlo como puerto sino usa el puerto 50011
port = int(sys.argv[1]) if len(sys.argv) > 1 else 50011

print("Conectando...")
#Se establece una conexión con el servidor utilizando el host y puerto
s.connect((host, port))
print("Realizado con éxito!")

print("Esperando datos...")
#Recibe datos del servidor
msg = s.recv(1024)
#Decodifica los datos en UTF-8 
print(msg.decode('UTF-8'))
#Se cierra la conexión del socket
s.close()
print("Cerrando...")