# from math import trunc


# def tiempo_24_horas(tiempo):
#     formato_24_horas =trunc(tiempo - 24*trunc(tiempo/24))
#     print(formato_24_horas)
#     return(formato_24_horas)

# #tiempo_24_horas(23.7)

# import csv
 
# with open('solucion_base_clusters.csv', newline='') as File:  
#     reader = csv.reader(File)
#     lista_id_clusters = []
#     lista_id_bases = []
#     contador = 0
#     for row in reader:
#         if contador > 0:
#             print(row)
#             print(type(row))
#             id_cluster = row[0]
#             lista_id_clusters.append(id_cluster)
#             id_base = row[1]
#             lista_id_bases.append(id_base)
#         contador += 1

# print(lista_id_clusters)
# print(lista_id_bases)
# print(len(list(set(lista_id_bases))))
# print(len(list(set(lista_id_clusters))))

lista = [0,80, 149, 216, 240, 306, 359, 422, 507, 570, 648, 708, 770, 831, 893, 952, 1023, 1086, 1168, 1235, 1309, 1379, 1444, 1495, 
1561, 1625, 1679, 1728, 1786, 1855, 1929, 1977, 2002, 2068, 2136, 2144, 2215, 2288, 2350, 2410, 2467, 2536, 2575, 2638, 2686, 2746,
 2787, 2853, 2924, 2988, 3040, 3109, 3163, 3223, 3289, 3294, 3368, 3439, 3485, 3549, 3603, 3671, 3745, 3788, 3851, 3908, 3974, 4045, 
 4106, 4164, 4228, 4298, 4305, 4378, 4442, 4521, 4591, 4669, 4736, 4804, 4866, 4905, 4963, 5038, 5068, 5149, 5214, 5280, 5342, 5406, 
 5486, 5569, 5619, 5698, 5772, 5836, 5885, 5964] 

for i in range(len(lista)):
    print(lista[i])
    print(lista[i+1])
    
# print(lista[0:10])