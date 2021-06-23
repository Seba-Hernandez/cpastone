import time
import math
import networkx as nx
import csv 

#clases
#class Nodo():
#    def __init__(id, coordenada_x, coordenada_y):
#        self.id = id
#        self.coordenada_x = coordenada_x
#        self.coordenada_y = coordenada_y

#lectura archivo eventos.csv
#with open('eventos.csv') as eventos:
#    lista_eventos = []
#    contador = 0
#   for i in csv.reader(eventos):
#        lista_eventos.append(i)
#        contador += 1

#función que permite calcular la distancia euclidiana entre 2 puntos dados por dos pares de coordenadas (x,y)
def calcular_distancia(coordenada_x1,coordenada_y1, coordenada_x2, coordenada_y2):
    distancia = ((float(coordenada_y2) - float(coordenada_y1))**2 + (float(coordenada_x2) - float(coordenada_x1))**2)**(0.5)
    return distancia

#función que determina cuál nodo de los 2727 nodos que tiene el grafo se encuentra más cercano a las coordenadas dadas como argumento
#esta función permitirá asociar un nodo del grafo a cada par de coordenadas (x,y) para cada base y cada centro de salu
#OJO que cada base y cada centro de salud deben asociarse a un nodo distinto para evitar 2 o más entidades (ya sea base o centro de salud) asociadas a un mismo nodo del grafo
def nodo_mas_cercano(coordenada_x_centro, coordenada_y_centro, Grafo):
    contador = 0
    for diccionario_nodo in Grafo.nodes.values():
        id_nodo = diccionario_nodo["Id"]
        coordenada_x_nodo = diccionario_nodo["Coordenada x"]
        coordenada_y_nodo = diccionario_nodo["Coordenada y"]
        distancia = calcular_distancia(coordenada_x_centro, coordenada_y_centro, coordenada_x_nodo, coordenada_y_nodo)
        if contador > 0:
            if distancia < distancia_minima_hasta_el_momento:
                distancia_minima_hasta_el_momento = distancia
                id_nodo_hasta_el_momento = id_nodo
        else:
            distancia_minima_hasta_el_momento = distancia
            id_nodo_hasta_el_momento = id_nodo
        contador += 1
    return id_nodo_hasta_el_momento

#función que obtiene rutas a mínimo tiempo dentro de un grafo ya instanciado Grafo, considerando una lista de orígenes y una lista de destinos dados como argumentos, además del tiempo sobre el cual se quiere hacer el cálculo de rutas entre los 24 tiempos que hay en el día
def rutas_tiempo_minimo_dijkstra_bidireccional(Grafo,lista_origenes,lista_destinos, string_tiempo):
    A=time.time()
    diccionario_tiempos={}
    diccionario_rutas={}
    contador=1
    for origen in lista_origenes:
        for destino in lista_destinos:
            a=time.time()
            tupla_origen_destino = (origen,destino)
            resultados_tiempo_minimo = nx.bidirectional_dijkstra(Grafo, origen, destino,weight=string_tiempo)
            print(f"ALGORITMO DE DIJKSTRA BIDIRECCIONAL PARA TIEMPOS ({string_tiempo})")
            print("Ruta número", contador, "para", string_tiempo)
            tiempo_ruta_tiempo_minimo = resultados_tiempo_minimo[0]
            lista_ruta_tiempo_minimo = resultados_tiempo_minimo[1]
            diccionario_tiempos[tupla_origen_destino] = tiempo_ruta_tiempo_minimo
            diccionario_rutas[tupla_origen_destino] = lista_ruta_tiempo_minimo
            print("Tiempo mínimo desde el nodo",origen,"al nodo", destino,":",tiempo_ruta_tiempo_minimo)
            print("Lista de nodos de la ruta de tiempo mínimo", lista_ruta_tiempo_minimo)
            b=time.time()
            print("Tiempo que tomó la obtención de ruta a tiempo mínimo usando Dijkstra Bidireccional para este par origen-destino (",origen,"-",destino,"):",b-a,"segundos; equivalente a",
                  (b-a)/60,"minutos")
            print("")
            contador+=1
    B=time.time()
    segundos=B-A
    minutos=segundos/60
    horas=minutos/60
    print("Tiempo total en las 68536 rutas a mínimo tiempo usando Dijkstra Bidireccional: ",segundos,"segundos; equivalente a",minutos,"minutos; equivalente a",horas,"horas")
    print("Tiempo promedio por ruta en cálculo de mínimo tiempo usando Dijkstra Bidireccional: ",segundos/68536,"segundos; equivalente a",minutos/68536,"minutos; equivalente a",horas/68536,"horas")
    return diccionario_tiempos,diccionario_rutas

#creación del grafo utilizando la librería de networkx
Grafo = nx.DiGraph()

#lectura archivo nodos.csv
with open('nodos.csv') as nodos:
    lista_nodos = []
    contador = 0
    for i in csv.reader(nodos):
        if contador > 0:
            lista_nodos.append(i)
        contador += 1

#agregación al grafo de los nodos de nodos.csv, a un diccionario de nodos, donde cada llave del diccionario es el id del nodo, y el value es otro diccionario con llaves "Id", "Coordenada x" y "Coordenada y" y values los valores correspondientes  
for nodo in lista_nodos:
    informacion_nodo = nodo[0]
    lista_informacion_nodo = informacion_nodo.split(";")
    id_nodo = int(lista_informacion_nodo[0])
    coordenada_x_nodo = float(lista_informacion_nodo[1])
    coordenada_y_nodo = float(lista_informacion_nodo[2])
    Grafo.add_node(id_nodo)
    Grafo.nodes[id_nodo]["Id"] = id_nodo
    Grafo.nodes[id_nodo]["Coordenada x"] = coordenada_x_nodo
    Grafo.nodes[id_nodo]["Coordenada y"] = coordenada_y_nodo

#lectura archivo arcos.csv    
with open('arcos.csv') as calles:
    lista_calles = []
    contador = 0
    for i in csv.reader(calles):
        if contador > 0:
            lista_calles.append(i)
        contador += 1

for calle in lista_calles:
    informacion_calle = calle[0]
    lista_informacion_calle = informacion_calle.split(";")
    id_nodo_origen = int(lista_informacion_calle[0])
    id_nodo_destino = int(lista_informacion_calle[1])
    v0 = float(lista_informacion_calle[2])
    v1 = float(lista_informacion_calle[3])
    v2 = float(lista_informacion_calle[4])
    v3 = float(lista_informacion_calle[5])
    v4 = float(lista_informacion_calle[6])
    v5 = float(lista_informacion_calle[7])
    v6 = float(lista_informacion_calle[8])
    v7 = float(lista_informacion_calle[9])
    v8 = float(lista_informacion_calle[10])
    v9 = float(lista_informacion_calle[11])
    v10 = float(lista_informacion_calle[12])
    v11 = float(lista_informacion_calle[13])
    v12 = float(lista_informacion_calle[14])
    v13 = float(lista_informacion_calle[15])
    v14 = float(lista_informacion_calle[16])
    v15 = float(lista_informacion_calle[17])
    v16 = float(lista_informacion_calle[18])
    v17 = float(lista_informacion_calle[19])
    v18 = float(lista_informacion_calle[20])
    v19 = float(lista_informacion_calle[21])
    v20 = float(lista_informacion_calle[22])
    v21 = float(lista_informacion_calle[23])
    v22 = float(lista_informacion_calle[24])
    v23 = float(lista_informacion_calle[25])

    cola_arco = id_nodo_origen
    cabeza_arco = id_nodo_destino

    nodo_origen = Grafo.nodes[id_nodo_origen]
    nodo_destino = Grafo.nodes[id_nodo_destino]

    #x1,y1,x2,y2
    distancia_arco = calcular_distancia(nodo_origen["Coordenada x"], nodo_origen["Coordenada y"], nodo_destino["Coordenada x"], nodo_destino["Coordenada y"])

    Grafo.add_edge(cola_arco, cabeza_arco)
    Grafo.edges[cola_arco, cabeza_arco]["Distancia"] = distancia_arco
    Grafo.edges[cola_arco, cabeza_arco]["Tiempo 0"] = distancia_arco / v0
    Grafo.edges[cola_arco, cabeza_arco]["Tiempo 1"] = distancia_arco / v1
    Grafo.edges[cola_arco, cabeza_arco]["Tiempo 2"] = distancia_arco / v2
    Grafo.edges[cola_arco, cabeza_arco]["Tiempo 3"] = distancia_arco / v3
    Grafo.edges[cola_arco, cabeza_arco]["Tiempo 4"] = distancia_arco / v4
    Grafo.edges[cola_arco, cabeza_arco]["Tiempo 5"] = distancia_arco / v5
    Grafo.edges[cola_arco, cabeza_arco]["Tiempo 6"] = distancia_arco / v6
    Grafo.edges[cola_arco, cabeza_arco]["Tiempo 7"] = distancia_arco / v7
    Grafo.edges[cola_arco, cabeza_arco]["Tiempo 8"] = distancia_arco / v8
    Grafo.edges[cola_arco, cabeza_arco]["Tiempo 9"] = distancia_arco / v9
    Grafo.edges[cola_arco, cabeza_arco]["Tiempo 10"] = distancia_arco / v10
    Grafo.edges[cola_arco, cabeza_arco]["Tiempo 11"] = distancia_arco / v11
    Grafo.edges[cola_arco, cabeza_arco]["Tiempo 12"] = distancia_arco / v12
    Grafo.edges[cola_arco, cabeza_arco]["Tiempo 13"] = distancia_arco / v13
    Grafo.edges[cola_arco, cabeza_arco]["Tiempo 14"] = distancia_arco / v14
    Grafo.edges[cola_arco, cabeza_arco]["Tiempo 15"] = distancia_arco / v15
    Grafo.edges[cola_arco, cabeza_arco]["Tiempo 16"] = distancia_arco / v16
    Grafo.edges[cola_arco, cabeza_arco]["Tiempo 17"] = distancia_arco / v17
    Grafo.edges[cola_arco, cabeza_arco]["Tiempo 18"] = distancia_arco / v18
    Grafo.edges[cola_arco, cabeza_arco]["Tiempo 19"] = distancia_arco / v19
    Grafo.edges[cola_arco, cabeza_arco]["Tiempo 20"] = distancia_arco / v20
    Grafo.edges[cola_arco, cabeza_arco]["Tiempo 21"] = distancia_arco / v21
    Grafo.edges[cola_arco, cabeza_arco]["Tiempo 22"] = distancia_arco / v22
    Grafo.edges[cola_arco, cabeza_arco]["Tiempo 23"] = distancia_arco / v23

print("")
print("Número de nodos (intersecciones) del grafo", len(Grafo.nodes))
print("Número de arcos (calles) del grafo", len(Grafo.edges))
print("")


#lectura archivo centros.csv
with open('centros.csv') as centros:
    lista_centros_destinos = []
    contador = 0
    ca = []
    caa = []
    for i in csv.reader(centros):
        if contador > 0:
            lista_informacion_centros = i[0].split(";")
            coordenada_x_centro = float(lista_informacion_centros[0])
            coordenada_y_centro = float(lista_informacion_centros[1])
            id_nodo_mas_cercano_a_centro = nodo_mas_cercano(coordenada_x_centro, coordenada_y_centro, Grafo)
            lista_centros_destinos.append(id_nodo_mas_cercano_a_centro)
            if (Grafo.nodes[id_nodo_mas_cercano_a_centro]["Coordenada x"], Grafo.nodes[id_nodo_mas_cercano_a_centro]["Coordenada y"] ) in ca:
                #print(Grafo.nodes[id_nodo_mas_cercano_a_centro]["Coordenada x"], Grafo.nodes[id_nodo_mas_cercano_a_centro]["Coordenada y"])
                #print(coordenada_x_centro, coordenada_y_centro)
                for i in caa:
                    id_nodo_mas_cercano_a_centro2 = nodo_mas_cercano(i[0], i[1], Grafo)
                    if id_nodo_mas_cercano_a_centro == id_nodo_mas_cercano_a_centro2:
                        #print(i[0], i[1])
                        #print(coordenada_x_centro, coordenada_y_centro)
                        #print(Grafo.nodes[id_nodo_mas_cercano_a_centro]["Coordenada x"], Grafo.nodes[id_nodo_mas_cercano_a_centro]["Coordenada y"])
                        pass
            else:
                ca.append((Grafo.nodes[id_nodo_mas_cercano_a_centro]["Coordenada x"],Grafo.nodes[id_nodo_mas_cercano_a_centro]["Coordenada y"] ))
                caa.append((coordenada_x_centro, coordenada_y_centro))
            #print()
        contador += 1

#lectura archivo bases.csv
with open('bases.csv') as bases:
    lista_bases_origenes = []
    contador = 0
    ca = []
    caa = []
    for i in csv.reader(bases):
        if contador > 0:
            lista_informacion_bases = i[0].split(";")
            coordenada_x_base = float(lista_informacion_bases[0])
            coordenada_y_base = float(lista_informacion_bases[1])
            id_nodo_mas_cercano_a_base = nodo_mas_cercano(coordenada_x_base, coordenada_y_base, Grafo)
            lista_bases_origenes.append(id_nodo_mas_cercano_a_base)
            #print(id_nodo_mas_cercano_a_base)
            #print()
            if (Grafo.nodes[id_nodo_mas_cercano_a_base]["Coordenada x"], Grafo.nodes[id_nodo_mas_cercano_a_base]["Coordenada y"] ) in ca:
                #print(Grafo.nodes[id_nodo_mas_cercano_a_centro]["Coordenada x"], Grafo.nodes[id_nodo_mas_cercano_a_centro]["Coordenada y"])
                #print(coordenada_x_centro, coordenada_y_centro)
                for i in caa:
                    id_nodo_mas_cercano_a_base2 = nodo_mas_cercano(i[0], i[1], Grafo)
                    if id_nodo_mas_cercano_a_base == id_nodo_mas_cercano_a_base2:
                        #print(i[0], i[1])
                        #print(coordenada_x_centro, coordenada_y_centro)
                        #print(Grafo.nodes[id_nodo_mas_cercano_a_centro]["Coordenada x"], Grafo.nodes[id_nodo_mas_cercano_a_centro]["Coordenada y"])
                        pass
            else:
                ca.append((Grafo.nodes[id_nodo_mas_cercano_a_base]["Coordenada x"],Grafo.nodes[id_nodo_mas_cercano_a_base]["Coordenada y"] ))
                caa.append((coordenada_x_base, coordenada_y_base))
            #print()
        contador += 1


#creación de lista_nodos la cual contiene a todos los nodos del grafo que no corresponden a una base ni a un centro de salud
lista_nodos = []
for nodo in Grafo.nodes():
    set_centros = set(lista_centros_destinos)
    set_bases = set(lista_bases_origenes)
    if nodo not in set_centros and nodo not in set_bases:
        if nodo in lista_nodos:
            print(nodo)
        lista_nodos.append(nodo)

#código para ver si todas las bases y centros de salud se asociaron a distintos nodos del grafo
#se espera que len(lista_centros_destinos) = len(set(lista_centros_destinos)) = 67, para que no haya 2 o más centros de salud asociados a un mismo nodo del grafo
#se espera que len(lista_bases_origenes) = len(set(lista_bases_origenes)) = 26, para que no haya 2 o más bases asociadas a un mismo nodo de grafo
#se espera que  len(lista_centros_destinos+lista_bases_origenes) = 93, para que no haya 2 o más entidades (ya sean base o centro de salud) asociadas a un mismo nodo del grafo

#print(len(list(set_centros)))
#print(len(lista_nodos))
#print(len(lista_centros_destinos))
#print(len(set(lista_centros_destinos)))
#print(len(lista_bases_origenes))
#print(len(set(lista_bases_origenes)))
#lista_prueba = lista_centros_destinos + lista_bases_origenes
#print(len(lista_prueba))
#print(len(set(lista_prueba)))
#print(calcular_distancia(31.5, 71.8, 33.0, 71.0))
#print(calcular_distancia(31.9, 71.8, 33.0, 71.0))

#Código para sacar rutas a tiempo mínimo usando dijkstra bidireccional con origen las bases y destino los potenciales nodos de demanda de atención médica
A = time.time()
for i in range(24):
    fstring = f"Tiempo {i}"
    dijkstra_bidireccional_tiempo_bases_nodos = rutas_tiempo_minimo_dijkstra_bidireccional(Grafo, lista_bases_origenes, lista_nodos, fstring)
B = time.time()
print(f"El tiempo que tomó calcular las 1644864 = 2636*26*24 rutas a tiempo mínimo fue de {B-A} segundos, equivalente a {(B-A)/60} minutos, equivalente a {(B-A)/3600} horas")
print(f"El tiempo promedio que tomó calcular cada ruta fue de {(B-A)/1644864} segundos, equivalente a {(B-A)/(60*1644864)} minutos, equivalente a {(B-A)/(3600*1644864)} horas")

#Código para sacar rutas a tiempo mínimo usando dijkstra bidireccional con origen los potenciales nodos de demanda de atención médica y destino los centros de salud
A = time.time()
for i in range(24):
    fstring = f"Tiempo {i}"
    dijkstra_bidireccional_tiempo_nodos_centros_de_salud = rutas_tiempo_minimo_dijkstra_bidireccional(Grafo, lista_nodos, lista_centros_destinos, fstring)
B = time.time()
print(f"El tiempo que tomó calcular las 1644864 = 2636*26*24 rutas a tiempo mínimo fue de {B-A} segundos, equivalente a {(B-A)/60} minutos, equivalente a {(B-A)/3600} horas")
print(f"El tiempo promedio que tomó calcular cada ruta fue de {(B-A)/1644864} segundos, equivalente a {(B-A)/(60*1644864)} minutos, equivalente a {(B-A)/(3600*1644864)} horas")