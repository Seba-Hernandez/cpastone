# import json 
# import matplotlib.pyplot as plt
from datetime import datetime
from datetime import timedelta
# lista =[]

# with open("diccionario_24_tiempos_rutas_bases_a_eventos.json") as f:
#     dicc_base_eventos = json.load(f)
    
# with open("diccionario_24_tiempos_rutas_eventos_a_centros.json") as f:
#     dicc_eventos_centros = json.load(f)
    
# with open("diccionario_24_tiempos_rutas_centros_a_bases.json") as f:
#     dicc_centros_bases = json.load(f)


# # for tiempo,diccionario_tiempo in dicc_eventos_centros.items():
    
# #     for evento,ruta_centro in diccionario_tiempo.items():
# #         lista.append(ruta_centro[0])
# #         print(f"Tiempo {ruta_centro[0]}, Ruta {ruta_centro[1]}, Id_centro {ruta_centro[2]}")
# #     print("")
# #     plt.plot(lista)
# #     plt.show()

# for tiempo,diccionario_tiempo in dicc_base_eventos.items():
    
#     for evento,rutas_evento_a_base in diccionario_tiempo.items():
#         contador = 1
#         for info_ruta in rutas_evento_a_base:
#             if contador == 2:
#                 lista.append(info_ruta[0])
#                 print(f"Tiempo {info_ruta[0]}, Ruta {info_ruta[1]}, Id_base {info_ruta[2]}")
#             contador += 1

#     print("")
#     plt.plot(lista)
#     plt.show()

def manejo_tiempo(fecha):
    datemask = '%H:%M'
    objeto = datetime.strptime(fecha, datemask)
    
    return objeto

def suma_tiempo(fecha1,fecha2):
    datemask = '%H:%M'
    objeto1 = datetime.strptime(fecha1, datemask)
    objeto2 = datetime.strptime(fecha2, datemask)

    suma_hora = objeto1.hour + objeto2.hour
    suma_min = objeto1.minute + objeto2.minute

    if suma_hora > 23:
        


def resta_tiempo(fecha1, fecha2):
    datemask = '%H:%M'
    objeto1 = datetime.strptime(fecha1, datemask)
    objeto2 = datetime.strptime(fecha2, datemask)

    resta_horario = objeto2 - objeto1
    resta_horas = (resta_horario.seconds)/(60*60)

    return [str(resta_horario)]#, resta_horas]


a = "23:00"
b = "03:00"

# c = a+ b
# print(c)

print(resta_tiempo(b,a))
print(resta_tiempo(a,b))





