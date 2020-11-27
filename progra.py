import sys
import numpy as np
#------------------------------------------------------Entrada txt-----------------------------------------------------#

''' Abrir archivo recibe un archivo txt y almacena su contenido en la variable lineas'''
def abrir_archivo():
    archivo = open(sys.argv[1],'r')
    lineas = archivo.readlines()
    i = 0
    while( i < len(lineas) ):
        lineas[i] = [int(e) for e in lineas[i].split(',')]
        i+=1
    return lineas

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


'''
print('\n'.join([''.join(['{:4}'.format(item) for item in row])
      for row in matriz]))
'''

'''Imprimir soluciones mochila pd, recibe la lista de soluciones de la funcion anterior, e imprime las soluciones con el 
formato requerido.'''
def imprimir_soluciones_mochila_pd(matriz,w,soluciones,elementos_distribuidos):
    print(matriz[len(elementos_distribuidos)-1][w])
    for i in range(len(soluciones)):
        if soluciones[i] != 0:
            print(str(i+1)+","+str(soluciones[i]))


def mochila_progra_dinamica():
    entrada = abrir_archivo()
    w = entrada[0][0]
    elementos = np.array(entrada[1:])
    elementos_ordenados = elementos[np.argsort(elementos[:, 0])]
    elementos_distribuidos = distribuir_entrada(elementos_ordenados)
    matriz = crear_matriz_inicial_mochila_pd(elementos_distribuidos,w)
    llenar_matriz(matriz,elementos_distribuidos)
    soluciones = buscar_elementos(elementos_distribuidos,elementos_ordenados,w,entrada,matriz)
    imprimir_soluciones_mochila_pd(matriz,w,soluciones,elementos_distribuidos)


#-------------------------------------------------------Mochila FB-----------------------------------------------------#

def mochila_fuerza_bruta():
    entrada = abrir_archivo()
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
    print(beneficio)
    for i in range(len(respuesta)):
        if respuesta[i]!=0:
            print(str(i+1)+","+str(respuesta[i]))

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
