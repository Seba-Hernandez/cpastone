from os import path


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

def cargar_eventos():
    lista_eventos = list()
    ruta = path.join("Eventos_horario_en_horas.csv")
    with open(ruta, "r") as archivo:
        eventos = archivo.readlines()
        i = 0  # Después se borrará
        for fila in eventos[1:]:
            fila = fila.strip().split(",")
            lista_eventos.append(fila)
            i += 1  # Después se borrarán estas líneas
            if i == 79:
                break
            else:
                continue

    return lista_eventos

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
