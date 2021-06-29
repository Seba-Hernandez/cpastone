from math import trunc


def tiempo_24_horas(tiempo):
    formato_24_horas =trunc(tiempo - 24*trunc(tiempo/24))
    print(formato_24_horas)
    return(formato_24_horas)

tiempo_24_horas(23.7)