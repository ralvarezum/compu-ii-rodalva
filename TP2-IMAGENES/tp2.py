import argparse
import http.server
import socketserver
import threading
from queue import Queue
from PIL import Image

image_queue = Queue()

def convert_to_grayscale(input_file, output_file):
    try:
        image = Image.open(input_file)
        grayscale_image = image.convert('L')
        grayscale_image.save(output_file)
    except Exception as e:
        print(f"Error al convertir la imagen a escala de grises: {e}")

def http_server(ip, port):
    try:
        httpd = socketserver.TCPServer(("0.0.0.0", port), http.server.SimpleHTTPRequestHandler)
        print(f"Servidor HTTP escuchando en {ip}:{port}")
        httpd.serve_forever()
    except Exception as e:
        print(f"Error en el servidor HTTP: {e}")

def image_processing_worker():
    while True:
        input_file, output_file = image_queue.get()
        convert_to_grayscale(input_file, output_file)
        image_queue.task_done()

def main():
    parser = argparse.ArgumentParser(description="Tp2 - Procesado de imágenes a gris")
    parser.add_argument("-i", "--ip", required=True, help="Dirección IP")
    parser.add_argument("-p", "--port", type=int, required=True, help="Puerto")
    args = parser.parse_args()

    ip = args.ip
    port = args.port

   
    http_server_thread = threading.Thread(target=http_server, args=(ip, port))
    http_server_thread.start()

    
    for _ in range(4):
        worker_thread = threading.Thread(target=image_processing_worker)
        worker_thread.daemon = True
        worker_thread.start()

    try:
        while True:
            input_file = "oasis.jpg"  
            output_file = "oasis-gris.jpg"  
            image_queue.put((input_file, output_file))
            image_queue.join()
    except Exception as e:
        print(f"Error en el manejo de IPC: {e}")

if __name__ == "__main__":
    main()
