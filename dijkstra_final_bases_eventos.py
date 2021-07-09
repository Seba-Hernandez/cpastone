import time
import math
import networkx as nx
import csv 
import json

#clases
#class Nodo():
#    def __init__(id, coordenada_x, coordenada_y):
#        self.id = id
#        self.coordenada_x = coordenada_x
#        self.coordenada_y = coordenada_y

#lectura archivo eventos.csv
with open('eventos.csv') as eventos:
    lista_eventos = []
    contador = 0
    for i in csv.reader(eventos):
        
        lista_eventos.append(i[0])
        contador += 1


def calcular_distancia(coordenada_x1, coordenada_y1, coordenada_x2, coordenada_y2):
    distancia = ((float(coordenada_y2) - float(coordenada_y1))**2 + (float(coordenada_x2) - float(coordenada_x1))**2)**(0.5)
    return distancia

def nodo_mas_cercano(coordenada_x_evento, coordenada_y_evento, Grafo):
    contador = 0
    for diccionario_nodo in Grafo.nodes.values():
        id_nodo = diccionario_nodo["Id"]
        coordenada_x_nodo = diccionario_nodo["Coordenada x"]
        coordenada_y_nodo = diccionario_nodo["Coordenada y"]
        distancia = calcular_distancia(coordenada_x_evento, coordenada_y_evento, coordenada_x_nodo, coordenada_y_nodo)
        if contador > 0:
            if distancia < distancia_minima_hasta_el_momento:
                distancia_minima_hasta_el_momento = distancia
                id_nodo_hasta_el_momento = id_nodo
        else:
            distancia_minima_hasta_el_momento = distancia
            id_nodo_hasta_el_momento = id_nodo
        contador += 1
    return id_nodo_hasta_el_momento


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
id_nodos = []
for nodo in lista_nodos:
    #print(nodo)
    informacion_nodo = nodo[0]
    lista_informacion_nodo = informacion_nodo.split(";")
    id_nodo = int(lista_informacion_nodo[0])
    id_nodos.append(id_nodo)
    coordenada_x_nodo = float(lista_informacion_nodo[1])
    coordenada_y_nodo = float(lista_informacion_nodo[2])
    Grafo.add_node(id_nodo)
    Grafo.nodes[id_nodo]["Id"] = id_nodo
    Grafo.nodes[id_nodo]["Coordenada x"] = coordenada_x_nodo
    Grafo.nodes[id_nodo]["Coordenada y"] = coordenada_y_nodo

print(len(id_nodos))
print(len(set(id_nodos)))

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

#función que obtiene rutas a mínimo tiempo dentro de un grafo ya instanciado Grafo, considerando una lista de orígenes y una lista de destinos dados como argumentos, además del tiempo sobre el cual se quiere hacer el cálculo de rutas entre los 24 tiempos que hay en el día
def rutas_tiempo_minimo_dijkstra_bidireccional(Grafo,lista_origenes,lista_destinos, string_tiempo):
    A=time.time()
    diccionario_tiempos={}
    diccionario_rutas={}
    contador=1
    diccionario_rutas_tiempo_minimo_bases_a_eventos = dict()
    for destino in lista_destinos:
        evento = destino
        diccionario_rutas_tiempo_minimo_bases_a_eventos[evento] = []
    for origen in lista_origenes:
        for destino in lista_destinos:
            id_evento = destino
            id_base = origen
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
            lista_de_3_elementos_sobre_ruta_base_a_evento = [tiempo_ruta_tiempo_minimo, lista_ruta_tiempo_minimo, id_base]
            diccionario_rutas_tiempo_minimo_bases_a_eventos[id_evento].append(lista_de_3_elementos_sobre_ruta_base_a_evento)

    B=time.time()
    segundos=B-A
    minutos=segundos/60
    horas=minutos/60

    for destino in lista_destinos:
        evento = destino
        diccionario_rutas_tiempo_minimo_bases_a_eventos[evento].sort()

    return diccionario_rutas_tiempo_minimo_bases_a_eventos

print("")
print("Número de nodos (intersecciones) del grafo", len(Grafo.nodes))
print("Número de arcos (calles) del grafo", len(Grafo.edges))
print("")


diccionario_centros_salud = dict()
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
            tupla_coordenadas = (coordenada_x_centro, coordenada_y_centro)
            bool_agregar_coordenada = False
            for id_centro in diccionario_centros_salud.keys():
                if id_centro == id_nodo_mas_cercano_a_centro:
                    bool_agregar_coordenada = True
            if bool_agregar_coordenada == True:
                diccionario_centros_salud[id_nodo_mas_cercano_a_centro].append(tupla_coordenadas)
            else:
                diccionario_centros_salud[id_nodo_mas_cercano_a_centro] = [tupla_coordenadas]
            




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
largo_lista_eventos = len(lista_eventos)
lista_reducida_eventos = lista_eventos[1:largo_lista_eventos] #eliminamos el header con los nombres de cada columna
print(len(lista_reducida_eventos))


diccionario_eventos = dict()
lista_nodos_eventos = []

for evento in lista_reducida_eventos:
    evento = evento.split(";")
    coordenada_x = evento[0]
    coordenada_y = evento[1]
    id_nodo_mas_cercano = nodo_mas_cercano(coordenada_x, coordenada_y, Grafo)
    tupla_coordenadas = (coordenada_x, coordenada_y)
    lista_nodos_eventos.append(id_nodo_mas_cercano)
    bool_agregar_coordenada = False
    for id_evento in diccionario_eventos.keys():
        if id_evento == id_nodo_mas_cercano:
            bool_agregar_coordenada = True
    if bool_agregar_coordenada == True:
        diccionario_eventos[id_nodo_mas_cercano].append(tupla_coordenadas)
    else:
        diccionario_eventos[id_nodo_mas_cercano] = [tupla_coordenadas]




set_nodos = set(lista_nodos_eventos)
print(f"Largo de lista con id de nodos asociados a eventos: {len(lista_nodos_eventos)}")
print(f"Largo de set con id de nodos asociados a eventos: {len(set(lista_nodos_eventos))}")
print(f"Los {len(lista_nodos_eventos)} eventos del primer día, se asocian a {len(set(lista_nodos_eventos))} nodos diferentes, por lo tanto existen {len(lista_nodos_eventos)-len(set(lista_nodos_eventos))} pares de eventos que se asocian a un mismo nodo de la ciudad")
for j, i in diccionario_eventos.items():
    cantidad_eventos_asociados_a_nodo = len(i)
    if cantidad_eventos_asociados_a_nodo > 1:
        print(f"El nodo con id {j} tiene asociado más de un evento. En particular, tiene asociado {cantidad_eventos_asociados_a_nodo} eventos. A continuación se muestran las coordenadas de los eventos asociados: {i}") 
print()
print(f"Largo de lista con id de nodos asociados a centros de salud: {len(lista_centros_destinos)}")
print(f"Largo de set con id de nodos asociados a centros de salud: {len(set(lista_centros_destinos))}")
print(f"Existen {len(lista_centros_destinos)-len(set(lista_centros_destinos))} pares de centros de salud asociados a un mismo nodo.")
for j, i in diccionario_centros_salud.items():
    cantidad_centros_asociados_a_nodo = len(i)
    if cantidad_centros_asociados_a_nodo > 1:
        print(f"El nodo con id {j} tiene asociado más de un centro de salud. En particular, tiene asociado {cantidad_centros_asociados_a_nodo} centros de salud. A continuación se muestran las coordenadas de los centros de salud asociados: {i}") 
print()
print(f"Largo de lista con id de nodos asociados a centros de salud y con id de nodos asociados a eventos: {len(list(set(lista_nodos_eventos))+list(set(lista_centros_destinos)))}")
print(f"Largo de set con id de nodos asociados a centros de salud y con id de nodos asociados a eventos: {len(set(list(set(lista_nodos_eventos))+list(set(lista_centros_destinos))))}")
print(f"Existen en {len(set(list(set(lista_nodos_eventos))+list(set(lista_centros_destinos)))) - len(list(set(lista_nodos_eventos))+list(set(lista_centros_destinos)))} ocasiones en que un mismo nodo está asociado tanto a un evento como a un centro de salud.")
for nodo_evento in list(set(lista_nodos_eventos)):
    for centro_salud in lista_centros_destinos:
        if nodo_evento == centro_salud:
            print(f'-El nodo con id {nodo_evento} y coordenadas ({Grafo.nodes[nodo_evento]["Coordenada x"]};{Grafo.nodes[nodo_evento]["Coordenada y"]}), tiene asociado tanto un evento como un centro de salud. El evento asociado ocurrió en las coordenadas: {diccionario_eventos[nodo_evento]}. El centro de salud tiene las siguientes coordenadas: {diccionario_centros_salud[nodo_evento]}')
print()
print(f"Largo de lista con id de nodos asociados a bases: {len(lista_bases_origenes)}")
print(f"Largo de set con id de nodos asociados a bases: {len(set(lista_bases_origenes))}")
print("")
if len(lista_bases_origenes) - len(set(lista_bases_origenes)) == 0:
    print("No existen bases que se asocien a un mismo nodo del grafo.")
    print("")
else:
    print("Sí existen bases que se asocien a un mismo nodo del grafo.")
    print("")
#Código para sacar rutas a tiempo mínimo usando dijkstra bidireccional con origen los nodos asociados a los evento de eventos.csv (todo el año) y destino los centros de salud
A = time.time()
diccionario_24_tiempos = dict()
contador = 0
for i in range(24):
    lista_bases_origenes = list(set(lista_bases_origenes))
    lista_eventos_destinos = list(set(id_nodos))
    
    fstring = f"Tiempo {i}"
    diccionario_dijkstra_bidireccional_tiempo_bases_a_eventos = rutas_tiempo_minimo_dijkstra_bidireccional(Grafo, lista_bases_origenes, lista_eventos_destinos, fstring)
    diccionario_24_tiempos[fstring] = diccionario_dijkstra_bidireccional_tiempo_bases_a_eventos
    cantidad_de_rutas_por_tiempo = len(lista_bases_origenes)*len(lista_eventos_destinos)
    contador += cantidad_de_rutas_por_tiempo
B = time.time()

print(f"El tiempo que tomó calcular las {contador} = {len(lista_bases_origenes)}*{len(lista_eventos_destinos)}*24 rutas a tiempo mínimo fue de {B-A} segundos, equivalente a {(B-A)/60} minutos, equivalente a {(B-A)/3600} horas")
print(f"El tiempo promedio que tomó calcular cada ruta fue de {(B-A)/contador} segundos, equivalente a {(B-A)/(60*contador)} minutos, equivalente a {(B-A)/(3600*contador)} horas")

# print(type(diccionario_24_tiempos))
# print(type(diccionario_24_tiempos["Tiempo 0"]))
# print(type(diccionario_24_tiempos["Tiempo 0"][3316]))
# print(len(diccionario_24_tiempos["Tiempo 0"][3316]))
# print(diccionario_24_tiempos["Tiempo 0"][3316][0])
# print(len(diccionario_24_tiempos["Tiempo 0"][3316][0]))
# print(type(diccionario_24_tiempos["Tiempo 0"][3316][0]))
# print(diccionario_24_tiempos["Tiempo 0"][3316][0][0])
# print(diccionario_24_tiempos["Tiempo 0"][3316][0][1])
# print(diccionario_24_tiempos["Tiempo 0"][3316][0][2])




# # {id_nodo_asociado_a_evento : lista_rutas_de_un_evento}
# # {1: [(20, [5,7,3,4,1], 5), ]}
# #for evento in lista_eventos:
# #    lista_rutas_de_un_evento = [[tiempo1, [ruta1], id_nodo_base1], [tiempo2, [ruta2], id_nodo_base2],...,[tiempo26, [ruta26], id_nodo_base26]]
# #    lista_rutas_de_un_evento.sort()

# #    diccionario_rutas_tiempo_minimo_bases_a_eventos[id_nodo_asociado_a_evento] = lista_rutas_de_un_evento




diccionario_24_tiempos_rutas_bases_a_eventos = diccionario_24_tiempos
# #diccionario_24_tiempos_rutas_bases_a_eventos = {"Tiempo 0": {id_evento1: [[tiempo1, [ruta1], id_base1], [tiempo2, [ruta2], id_base2], ....], ..., id_evento_79: [[tiempo1, [ruta1], id_base1], [tiempo2, [ruta2], id_base2], ....]}, ..., "Tiempo 23": {id_evento1: [[tiempo1, [ruta1], id_base1], [tiempo2, [ruta2], id_base2], ....], ..., id_evento_79: [[tiempo1, [ruta1], id_base1], [tiempo2, [ruta2], id_base2], ....]}}
# #A LA SIMULACIÓN HAY QUE PASARLE EL DICCIONARIO diccionario_24_tiempos_rutas_bases_a_eventos
with open("dijkstra_final_bases_a_eventos.json", "w") as f:
    json.dump(diccionario_24_tiempos_rutas_bases_a_eventos, f)