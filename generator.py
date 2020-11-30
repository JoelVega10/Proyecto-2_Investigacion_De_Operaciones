import sys
import random

def generar_archivo_mochila(archivo,w,n,minPeso,maxPeso,minBeneficio,maxBeneficio,minCantidad,maxCantidad):
    salida = open(archivo, "x")
    salida.write(w+"\n")
    while(n > 0):
        peso = random.randint(minPeso,maxPeso)
        beneficio = random.randint(minBeneficio,maxBeneficio)
        cantidad = random.randint(minCantidad,maxCantidad)
        elemento = str(peso) + "," + str(beneficio) + "," +str(cantidad)+"\n"
        salida.write(elemento)
        n-=1
    salida.close()

def main():
    if sys.argv[1] == "1":
        generar_archivo_mochila(sys.argv[2],sys.argv[3],int(sys.argv[4]),int(sys.argv[5]),int(sys.argv[6]),int(sys.argv[7]),int(sys.argv[8]),int(sys.argv[9]),int(sys.argv[10]))
        print("Archivo creado correctamente.")
main()