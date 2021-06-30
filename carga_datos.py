from os import path
import csv


def cargar_bases():
    lista_bases = list()
    ruta = path.join("bases.csv")
    with open(ruta, "r") as archivo:
        bases = archivo.readlines()
        for fila in bases[1:]:
            fila = fila.strip().split(";")
            fila[0] = float(fila[0])
            fila[1] = float(fila[1])
            lista_bases.append(fila)

    return lista_bases

def cargar_centros():
    lista_centros = list()
    ruta = path.join("centros.csv")
    with open(ruta, "r") as archivo:
        bases = archivo.readlines()
        for fila in bases[1:]:
            fila = fila.strip().split(";")
            fila[0] = float(fila[0])
            fila[1] = float(fila[1])
            lista_centros.append(fila)

    return lista_centros

# EVENTOS EN FORMATO HORA string HH:MM CON SEPARACIÓN DE COMA (;)
def cargar_eventos():
    lista_eventos = list()
    ruta = path.join("eventos.csv")
    with open(ruta, "r") as archivo:
        eventos = archivo.readlines()
        i = 0  # Después se borrará
        for fila in eventos[1:]:
            # print(fila)
            fila = fila.strip().split(";")
            lista_eventos.append(fila)
            i += 1  # Después se borrarán estas líneas  #
            if i == 6000: #Día 1: 79, D2 = 149, D3 = 239, D7 = 506, D15 = 1022, D31 = 2001
                break
            else:
                continue 

    return lista_eventos

def cargar_bases_de_solucion(nombre_archivo_solucion):
    with open(nombre_archivo_solucion, newline='') as File:  
        reader = csv.reader(File)
        lista_id_clusters = []
        lista_id_bases = []
        contador = 0
        for row in reader:
            if contador > 0:
   
                id_cluster = row[0]
                lista_id_clusters.append(id_cluster)
                id_base = row[1]
                lista_id_bases.append(id_base)
            contador += 1

    return list(set(lista_id_bases))


def cargar_solucion_a_diccionario(nombre_archivo_solucion):
    with open(nombre_archivo_solucion, newline='') as file:
        reader = csv.reader(file)
        diccionario_bases = dict()
        contador = 0
        for row in reader:
            if contador > 0:
                lista = row[0].split(";")
                id_base = lista[0]
                cantidad_ambulancias = lista[1]
                diccionario_bases[id_base] = cantidad_ambulancias
                
                
            contador +=1
    return diccionario_bases
        
                


# EVENTOS EN FORMATO HORA FLOAT CON SEPARACIÓN DE COMA (,)
# def cargar_eventos():
#     lista_eventos = list()
#     ruta = path.join("Eventos_horario_en_horas.csv")
#     with open(ruta, "r") as archivo:
#         eventos = archivo.readlines()
#         i = 0  # Después se borrará
#         for fila in eventos[1:]:
#             print(fila)
#             fila = fila.strip().split(",")
#             lista_eventos.append(fila)
#             i += 1  # Después se borrarán estas líneas  #
#             if i == 239: #Día 1: 79, D2 = 149, D3 = 239
#                 break
#             else:
#                 continue 

#     return lista_eventos

def cargar_nodos():
    lista_nodos = list()
    lista_nodos_floats = list()
    lista_aux = list()
    ruta = path.join("nodos.csv")
    with open(ruta, "r") as archivo:
        nodos = archivo.readlines()
        for fila in nodos[1:]:
            fila = fila.strip().split(";")
            lista_nodos.append(fila)

        for elemento in lista_nodos:
            for numero in elemento:
                lista_aux.append(float(numero))
            lista_nodos_floats.append(lista_aux)
            lista_aux = []

    return lista_nodos_floats

lista = cargar_eventos()
