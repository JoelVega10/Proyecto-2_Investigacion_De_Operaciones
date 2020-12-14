import sys
import numpy as np
import time
from itertools import permutations
from collections import defaultdict
start_time = time.time()
#------------------------------------------------------Entrada txt-----------------------------------------------------#

''' Abrir archivo recibe un archivo txt y almacena su contenido en la variable lineas'''
def abrir_archivo(input):
    lineas = [line.rstrip() for line in open(sys.argv[3])]
    return lineas

''' imprimir matriz, imprime los resultados de una matriz de una manera en que las filas y las columnas se vean representadas
de una manera estetica'''
def imprimir_matriz(matriz):
    print('\n'.join([''.join(['{:4}'.format(elemento) for elemento in fila])
      for fila in matriz]))


#-------------------------------------------------------Mochila PD-----------------------------------------------------#

'''Distribuir entrada recibe los elementos de la entrada, y devuelve una lista con los elementos distribuidos en las
cantidades indicadas en la entrada por cada elemento.'''
def distribuir_entrada(elementos_ordenados):
    elementos_distribuidos = []
    i = 0
    while(i<len(elementos_ordenados)):
        j = 0
        while(j<elementos_ordenados[i][2]):
            elementos_distribuidos.append(elementos_ordenados[i])
            j+=1
        i+=1
    return elementos_distribuidos


'''Generador lista de ceros recibe un n, que va a ser el largo de la lista de ceros que se retorna.'''
def generador_lista_de_ceros(n):
    return n*[0]


'''Crear matriz inicial mochila pd, recibe el numero de elementos y peso maximo de la mochila, y devuelve una matriz
con el numero de elementos como filas, y el numero maximo de peso como columnas, rellena de ceros.'''
def crear_matriz_inicial_mochila_pd(elementos_distribuidos,w):
    filas = len(elementos_distribuidos)
    matriz = []
    for i in range(filas):
        columnas = generador_lista_de_ceros(w+1)
        matriz.append(columnas)
    return matriz

'''llenar matriz recibe la matriz inicial creada en la funcion anterior y los elementos a usar en la mochila,
su salida es la matriz llena con los valores que el algoritmo de la mochila 0-1 nos da.'''
def llenar_matriz(matriz,elementos_distribuidos):
    i = 1
    while (i < len(matriz)):
        j = 0
        while (j < len(matriz[0])):
            if (elementos_distribuidos[i-1][0] <= j):
                if elementos_distribuidos[i-1][1] + matriz[i - 1][j - elementos_distribuidos[i-1][0]] > matriz[i - 1][j]:
                    matriz[i][j] = elementos_distribuidos[i-1][1] + matriz[i - 1][j - elementos_distribuidos[i-1][0]]
                else:
                    matriz[i][j] = matriz[i - 1][j]
            else:
                matriz[i][j] = matriz[i - 1][j]
            j += 1
        i += 1

'''Buscar elementos, recibe la matriz de mochila dp llena anteriormente y busca los elementos que se usaron para llegar
al beneficio maximo (la solucion) devuelve una lista con el numero de veces que se uso un elemento para la solucion'''
def buscar_elementos(elementos_distribuidos,elementos_ordenados,w,entrada,matriz):
    i = len(elementos_distribuidos)-1
    j = w
    soluciones = generador_lista_de_ceros(len(elementos_ordenados))
    while(i > 0 and j > 0):
        if matriz[i][j] > matriz[i-1][j]:
            soluciones[entrada.index(elementos_distribuidos[i-1].tolist())-1]+=1
            i = i - 1
            j = j - elementos_distribuidos[i-1][0]
        else:
            i = i - 1
    return soluciones


'''Imprimir soluciones mochila pd, recibe la lista de soluciones de la funcion anterior, e imprime las soluciones con el 
formato requerido.'''
def imprimir_soluciones_mochila_pd(matriz,w,soluciones,elementos_distribuidos):
    print(matriz[len(elementos_distribuidos)-1][w])
    for i in range(len(soluciones)):
        if soluciones[i] != 0:
            print(str(i+1)+","+str(soluciones[i])+ " # articulo " + str(i+1) + " " + str(soluciones[i]) + " unidades")

'''Mochila progra dinamica, llama a todas las funciones necesarias para imprimir la solucion de la mochila, recibe el nombre del archivo
de entrada e imprime la solucion de la mochila.'''
def mochila_progra_dinamica(input):
    entrada = abrir_archivo(input)
    i = 0
    while (i < len(entrada)):
        entrada[i] = [int(e) for e in entrada[i].split(',')]
        i += 1
    w = entrada[0][0]
    elementos = np.array(entrada[1:])
    elementos_ordenados = elementos[np.argsort(elementos[:, 0])]
    elementos_distribuidos = distribuir_entrada(elementos_ordenados)
    matriz = crear_matriz_inicial_mochila_pd(elementos_distribuidos,w)
    llenar_matriz(matriz,elementos_distribuidos)
    soluciones = buscar_elementos(elementos_distribuidos,elementos_ordenados,w,entrada,matriz)
    print("Mochila Programacion Dinamica")
    imprimir_soluciones_mochila_pd(matriz,w,soluciones,elementos_distribuidos)


#-------------------------------------------------------Mochila FB-----------------------------------------------------#
'''Mochila progra dinamica, llama a todas las funciones necesarias para imprimir la solucion de la mochila, recibe el nombre del archivo
de entrada e imprime la solucion de la mochila.'''
def mochila_fuerza_bruta(input):
    entrada = abrir_archivo(input)
    i = 0
    while (i < len(entrada)):
        entrada[i] = [int(e) for e in entrada[i].split(',')]
        i += 1
    w = entrada[0][0]
    elementos = np.array(entrada[1:])
    elementos_ordenados = elementos[np.argsort(elementos[:, 0])]
    elementos_distribuidos = distribuir_entrada(elementos_ordenados)
    n = len(elementos_distribuidos)
    soluciones = []
    beneficio = mochila_recursiva(w,elementos_distribuidos,n,entrada,soluciones)
    respuesta = generador_lista_de_ceros(len(entrada)-1)
    for i in range(len(soluciones)):
        respuesta[entrada.index(soluciones[i])-1] += 1
    print("Mochila Fuerza Bruta")
    print(beneficio)
    for i in range(len(respuesta)):
        if respuesta[i]!=0:
            print(str(i+1)+","+str(respuesta[i]) + " # articulo " + str(i+1) + " " + str(respuesta[i]) + " unidades")
'''Mochila recursiva, realiza la solucion de la mochila de una manera recursiva usando fuerza bruta, recibe el peso total que se tiene,
los elementos que se pueden utilizar, la cantidad de elementos, la entrada generada por el archivo txt, y una lista de soluciones
que esta llena de ceros al inicio para saber cuantas veces se uso un elemento'''
def mochila_recursiva(w, elementos_distribuidos,n,entrada,soluciones):
    lista_llevo = []
    lista_no_llevo = []
    if n == 0 or w == 0:
        return 0
    if (elementos_distribuidos[n-1][0] > w):
        return mochila_recursiva(w, elementos_distribuidos, n - 1,entrada,lista_no_llevo)

    lista_llevo.append(elementos_distribuidos[n-1].tolist())

    llevo = elementos_distribuidos[n-1][1] + mochila_recursiva(w - elementos_distribuidos[n-1][0], elementos_distribuidos, n - 1, entrada ,lista_llevo)
    no_llevo = mochila_recursiva(w, elementos_distribuidos, n - 1, entrada,lista_no_llevo)

    resp = max(llevo, no_llevo)
    if (resp == llevo):
        for i in lista_llevo:
            soluciones.append(i)
    else:
        for i in lista_no_llevo:
            soluciones.append(i)

    return resp
#--------------------------------------------------Alineamiento PD-----------------------------------------------------#
'''Alineamiento progra dinamica, llama a todas las funciones necesarias para imprimir la solucion del alineamiento de dos hileras, 
recibe el nombre del archivo de entrada e imprime la solucion del alineamiento.'''
def alineamiento_progra_dinamica(input):
    entrada = abrir_archivo(input)
    hilera1 = entrada[1]
    hilera2 = entrada[2]
    bandera = True
    if len(hilera1) < len(hilera2):
        hilera1 , hilera2 = hilera2 , hilera1
        bandera = False
    matriz = crear_matriz_inicial_alineamiento_pd(hilera1,hilera2)
    llenar_matriz_alineamiento_pd(matriz,hilera1,hilera2)
    encontrar_secuencias(matriz,hilera1,hilera2,bandera)


'''
Crear matriz inicial alineamiento, recibe las dos hileras que se les va realizar el alineamiento y devuelve una matriz llena de ceros del tamaño 
de filas de la hilera uno y el tamaño de columnas de la hilera dos, y despues en la primera columna y primera fila se multiplica el indice por menos 
dos, para tener en cuenta el valor de los gaps 
'''
def crear_matriz_inicial_alineamiento_pd(hilera1,hilera2):
    matriz = []
    for i in range(len(hilera1)+1):
        temp = generador_lista_de_ceros(len(hilera2)+1)
        matriz.append(temp)
    sum = -2
    j = 1
    while(j<=len(hilera1)):
        if j <= len(hilera2):
            matriz[0][j] = sum
        matriz[j][0] = sum
        sum+=-2
        j+=1
    return matriz

'''
Llenar matriz alineamiento recorre cada posicion y coloca el valor adecuado segun las posiciones anteriores en la matriz, recibe la matriz
la hilera 1 y la hilera 2.
'''
def llenar_matriz_alineamiento_pd(matriz,hilera1,hilera2):
    i = 1
    while(i<len(matriz)):
        j = 1
        while(j<len(matriz[0])):
            if hilera1[i-1] == hilera2[j-1]:
                matriz[i][j] = max(matriz[i-1][j]-2,matriz[i][j-1]-2,matriz[i-1][j-1]+1)
            else:
                matriz[i][j] = max(matriz[i-1][j]-2,matriz[i][j-1]-2,matriz[i-1][j-1]-1)
            j+=1
        i+=1
'''
Encontrar secuencias se coloca en la ultima posicion de la matriz con los valores ya colocados, y de acuerdo a la ruta que tome va creando la respuesta
de las dos hileras, recibe la matriz, hilera 1 , hilera 2 y una bandera que indica si en algun momento se intercambio la hilera 1 con la hilera 2
'''
def encontrar_secuencias(matriz,hilera1,hilera2,bandera):
    i = len(matriz)-1
    j = len(matriz[0])-1
    resp1 = ""
    resp2 = ""
    while(i > 0 or j > 0):
        print(str(i) + " "+str(j))
        if i == 0:
            resp2 = hilera2[j-1] + resp2
            resp1 = "_" + resp1
            j-=1
        elif j == 0:
            resp2 = "_" + resp2
            resp1 = hilera1[i-1] + resp1
            i-=1
        elif hilera1[i-1] == hilera2[j-1]:
            resp1 = hilera1[i-1] + resp1
            resp2 = hilera2[j-1] + resp2
            i-=1
            j-=1
        else:
            maximo = max(matriz[i][j-1],matriz[i-1][j],matriz[i-1][j-1])
            if maximo == matriz[i-1][j-1]:
                resp1 = hilera1[i - 1] + resp1
                resp2 = hilera2[j - 1] + resp2
                i -= 1
                j -= 1
            elif maximo == matriz[i-1][j]:
                resp2 = "_" + resp2
                resp1 = hilera1[i - 1] + resp1
                i-=1
            else:
                resp2 = hilera2[j - 1] + resp2
                resp1 = "_" + resp1
                j -= 1

    print("Tabla de resultados: ")
    imprimir_matriz(matriz)
    print("Scoring Final: " + str(matriz[len(matriz)-1][len(matriz[0])-1]))
    if bandera:
        print("Hilera 1: " + resp1)
        print("Hilera 2: " + resp2)
    else:
        print("Hilera 1: " + resp2)
        print("Hilera 2: " + resp1)


#--------------------------------------------------Alineamiento FB-----------------------------------------------------#
'''
Maximo valor, saca el maximo valor de una permutacion de la hilera 1, con todas las permutaciones de la hilera 2, y devuelve el maximo valor encontrado
la permutacion de la hilera 1 y la permutacion de la hilera 2 con la cual se obtuvo ese valor 
'''
def maximo_valor(permutacionH1,hilera1,memo,largo,hilera2):
    i = 0
    maximo = -10000
    resp = []
    simbolo = ['{}']
    gaps = ['_']
    lista = simbolo*len(hilera2)
    lista1 = gaps * largo
    per = lista+lista1
    for p in permutations(per):
        if p not in memo[permutacionH1]:
            memo[permutacionH1][p] = valor_secuencia(list(permutacionH1),list(p),hilera1,hilera2)
            if memo[permutacionH1][p][2]>maximo:
                maximo = memo[permutacionH1][p][2]
                resp = memo[permutacionH1][p]
    return resp

'''
Valor secuencia, recibe dos permutaciones, uno de la hilera 1 y otra de la hilera 2, y compara si hay un match se le suma 1 al valor, si hay un mismatch
se le resta 1 al valor y si hay un gap se le resta 2 al valor. Devuelve una lista con las permutaciones comparadas y el valor resultante.
'''
def valor_secuencia(permutacion1,permutacion2,hilera1,hilera2):
    valor = 0
    j = 0
    k = 0
    for i in range(len(permutacion1)):
        if permutacion1[i] == "_":
            if permutacion2[i] != "_":
                k+=1
            valor-=2
        elif permutacion2[i] == "_":
            if permutacion1[i] != "_":
                j+=1
            valor-=2
        elif (j < len(hilera1) and k < len(hilera2)) and (
                permutacion1[i].format(hilera1[j]) == permutacion2[i].format(hilera2[k])):
            k += 1
            j += 1
            valor += 1
        else:
            k+=1
            j+=1
            valor-=1
    return [permutacion1,permutacion2,valor]
'''
Obtener combinaciones secuencias recibe la hilera1 y la hilera2, y saca las combinaciones del tamaño de la suma de las dos hileras, añadiendo gaps, 
hasta el tamaño de la hilera con el mayor largo, sacando el maximo valor de las combinaciones de estas permutaciones, e imprime al final 
las dos permutaciones que dieron resultado al mayor valor y valor resultante.
'''
def obtener_combinaciones_secuencias(hilera1,hilera2,bandera):
    resta = len(hilera1)-len(hilera2)
    n = len(hilera1)-1
    maximo = -10000
    resp = []
    while(n >= 0):
        memo = defaultdict(dict)
        simbolo = ['{}']
        gaps = ['_']
        lista = simbolo * len(hilera1)
        lista1 = gaps * n
        per = lista+lista1
        for p in permutations(per):
            if p not in memo:
                res = maximo_valor(p, hilera1,memo,n+resta,hilera2)
                if res[2] > maximo:
                    maximo = res[2]
                    resp = res
        n-=1
    h1 = ""
    h2 = ""
    j = 0
    k = 0
    for i in range(len(resp[0])):
        if resp[0][i] == '{}':
            h1 = h1 +resp[0][i].format(hilera1[j])
            j+=1
        else:
            h1 = h1 + "_"
        if resp[1][i] == '{}':
            h2 = h2 +resp[1][i].format(hilera2[k])
            k+=1
        else:
            h2 = h2 + "_"
    print("Scoring Final: " + str(resp[2]))
    if bandera:
        print("Hilera 1: " + h1)
        print("Hilera 2: " + h2)
    else:
        print("Hilera 1: " + h2)
        print("Hilera 2: " + h1)

'''Alineamiento fuerza bruta , llama a todas las funciones necesarias para imprimir la solucion del alineamiento de dos hileras
recibe el nombre del archivo de entrada e imprime la solucion de la del alineamiento.'''
def alineamiento_fuerza_bruta(input):
    entrada = abrir_archivo(input)
    hilera1 = entrada[1]
    hilera2 = entrada[2]
    bandera = True
    if len(hilera1) < len(hilera2):
        hilera1 , hilera2 = hilera2 , hilera1
        bandera = False
    obtener_combinaciones_secuencias(hilera1,hilera2,bandera)


#------------------------------------------------------- Main ---------------------------------------------------------#
'''Main es el controlador, que de acuerdo a la entrada, llama a los metodos indicados por el usuario en terminal'''
def main():
    if sys.argv[1] == "-h":
        print("El presente proyecto se ejecuta en terminal de la siguiente manera:")
        print("python3 solver.py PROBLEMA ALGORITMO ARCHIVO")
        print("En donde PROBLEMA, ALGORITMO y ARCHIVO representan lo siguiente: ")
        print("PROBLEMA valor de 1 o 2, indicando el problema a resolver, 1 contenedor, 2 alineamiento.")
        print("ALGORITMO valor de 1 o 2, indicando el algoritmo a usar, 1 fuerza bruta, 2 programación dinámica")
        print("ARCHIVO indica el archivo de entrada donde el programa toma los parámetros del problema y procede a resolverlo con el algoritmo especificado.")
    else:
        if sys.argv[1] == "1":
            if sys.argv[2] == "1":
                mochila_fuerza_bruta(sys.argv[3])
            elif sys.argv[2] == "2":
                mochila_progra_dinamica(sys.argv[3])
            else:
                print("Algoritmo no reconocido")

        elif sys.argv[1] == "2":
            if sys.argv[2] == "1":
                alineamiento_fuerza_bruta(sys.argv[3])
            elif sys.argv[2] == "2":
                alineamiento_progra_dinamica(sys.argv[3])
            else:
                print("Algoritmo no reconocido")
        else:
            print("Problema no reconocido")

main()
#Imprime el tiempo que paso en la ejecucion del programa
print("--- %s segundos ---" % (time.time() - start_time))
