# from _typeshed import OpenTextModeReading
from collections import deque
from random import expovariate, randint, uniform, seed
from datetime import datetime, timedelta
import time
from math import sqrt, floor
from datetime import datetime
from datetime import timedelta
from math import trunc
import pandas as pd

from numpy import printoptions
import numpy as np
from carga_datos import cargar_bases, cargar_centros, cargar_eventos, cargar_nodos, cargar_bases_de_solucion
from random import choice, shuffle
import networkx as nx
import csv 
import json
import matplotlib.pyplot as plt

def segundo_elemento(elem):
    return elem.duracion_total + elem.tiempo_llegada

def tiempo_24_horas(tiempo):
    formato_24_horas =trunc(tiempo - 24*trunc(tiempo/24))
    # print(formato_24_horas)
    return(formato_24_horas)



def manejo_tiempo(fecha):
    datemask = '%H:%M:%S'
    objeto = datetime.strptime(fecha, datemask)
    return objeto


class Eventos:
    _id = 0
    def __init__(self, tiempo_inicio, posicion_x, posicion_y, preparacion, atencion, derivacion):
        self._id += 1
        self.posicion_x = posicion_x
        self.posicion_y = posicion_y
        #self.bases = self.asignar_base()
        self.preparacion = preparacion / 60 #DESDE QUE LLAMAN HASTA QUE LA AMBULANCIA SALE
        self.viaje_llamado = 0  #CUANTO ME DEMORO EN LLEGAR AL ACCIDENTE
        self.atencion = atencion / 60     #DESDE QUE LLEGA HASTA EL LLAMADO, HASTA QUE PARTE AL CENTRO
        self.viaje_hospital = 0 #CUANTO ME DEMORO EN LLEGAR AL HOSPITAL
        self.derivacion = derivacion / 60  #DESDE QUE LLEGA AL HOSPITAL, HASTA QUE PARTE A LA BASE
        self.viaje_base = 0    #CUANTO ME DEMORO EN RETORNAR A LA BASE
        self.tiempo_llegada = tiempo_inicio
        # self.tiempo_termino = None
        self.tiempo_en_cola = 0
        self.duracion_total = self.tiempo_en_cola + self.preparacion + self.viaje_llamado + self.atencion +  self.viaje_hospital + self.derivacion \
            + self.viaje_base
        self.nodo_asociado = None
        self.hora_partida = self.tiempo_llegada + self.preparacion
        #self.hora_evento = floor(tiempo_inicio)
        self.ambulancia = None  

    def actualizar_duracion_total(self):
        self.duracion_total = self.tiempo_en_cola + self.preparacion + self.viaje_llamado + self.atencion +  self.viaje_hospital + self.derivacion \
            + self.viaje_base
    #SUMAR TIEMPOS
    
    def obtener_viaje_llamado(self): #DE LAS 20 RUTAS MÍNIMAS, ME QUEDO CON LA QUE ESTÁ MÁS CERCANA Y TIENE AMBULANCIA DISP
        pass
    def obtener_viaje_hospital(self):
        pass
    def obtener_viaje_base(self):
        pass


    def generar_tiempo_termino (self):
        tiempo = self.preparacion + self.viaje_llamado + self.atencion + self.viaje_hospital + self.derivacion + self.viaje_base
        return(tiempo)

    #ASIGNAR UNA BASE

    def asignar_base(self):
        lista_bases_que_cubren = []
         #cargar las bases que cubren el evento

         #INSTANCIAR BASES?

        return(lista_bases_que_cubren)

class Ambulancia:
    def __init__(self,id):
        self.id = id
        self.disponible = True
        self.base_asignada = None
        #self.base_asignada = None  # Asignación de base
        

    #def hospital_mas_cercano(self):  # aún debo ver si uso self.hospitales o trabajo esa lista fuera
     #   for hospital in lista_centros_salud_creados:
      #      self.distancias_hospitales.append(sqrt((hospital.posicion_x - self.posicion_x) ** 2) +
       #                                       ((hospital.posicion_y - self.posicion_y) ** 2))
        #index_distancia_cercana = self.distancias_hospitales.index(min(self.distancias_hospitales))
        #self.hospital_mas_cercano = self.hospitales[index_distancia_cercana]

    def __repr__(self):
        return f"Ambulancia Nº{self.id}"

    def __getitem__(self, item):
        return item


class Base:
    def __init__(self, posicion_x, posicion_y, _id):
        self.posicion_x = float(posicion_x)
        self.posicion_y = float(posicion_y)
        self.activada = False  # 0 si no hay ambulancia, 1 si hay una ambulancia
        self.id = _id
        self.lista_ambulancias_base = []
        self.ambulancia_asignada = None  # Asignación de ambulancia
        self.nodo_ubicacion = None
        self.nodo_asociado = None
        self.num_llegadas = []
        self.num_termino = []
        self.num_manejados = []

    

    def enviar_ambulancia(self):
        if self.ocupacion == 1:
            pass
        else:
            print(f"La base no tiene una ambulancia disponible")
        pass

    def __repr__(self):
        return f"Base Nº{self.id}"

    def __getitem__(self, item):
        return item

class CallCenter:
    def __init__(self ):
        self.lista_bases = []
        self.lista_eventos = cargar_eventos()
        self.lista_centros_salud_creados = []
        self.lista_bases_creadas = []
        self.lista_ambulancias_creadas = []
        #Listas para decidir
        self.lista_eventos_cola = []

        self.lista_de_llegadas = [] 
        self.lista_de_terminos = []
        self.lista_eventos_manejados = []
        self.lista_cola = deque([])
        self.grafo = None

        self.contador_ambulancia = 0

        self.lista_tiempos_en_cola = []
        self.PARAMETRO_UMBRAL = 2

        # usamos datetime para manejar temporalidad
        tiempo = 0

        #Plot variables
        self.lista_de_duraciones =[]
        self.lista_de_tiempos_respuesta =[]
                    

        # seteamos variables de tiempo
        self.tiempo_actual = tiempo

        self.dicc_base_eventos = None
        self.dicc_eventos_centros = None
        self.dicc_centros_bases = None
        # self.tiempo_maximo = tiempo + timedelta(hours = tiempo_simulacion) ##Qué es timedelta
        # self.proximo_llamado_llega = self.tiempo_actual #Agregar
        # self.tiempos_abandono = [[self.tiempo_actual.replace(year=3000), None]]
        self.crear_grafo()
        self.cargar_lista_llegadas()
        self.cargar_lista_centros()
        self.cargar_lista_ambulancias()
        self.cargar_lista_bases()
        
        self.asociar_evento_nodo()
        self.cargar_diccionarios()



    def cargar_lista_bases(self):

        # #17 bases activadas: ['0', '3', '6', '12', '9', '5', '23', '25', '20', '8', '10', '13', '7', '1', '11', '18', '22'] con 7, 9 y 25 asignados a 2 clusters y el resto a 1 cluster, umbral = 1 hora
        # self.PARAMETRO_UMBRAL = 1 
        # lista_bases = cargar_bases()
        # #lista_bases_solucion = cargar_bases_de_solucion("solucion_base_clusters.csv")
        # j = 0
        # i = 0
        # for base in lista_bases:
        #     Base_n = Base(base[0], base[1], i) 
        #     i += 1
        #     self.lista_bases_creadas.append(Base_n)
        #     base.lista_ambulancias_base.append(self.lista_ambulancias_creadas[j])
        #     base.activada = True
        #     self.lista_ambulancias_creadas[j].base_asignada = base
        #     j += 1
        # for base in self.lista_bases_creadas:
        #     base.nodo_asociado = self.nodo_mas_cercano(base.posicion_x, base.posicion_y)


        #20 bases activadas: ['0', '3', '6', '12', '9', '5', '23', '25', '20', '8', '10', '13', '7', '1', '11', '18', '22'] donde las bases 7, 9 y 25 tienen 2 ambulancias, umbral = 1 hora
        # self.PARAMETRO_UMBRAL = 1 
        # lista_bases = cargar_bases()
        # lista_bases_solucion = cargar_bases_de_solucion("solucion_base_clusters.csv")
        # j = 0
        # i = 0
        # for base in lista_bases:
        #     Base_n = Base(base[0], base[1], i) 
        #     i += 1
        #     self.lista_bases_creadas.append(Base_n)
        # #print(self.lista_bases_creadas)
        # for id_base in lista_bases_solucion:
        #     for base in self.lista_bases_creadas:
        #         if int(id_base) == base.id:
        #             base.lista_ambulancias_base.append(self.lista_ambulancias_creadas[j])
        #             base.activada = True
        #             self.lista_ambulancias_creadas[j].base_asignada = base
        #             j += 1
        # contador_bases_adicionales = 0
        # for id_base in lista_bases_solucion:
        #     for base in self.lista_bases_creadas:
        #         if int(id_base) == base.id:
        #             if int(id_base) == 7 or int(id_base) == 9 or int(id_base) == 25:
        #                 base.lista_ambulancias_base.append(self.lista_ambulancias_creadas[j+contador_bases_adicionales])
        #                 base.activada = True
        #                 self.lista_ambulancias_creadas[j+contador_bases_adicionales].base_asignada = base
        #                 contador_bases_adicionales += 1
        # for base in self.lista_bases_creadas:
        #     base.nodo_asociado = self.nodo_mas_cercano(base.posicion_x, base.posicion_y)

        # #20 bases activadas: ['0', '3', '6', '12', '9', '5', '23', '25', '20', '8', '10', '13', '7', '1', '11', '18', '22'] donde las bases 7, 9 y 25 tienen 2 ambulancias, umbral = 2 hora
        # self.PARAMETRO_UMBRAL = 2 
        # lista_bases = cargar_bases()
        # lista_bases_solucion = cargar_bases_de_solucion("solucion_base_clusters.csv")
        # j = 0
        # i = 0
        # for base in lista_bases:
        #     Base_n = Base(base[0], base[1], i) 
        #     i += 1
        #     self.lista_bases_creadas.append(Base_n)
        # #print(self.lista_bases_creadas)
        # for id_base in lista_bases_solucion:
        #     for base in self.lista_bases_creadas:
        #         if int(id_base) == base.id:
        #             base.lista_ambulancias_base.append(self.lista_ambulancias_creadas[j])
        #             base.activada = True
        #             self.lista_ambulancias_creadas[j].base_asignada = base
        #             j += 1
        # contador_bases_adicionales = 0
        # for id_base in lista_bases_solucion:
        #     for base in self.lista_bases_creadas:
        #         if int(id_base) == base.id:
        #             if int(id_base) == 7 or int(id_base) == 9 or int(id_base) == 25:
        #                 base.lista_ambulancias_base.append(self.lista_ambulancias_creadas[j+contador_bases_adicionales])
        #                 base.activada = True
        #                 self.lista_ambulancias_creadas[j+contador_bases_adicionales].base_asignada = base
        #                 contador_bases_adicionales += 1
        # for base in self.lista_bases_creadas:
        #     base.nodo_asociado = self.nodo_mas_cercano(base.posicion_x, base.posicion_y)



        #solución modelo
        self.PARAMETRO_UMBRAL = 2
        lista_bases = cargar_bases()
        lista_bases_solucion = cargar_bases_de_solucion("solucion_base_clusters.csv")
        j = 0
        i = 0
        dic_ambulancias_por_base = {2:1, 4:2, 9:2, 14:4, 15:1, 17:3, 19:2, 22:3, 25:2}
        for base in lista_bases:
            Base_n = Base(base[0], base[1], i) 
            i += 1
            self.lista_bases_creadas.append(Base_n)
        #print(self.lista_bases_creadas)
        for id_base, cantidad_ambulancias in dic_ambulancias_por_base.items():
            for base in self.lista_bases_creadas:
                if int(id_base) == base.id:
                    for k in range(0, cantidad_ambulancias):
                        base.lista_ambulancias_base.append(self.lista_ambulancias_creadas[j])
                        base.activada = True
                        self.lista_ambulancias_creadas[j].base_asignada = base
                        j += 1
        for base in self.lista_bases_creadas:
            base.nodo_asociado = self.nodo_mas_cercano(base.posicion_x, base.posicion_y)




    def cargar_lista_centros(self):
        lista_centros_salud = cargar_centros()
        j = 0
        for centro in lista_centros_salud:
            Centro_n = CentrosSalud(centro[0], centro[1], j)   ###########BORRAR EL QUE SE REPITE
            self.lista_centros_salud_creados.append(Centro_n)
            j += 1
        for centro in self.lista_centros_salud_creados:
            centro.nodo_asociado = self.nodo_mas_cercano(centro.posicion_x, centro.posicion_y)

    def cargar_lista_ambulancias(self):
        z = 0
        while z != 20:
            ambulancia = Ambulancia(z) #z = id
            self.lista_ambulancias_creadas.append(ambulancia)
            z += 1
                    

    def cargar_lista_llegadas(self):
        print("LISTA EVENTOS",self.lista_eventos[0])
        self.contador_dias = 0
        hora_primer_dia = float(0)
        for evento in self.lista_eventos:
            formato_hora = evento[2].split(":")
            hora_transformada = float(formato_hora[0])+float(formato_hora[1])/60
            hora_comparar = float(hora_transformada)
            if  hora_comparar < hora_primer_dia:
                self.contador_dias += 1
                hora_primer_dia = hora_comparar
            else:
                hora_primer_dia = hora_comparar
                obj_evento = Eventos((24*self.contador_dias) + hora_transformada, float(evento[0]), float(evento[1]), float(evento[3]), float(evento[4]), float(evento[5]))
                self.lista_de_llegadas.append(obj_evento)
        

    

    # @property
    # def proximo_llamado_termina(self):
    #     # Esta la próxima persona que terminará de ser atendida con su tiempo asociado
    #     x, y = self.tiempos_abandono[0]
    #     return x, y

    
    def proximo_evento(self):
        
        if len(self.lista_de_llegadas) == 0 and len(self.lista_de_terminos) != 0:
            #NO HAY LLEGADAS, PERO FALTAN QUE TERMINEN
            return 'retornar_evento_termino'

        elif len(self.lista_de_llegadas) != 0 and len(self.lista_de_terminos) == 0:
            #HAY LLEGADAS, TODOS TERMINARON
            return 'retornar_evento_llegada'
            
        elif len(self.lista_de_llegadas) != 0 and len(self.lista_de_terminos) != 0:
            #HAY LLEGADAS, FALTAN QUE TERMINEN
            return 'comparar'

        elif len(self.lista_de_llegadas) == 0 and len(self.lista_de_terminos) == 0 and len(self.lista_cola) != 0:
            #Eventos cola
            return 'retornar_evento_cola'
        ## 0 1
        ## 1 0
        ## 1 1
        ## 0 0

        # tiempos = [self.proximo_llamado_llega,
        #            self.proximo_llamado_termina[0]]
        # tiempo_prox_evento = min(tiempos)

        # if tiempo_prox_evento >= self.tiempo_maximo:
        #     return "fin"
        # eventos = ["llegada_llamado", "llegada_base"]
        # return eventos[tiempos.index(tiempo_prox_evento)]
    
    def run(self):
        t_inicial = time.time()
        capstone = 0
        while capstone == 0:
            string_evento = self.proximo_evento()
            # print("en el modulo hay {}".format(self.modulo_atencion))
            # if evento == "fin":
            #     self.tiempo_actual = self.tiempo_maximo
            #     break
            evento = self.manejo_listas_eventos(string_evento)
            if len(self.lista_de_llegadas) == 0 and len(self.lista_de_terminos) == 0: #and len(self.lista_cola) == 0:
                capstone = 1
                t_final = time.time()
        t_total = t_final-t_inicial
        print("TIEMPO DE SIMULACION: ", t_total, " SEGUNDOS \n")
        
            
    
    #Actualizar tiempo ??

    def tratamiento_cola(self, evento_lista): #RECIBE EVENTO DE TÉRMINO
        var_estado = False
        # print("Entró a la cola")
            # evento_lista = self.lista_cola.popleft()
        
        for evento_cola in self.lista_cola:
            hora_salida = tiempo_24_horas(evento_cola.hora_partida)
            fstring=f"Tiempo {hora_salida}" 
            id_nodo_base = evento_lista.ambulancia.base_asignada.nodo_asociado
            lista_rutas_bases =  self.dicc_base_eventos[fstring][str(evento_cola.nodo_asociado)] 
            contador = 0
            for datos_ruta in lista_rutas_bases: #TIEMPO-RUTA-ID_BASE
                # print(datos_ruta[2],"\n")
                # print(id_nodo_base)
                if datos_ruta[2] == id_nodo_base:
                    # print("Entró a las bases")
                    if datos_ruta[0] < self.PARAMETRO_UMBRAL:
                        tiempo_base_evento = datos_ruta[0]
                        # print("Entró AL UMBRAAAAAAAAAL")
                        evento_cola.ambulancia = evento_lista.ambulancia

                        evento_cola.tiempo_en_cola = self.tiempo_actual - evento_cola.tiempo_llegada
                        self.lista_tiempos_en_cola.append(evento_cola.tiempo_en_cola)
                        # evento_cola.actualizar_duracion_total()
                        self.tiempo_actual = evento_cola.tiempo_llegada + evento_cola.tiempo_en_cola  #+ evento_cola.duracion_total
                        evento_cola.tiempo_llegada = self.tiempo_actual
                        # tiene_ambulancia = self.cargar_evento_llegada(evento_cola)
                        # if tiene_ambulancia == True:

                        #MANEJO TIEMPO BASE A EVENTO

                        hora_salida_centro = tiempo_24_horas(evento_cola.tiempo_llegada + tiempo_base_evento + evento_cola.atencion) # Tiempo para poner al diccionario como KEy
                        hora_salida_centro_2 = evento_cola.tiempo_llegada + tiempo_base_evento + evento_cola.atencion #Tiempo que se suma 

                        fstring=f"Tiempo {hora_salida_centro}"
                        # if hora_salida_centro >= 24:
                        #     fstring = f"Tiempo {23}" 
                        ruta_evento_centro =  self.dicc_eventos_centros[fstring][str(evento_cola.nodo_asociado)]
                        id_centro = ruta_evento_centro[2]
                        tiempo_evento_centro = ruta_evento_centro[0]

                        hora_salida_base = tiempo_24_horas(hora_salida_centro_2 + tiempo_evento_centro + evento_cola.derivacion)
                        fstring2 = f"Tiempo {hora_salida_base}"  #hora_salida_base

                        id_nodo_base_retornar = evento_cola.ambulancia.base_asignada.nodo_asociado
                        # print(id_nodo_base_retornar,type(id_nodo_base_retornar))

                        # if hora_salida_base >= 24:
                        #     fstring2 = f"Tiempo {23}" 
                        lista_centros_bases = self.dicc_centros_bases[fstring2][str(id_centro)]  #Lista desde centro a lista de bases (primero debiese ser la que le pertenece y no las más cercana)
                        # print(evento._id, "EVENTO IDD")

                        for base in lista_centros_bases:         #Base[0]: Tiempo de la ruta
                            if base[2] == id_nodo_base_retornar: #Base[2]: base asociada a ruta centro - base
                                tiempo_centro_base = base[0]     #Base[1]: lista con los id de la ruta      
                                hora_salida_final = hora_salida_centro_2 + tiempo_evento_centro + evento_cola.derivacion
                                evento_cola.viaje_llamado = tiempo_base_evento
                                evento_cola.viaje_hospital = tiempo_evento_centro
                                evento_cola.viaje_base = tiempo_centro_base
                                # print(f"Tiempo que va al evento {evento.viaje_llamado}\nTiempo que va al Centro { evento.viaje_hospital}\nTiempo que va a la Base {evento.viaje_base} \
                                #     \nTiempo Preparacion {evento.preparacion},\nTiempo Atencion {evento.atencion},\nTiempo Derivacion {evento.derivacion},\nTiempo Llegada {evento.tiempo_llegada},\nTiempo cola {evento.tiempo_en_cola} ")
                                    
                                # print("Tiempo de Respuesta : ",evento.preparacion + evento.viaje_llamado )
                                self.lista_de_tiempos_respuesta.append(evento_cola.preparacion + evento_cola.viaje_llamado)

                                evento_cola.actualizar_duracion_total()
                                evento_cola.duracion_total = evento_cola.duracion_total - evento_cola.tiempo_en_cola 
                                # print("Duracion TOtal: ",evento_cola.duracion_total )
                                self.lista_de_duraciones.append(evento_cola.duracion_total)
                                break



                        self.lista_de_terminos.append(evento_cola)
                        var_estado = True
                        break
            if var_estado == True:
                break
        if var_estado == True:
            
            self.lista_cola.remove(evento_cola)

        elif var_estado == False:
            self.contador_ambulancia += 1
            # print("LA VARIEBLE DE ESTADO ES FALSSE")


    def manejo_listas_eventos(self, string_evento):
        
        if string_evento == "retornar_evento_termino":
                print("")
                # print(string_evento)
                evento_lista = self.lista_de_terminos.pop(0)
                self.tiempo_actual = evento_lista.tiempo_llegada + evento_lista.duracion_total
                self.lista_eventos_manejados.append(evento_lista)
                evento_lista.ambulancia.disponible = True

                # print(f"Tiempo Actual Evento Término: {self.tiempo_actual}")
                # print("Lista Llegadas",len(self.lista_de_llegadas))
                # print("Lista Términos",len(self.lista_de_terminos))
                # print("Lista Colas",len(self.lista_cola))
                # print("Lista manejados",len(self.lista_eventos_manejados),"\n")
                # print(f"El evento terminó, Tiempo Actual {self.tiempo_actual}")

                if len(self.lista_cola) != 0:
                        self.tratamiento_cola(evento_lista)

                # return algo

        # elif string_evento == "retornar_evento_cola":
            
        #     if len(self.lista_cola) != 0:
        #                 var_estado = False
        #                 # print("Entró a la cola")
        #                 evento_cola = self.lista_cola.popleft()
        #                 hora_salida = floor(evento_cola.hora_partida)
        #                 fstring=f"Tiempo {hora_salida}" 
        #                 id_nodo_base = evento_cola.ambulancia.base_asignada.nodo_asociado
        #                 lista_rutas_bases =  self.dicc_base_eventos[fstring][str(evento_cola.nodo_asociado)]

        #                 # for evento_cola in self.lista_cola:
        #                 #     hora_salida = floor(evento_cola.hora_partida)
        #                 #     fstring=f"Tiempo {hora_salida}" 
        #                 #     id_nodo_base = evento_lista.ambulancia.base_asignada.nodo_asociado
        #                 #     lista_rutas_bases =  self.dicc_base_eventos[fstring][str(evento_cola.nodo_asociado)]
        #                 for datos_ruta in lista_rutas_bases:
        #                     # print(datos_ruta[2],"\n")
        #                     # print(id_nodo_base)
                            
        #                     if datos_ruta[2] == id_nodo_base:
        #                         # print("Entró a las bases")
        #                         if datos_ruta[0] < 2:
        #                             # print("Entró AL UMBRAAAAAAAAAL")
        #                             evento_cola.ambulancia = evento_lista.ambulancia

        #                             evento_cola.tiempo_en_cola = self.tiempo_actual - evento_cola.tiempo_llegada
        #                             # evento_cola.actualizar_duracion_total()
        #                             self.tiempo_actual = evento_cola.tiempo_llegada + evento_cola.tiempo_en_cola  #+ evento_cola.duracion_total
        #                             evento_cola.tiempo_llegada = self.tiempo_actual
        #                             # tiene_ambulancia = self.cargar_evento_llegada(evento_cola)
        #                             # if tiene_ambulancia == True:
        #                             self.lista_de_terminos.append(evento_cola)
        #                             var_estado = True
        #                             break
        #                 if var_estado == True:
        #                     break
        #             if var_estado == True:
        #                 self.lista_cola.remove(evento_cola)

        elif string_evento == "retornar_evento_llegada":      ##Termino cuando la ambulancia llega a la base
                # print(string_evento)
                evento_lista = self.lista_de_llegadas.pop(0)
                self.tiempo_actual = evento_lista.tiempo_llegada
                # FUncion que completa atributos de tiempos de viaje con DIJKSTRA del evento de termino que reciba evento_lista
                tiene_ambulancia = self.cargar_evento_llegada(evento_lista)
                if tiene_ambulancia == True:
                    self.lista_de_terminos.append(evento_lista)
                
                # print(f"Tiempo Actual Evento Llegada {self.tiempo_actual}")
                # print("Lista Llegadas",len(self.lista_de_llegadas))
                # print("Lista Términos",len(self.lista_de_terminos))
                # print("Lista Colas",len(self.lista_cola))
                # print("Lista manejados",len(self.lista_eventos_manejados),"\n")
                #print(f"iNFO DEL EVENTO {evento_lista.tiempo_llegada }")

                return evento_lista
                

        elif string_evento == "comparar":      ##Termino cuando la ambulancia llega a la base
                # print(string_evento)
                min_llegada = self.lista_de_llegadas[0].tiempo_llegada
                #print(f"Tiempo Minmino llegada {min_llegada}")
                # print(f"Tiempo Actual {self.tiempo_actual}")
                

            
                self.lista_de_terminos = sorted(self.lista_de_terminos, key=segundo_elemento)
                
                min_termino = self.lista_de_terminos[0].duracion_total + self.lista_de_terminos[0].tiempo_llegada
                #print(f"Tiempo Minmino Termino {min_termino}")
                # print(f"Tiempo Actual {self.tiempo_actual}")

                if min_llegada <= min_termino:
                    
                    # print("EVENTO DE LLEGADA OCURRE PRIMERO")
                    evento_lista = self.lista_de_llegadas.pop(0) 
                    self.tiempo_actual = evento_lista.tiempo_llegada
                    evento_lista.hora_partida = self.tiempo_actual + evento_lista.preparacion
                    tiene_ambulancia = self.cargar_evento_llegada(evento_lista)
                    if tiene_ambulancia == True:
                        self.lista_de_terminos.append(evento_lista)
                    # print(f"Tiempo Actual Comparacion: Llegada primero {self.tiempo_actual}")
                    # print("Lista Llegadas",len(self.lista_de_llegadas))
                    # print("Lista Términos",len(self.lista_de_terminos))
                    # print("Lista Colas",len(self.lista_cola))
                    # print("Lista manejados",len(self.lista_eventos_manejados),"\n")

                    # FUncion que completa atributos de tiempos de viaje con DIJKSTRA del evento de termino que reciba evento_lista
                    
                    
                    return  evento_lista
                else:
                    # print("EVENTO DE TERMINO OCURRE PRIMERO")
                    evento_lista = self.lista_de_terminos.pop(0)
                    
                    # print(evento_lista.ambulancia)
                    evento_lista.ambulancia.disponible = True
                    
                    self.lista_eventos_manejados.append(evento_lista)
                    self.tiempo_actual = evento_lista.tiempo_llegada + evento_lista.duracion_total

                    # print(f"Tiempo Actual Comparacion: Término primero: {self.tiempo_actual}")
                    # print("Lista Llegadas",len(self.lista_de_llegadas))
                    # print("Lista Términos",len(self.lista_de_terminos))
                    # print("Lista Colas",len(self.lista_cola))
                    # print("Lista manejados",len(self.lista_eventos_manejados),"\n")
                    #print(f"LARGO DE COLAAAAAAAA: {len(self.lista_cola)}")

                    if len(self.lista_cola) != 0:
                        self.tratamiento_cola(evento_lista)
                                
                    #trabajar cola
                    return  evento_lista

        # Dijkstra: FUncion que completa atributos de tiempos de viaje con DIJKSTRA del evento de termino que reciba evento_lista
        # Además cuando selecciona base, se cambia atributo de las ambulancias disponibles y el atributo de disponibilidad 
        # de la ambulancia


        # self.tiempo_actual = self.proximo_llamado_llega
        # self.proximo_llamado_llega = self.tiempo_actual 
        # llamado = Llamados(self.tiempo_actual, eventos[0][0], eventos) ## FALTA RELLENAR LOS PARÁMETROS
        # ###AQUÍ LE ASIGNO LA BASE MÁS CERCANA
        
        #print("\r\r\033[91m[LLEGADA]\033[0m ha llegado un auto id: {} {}".format(auto._id,self.tiempo_actual))

    def cargar_evento_llegada(self, evento):
        hay_ambulancia = 0 #NO hay ambulancia
        id_nodo_evento = evento.nodo_asociado   #DETERMINAR TIEMPOS QUE NO TENEMOS
        hora_salida = tiempo_24_horas(evento.hora_partida)
        fstring=f"Tiempo {hora_salida}" 
        # if hora_salida >= 24:
        #         fstring = f"Tiempo {23}"

        lista_rutas_bases =  self.dicc_base_eventos[fstring][str(id_nodo_evento)]
        contador = 0
        #REVISIÓN DE BASES PARA VER AMBULANCIAS DISPONIBLES
        contador_bases = 0
        for lista in lista_rutas_bases:
            if contador_bases <= 2:
                id_base = lista[2]  #Base más cercana 
                
                for objeto_base in self.lista_bases_creadas:
                    if (objeto_base.nodo_asociado == id_base) and (objeto_base.activada == True) and hay_ambulancia != 1:
                        #distancia es mayor A: umbral

                        for ambulancia in objeto_base.lista_ambulancias_base :

                            #print(ambulancia.disponible)
                            if ambulancia.disponible == True and hay_ambulancia != 1:
                                
                                info_ruta = lista_rutas_bases[contador]
                                tiempo_base_evento = info_ruta[0]      
                                
                                if tiempo_base_evento > self.PARAMETRO_UMBRAL: #Umbral para que eliga ambulancia que se demora menos
                                    pass

                                else:
                                    # print("ALGO CON MAYÚSCULA HARTO HARTO HARTO \n \n ")
                                    hay_ambulancia = 1
                                    ambulancia_elegida = ambulancia
                                    #no_disponible
                                    ##ASIGNAR LA AMBULANCIA
                                    ambulancia_elegida.disponible = False
                                    evento.ambulancia = ambulancia
                                    # print(f"Hora que va al evento {evento.hora_partida}\n Tiempo que va al evento {tiempo_base_evento}\n Tiempo Atención {evento.atencion}")
                                    hora_salida_centro = tiempo_24_horas(evento.hora_partida + tiempo_base_evento + evento.atencion) # Tiempo para poner al diccionario como KEy
                                    hora_salida_centro_2 = evento.hora_partida + tiempo_base_evento + evento.atencion #Tiempo que se suma 
                                    # print("ID DE LA BASE QUE ENTRÓ", id_base)
                                    # print("CONTADOR", contador)
                                    break
                                
                            else:
                                pass
                    if hay_ambulancia == 1:
                        break
                    
                contador +=1
                if hay_ambulancia == 1:
                    break
            contador_bases += 1
        # print(contador)
        #LUEGO DE BUSCAR TODAS LAS AMBLANCIAS EN LAS BASES, SI NO HAY DISPONIBLES SE MANDA A LA COLA
        if hay_ambulancia == 0:
            self.lista_cola.append(evento)
            return False
            #print("UUUUUUUUUUUUUUUUUUUUUU")

        #MANEJO TIEMPOS EVENTO A CENTRO
        else:
            #ambulancia_elegida.disponible = False
            #print("COLOLCOAOLCOAS")
            fstring=f"Tiempo {hora_salida_centro}"
            # print(f"Tiempo hora salida centro {hora_salida_centro}")
            # if hora_salida_centro >= 24:
            #     fstring = f"Tiempo {23}" 
            ruta_evento_centro =  self.dicc_eventos_centros[fstring][str(id_nodo_evento)]
            id_centro = ruta_evento_centro[2]
            tiempo_evento_centro = ruta_evento_centro[0]

            hora_salida_base = tiempo_24_horas(hora_salida_centro_2 + tiempo_evento_centro + evento.derivacion)
            fstring2 = f"Tiempo {hora_salida_base}"  #hora_salida_base
            id_nodo_base_retornar = ambulancia_elegida.base_asignada.nodo_asociado
            # print(id_nodo_base_retornar,type(id_nodo_base_retornar))
            

        #MANEJO TIEMPO DESDE CENTRO HASTA DEVUELTA A LA BASE
            # if hora_salida_base >= 24:
            #     fstring2 = f"Tiempo {23}" 
            lista_centros_bases = self.dicc_centros_bases[fstring2][str(id_centro)]  #Lista desde centro a lista de bases (primero debiese ser la que le pertenece y no las más cercana)
            # print(evento._id, "EVENTO IDD")

            for base in lista_centros_bases:         #Base[0]: Tiempo de la ruta
                if base[2] == id_nodo_base_retornar: #Base[2]: base asociada a ruta centro - base
                    tiempo_centro_base = base[0]     #Base[1]: lista con los id de la ruta      
                    hora_salida_final = hora_salida_centro_2 + tiempo_evento_centro + evento.derivacion
                    evento.viaje_llamado = tiempo_base_evento
                    evento.viaje_hospital = tiempo_evento_centro
                    evento.viaje_base = tiempo_centro_base
                    # print(f"Tiempo que va al evento {evento.viaje_llamado}\nTiempo que va al Centro { evento.viaje_hospital}\nTiempo que va a la Base {evento.viaje_base} \
                    #     \nTiempo Preparacion {evento.preparacion},\nTiempo Atencion {evento.atencion},\nTiempo Derivacion {evento.derivacion},\nTiempo Llegada {evento.tiempo_llegada},\nTiempo cola {evento.tiempo_en_cola} ")
                        
                    # print("Tiempo de Respuesta : ",evento.preparacion + evento.viaje_llamado )
                    self.lista_de_tiempos_respuesta.append(evento.preparacion + evento.viaje_llamado)

                    evento.actualizar_duracion_total()
                    evento.duracion_total = evento.duracion_total - evento.tiempo_en_cola 
                    # print("Duracion TOtal: ",evento.duracion_total )
                    self.lista_de_duraciones.append(evento.duracion_total)
                    break
            return True

    def cargar_diccionarios(self):
        with open("dijkstra_final_bases_a_eventos.json") as f:
            self.dicc_base_eventos = json.load(f)
            
        with open("dijkstra_final_eventos_a_centros.json") as f:
            self.dicc_eventos_centros = json.load(f)
            
        with open("dijkstra_final_centros_a_bases.json") as f:
            self.dicc_centros_bases = json.load(f)
            
    def asociar_evento_nodo(self):
        for evento in self.lista_de_llegadas:
            evento.nodo_asociado = self.nodo_mas_cercano(evento.posicion_x, evento.posicion_y)

    def calcular_distancia(self, coordenada_x1, coordenada_y1, coordenada_x2, coordenada_y2):
        distancia = ((float(coordenada_y2) - float(coordenada_y1))**2 + (float(coordenada_x2) - float(coordenada_x1))**2)**(0.5)
        return distancia

    def nodo_mas_cercano(self, coordenada_x_evento, coordenada_y_evento):
        contador = 0
        for diccionario_nodo in self.grafo.nodes.values():            
            id_nodo = diccionario_nodo["Id"]
            coordenada_x_nodo = diccionario_nodo["Coordenada x"]
            coordenada_y_nodo = diccionario_nodo["Coordenada y"]
            distancia = self.calcular_distancia(coordenada_x_evento, coordenada_y_evento, coordenada_x_nodo, coordenada_y_nodo)
            if contador > 0:
                if distancia < distancia_minima_hasta_el_momento:
                    distancia_minima_hasta_el_momento = distancia
                    id_nodo_hasta_el_momento = id_nodo
            else:
                distancia_minima_hasta_el_momento = distancia
                id_nodo_hasta_el_momento = id_nodo
            contador += 1
        return id_nodo_hasta_el_momento
        

    def crear_grafo(self):
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
            distancia_arco = self.calcular_distancia(nodo_origen["Coordenada x"], nodo_origen["Coordenada y"], nodo_destino["Coordenada x"], nodo_destino["Coordenada y"])

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
        self.grafo = Grafo


    def recibir_evento(self):
        pass

    def llamar_base(self):
        pass


class CentrosSalud:
    def __init__(self, posicion_x, posicion_y, _id):
        self.posicion_x = posicion_x
        self.posicion_y = posicion_y
        self.id = _id
        self.nodo_ubicacion = None
        self.nodo_asociado = None
    def __repr__(self):
        return f"Hospital Nª{self.id}"

    def __getitem__(self, item):
        return item





        

# Creación entidades
# w = 0
# for base in lista_bases_creadas:  # Se llenan las bases
#     if w <= 19:
#         base.lista_ambulancias = lista_ambulancias
#         base.ocupacion = 1
#         base.ambulancia_asignada = lista_ambulancias[w]
#         lista_ambulancias[w].base_asignada = base
#         w += 1
#     else:
#         break

lista_nodos = cargar_nodos()

# Aquí podemos asignar el nodo a una base y centro hospitalario


call_center = CallCenter()
call_center.run()
# print("Lista duraciones",call_center.lista_de_duraciones)
# print(len(call_center.lista_de_duraciones))

# for evento_cola in call_center.lista_cola:
#     hora_salida = floor(evento_cola.hora_partida)
#     fstring=f"Tiempo {hora_salida}" 
#     # id_nodo_base = evento_cola.ambulancia.base_asignada.nodo_asociado
#     lista_rutas_bases =  call_center.dicc_base_eventos[fstring][str(evento_cola.nodo_asociado)]
#     print(lista_rutas_bases[0], lista_rutas_bases[1])

# for lista in call_center.lista_bases_creadas:
#     for ambulancia in lista.lista_ambulancias_base:
#         print("Estado Ambulancias",ambulancia.disponible)
# print("Contador ambulancias", call_center.contador_ambulancia)

print("Días simulados: ",call_center.contador_dias)

print(f"Tiempo Actual Evento Término: {call_center.tiempo_actual}")
print("Lista Llegadas",len(call_center.lista_de_llegadas))
print("Lista Términos",len(call_center.lista_de_terminos))
print("Lista Colas",len(call_center.lista_cola))
print("Lista manejados",len(call_center.lista_eventos_manejados))
print(f"El evento terminó, Tiempo Actual {call_center.tiempo_actual}")


my_array = np.array(call_center.lista_de_duraciones)
# print(my_array)
df = pd.DataFrame(my_array, columns = ['Duraciones'])
# print(df)
print(df.describe())

my_array1 = np.array(call_center.lista_de_tiempos_respuesta)
# print(my_array1)
df1 = pd.DataFrame(my_array1, columns = ['Tiempo de Respuesta'])
# print(df1)
print(df1.describe())

my_array2 = np.array(list(set(call_center.lista_tiempos_en_cola)))
# print(my_array2)
df2 = pd.DataFrame(my_array2, columns = ['Tiempos en Cola'])
# print(df2)
print(df2.describe())

# a = np.array(call_center.lista_tiempos_en_cola)  
# b=np.mean(a)  
# c=np.median(a)  
# # d=np.quantile(a, q = 0.1)  
# e=np.std(a)  
# print(f"PROMEDIO: {b}\nMediana: {c}\n Std: {e}")

#PLOT MEDIDAS DESEMPEÑO

# plt.plot(call_center.lista_de_duraciones) # todo el viaje
# plt.plot(call_center.lista_de_tiempos_respuesta) # preparacion + viaje a evento
# plt.show()
# plt.plot(call_center.lista_tiempos_en_cola) 
# plt.show()



# print("LLEGADAS", call_center.lista_de_llegadas)
# print("\n")
# print("LARGO LLegadas", len(call_center.lista_de_llegadas))
# print("\n")
# print(call_center.lista_de_terminos)
# print("GUARDADOS MANEJADOS", len(call_center.lista_eventos_manejados))
# print("HORA", call_center.tiempo_actual)
# print("COLA LONGITUD", len(call_center.lista_cola))
# # Medidas de desempeño
# print("NUNERIO DE ANMB", len(call_center.lista_ambulancias_creadas))
# print(call_center.lista_eventos_manejados)

tiempo_total_preparacion = 0
tiempo_total_atencion = 0
tiempo_total_derivar = 0
tiempo_total = tiempo_total_preparacion + tiempo_total_atencion + tiempo_total_derivar


# medidas desempeño sobre tiempo de colas en esta línea

## Simulacion ##

# Un for que, usando time (leemos el momento de ocurrencia de cada evento) iniciamos cada evento y
# y dejamos que itere hasta que se acaben los eventos


# contador_auxiliar = 0
# for evento in eventos:
#     thread = crear el thread
#     thread.join
#     # Actualizar medidas de desempeño

## DESPACHO DIJKSTRA_LLEGAR ATENCION DIJKSTRA_CENTRO DERIVACIÓN DIJKSTRA_BASE