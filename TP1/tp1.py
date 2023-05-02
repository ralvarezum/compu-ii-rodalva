import argparse
import os
import sys

def invertir_lineas(linea):
    return linea.strip()[::-1]

def main():
    parser = argparse.ArgumentParser(description='Invierte cada línea de un archivo.')
    parser.add_argument('archivo', help='Archivo a procesar.')
    args = parser.parse_args()

    try:
        with open(args.archivo, 'r') as file:
            lineas = file.readlines()
    except FileNotFoundError:
        print(f"Error: el archivo {args.archivo} no se encontró.")
        sys.exit(1)

    pipes = []
    for linea in lineas:
        r, w = os.pipe()
        pid = os.fork()
        if pid == 0:
            os.close(r)
            w = os.fdopen(w, 'w')
            w.write(invertir_lineas(linea))
            w.close()
            sys.exit(0)
        else:
            os.close(w)
            pipes.append(r)

    resultados = []

    for pipe in pipes:
        r = os.fdopen(pipe)
        resultado = r.readline().strip()
        resultados.append(resultado)
        r.close()

    for _ in lineas:
        os.wait()

    for resultado in resultados:
        print(resultado, end='\n')

if __name__ == '__main__':
    main()