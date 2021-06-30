from math import trunc


def tiempo_24_horas(tiempo):
    formato_24_horas =trunc(tiempo - 24*trunc(tiempo/24))
    print(formato_24_horas)
    return(formato_24_horas)

#tiempo_24_horas(23.7)

import csv
 
with open('solucion_base_clusters.csv', newline='') as File:  
    reader = csv.reader(File)
    lista_id_clusters = []
    lista_id_bases = []
    contador = 0
    for row in reader:
        if contador > 0:
            print(row)
            print(type(row))
            id_cluster = row[0]
            lista_id_clusters.append(id_cluster)
            id_base = row[1]
            lista_id_bases.append(id_base)
        contador += 1

print(lista_id_clusters)
print(lista_id_bases)
print(len(list(set(lista_id_bases))))
print(len(list(set(lista_id_clusters))))