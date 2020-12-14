import sys
import random

'''
Generar archivo mochila, recibe el nombre de archivo, capacidad de la mochila, numero de elementos, minimo peso esperado,
maximo peso esperado, minimo beneficio esperado, maximo beneficio esperado, minima cantidad esperada, maxima cantidad
esperada, todos estos anteriores esperados para cada articulo. Devuelve un txt con la cantidad de elementos que se indiquen
y las caracteristicas mencionadas. 
'''
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

'''
Generar archivo alineamiento, recibe el nombre del archivo para el txt, el largo de la hilera 1 y el largo de la hilera2,
devuelve un txt con dos hileras con las letras A,T,C,G acomodadas aleatoriamente con el largo indicado en la entrada.
'''
def generar_archivo_alineamiento(archivo, largoH1, largoH2):
    salida = open(archivo, "x")
    letras = ["A","T","C","G"]
    largoH1 = int(largoH1)
    largoH2 = int(largoH2)
    largo = max(largoH1,largoH2)
    minimo = min(largoH1,largoH2)
    hilera1 = ""
    hilera2 = ""
    for i in range(largo):
        if i<minimo:
            letraH2 = random.randint(0, 3)
            hilera2+= letras[letraH2]
        letraH1 = random.randint(0,3)
        hilera1 += letras[letraH1]
    salida.write("1,-1,-2\n"+hilera1+"\n"+hilera2)
    salida.close()
'''Main es el controlador, que de acuerdo a la entrada, llama a los metodos indicados por el usuario en terminal'''
def main():
    if sys.argv[1] == "1":
        generar_archivo_mochila(sys.argv[2],sys.argv[3],int(sys.argv[4]),int(sys.argv[5]),int(sys.argv[6]),int(sys.argv[7]),int(sys.argv[8]),int(sys.argv[9]),int(sys.argv[10]))
        print("Archivo creado correctamente.")
    elif sys.argv[1] == "2":
        generar_archivo_alineamiento(sys.argv[2],sys.argv[3],int(sys.argv[4]))
        print("Archivo creado correctamente.")
    else:
        print("Problema no encontrado")
main()