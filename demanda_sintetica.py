#!/usr/bin/env python
# coding: utf-8

# In[34]:


import pandas as pd
import random as r
import time
import datetime
from datetime import date


# In[35]:
def generador_demanda_sintetica():

    df = pd.read_csv("eventos.csv",sep=";")
#####      CAMBIO DE HORA DE BASE DE DATOS
    # i = 0
    # while i<=22115:
    #     x = df.at[i,"HORARIO"]
    #     dto = datetime.datetime.strptime(x, '%H:%M')
    #     f = r.randint(-10,10)
    #     hora = datetime.timedelta(minutes=f) 
    #     final = (dto + hora).time()

        
    #     try:
    #         y = df.at[i+1,"HORARIO"] 
    #         dto_y = datetime.datetime.strptime(y, '%H:%M').time()
    #     except:
    #         pass

    #     try:
    #         z = df.at[i-1,"HORARIO"] 
    #         dto_z = datetime.datetime.strptime(z, '%H:%M').time()
    #     except:
    #         pass

        
    #     if  dto_z <= final <= dto_y:
    #     #  print(str(final))
    #     #  print(i)
            
    #         df.at[i,"HORARIO"]=(str(final))[0:5]
    #     i+=1


#####          CAMBIO TIEMPO DE DESPACHO
    i = 0
    while i<=22117:
        x = r.randint(-10,10)
        if df.at[i,"DESPACHO"] + x < 0: 
            y = r.randint(0,10)
            df.at[i,"DESPACHO"] += y
            i += 1
        else:
            df.at[i,"DESPACHO"]+=x
            i+=1



#####          CAMBIO DE TIEMPO DE ATENCION
    i = 0
    while i<=22117:
        x = r.randint(-10,10)
        if df.at[i,"ATENCION"] + x < 0: 
            y = r.randint(0,10)
            df.at[i,"ATENCION"] += y
            i += 1
        else:
            df.at[i,"ATENCION"]+=x
            i+=1




#####           CAMBIO DE TIEMPO DE DERIVACION  
    i = 0
    while i<=22117:
        x = r.randint(-10,10)
        if df.at[i,"DERIVACION"] + x < 0: 
            y = r.randint(0,10)
            df.at[i,"DERIVACION"] += y
            i += 1
        else:
            df.at[i,"DERIVACION"]+=x
  

#####           CAMBIO DE COORDENADAS
    i = 0
    while i<=22117:
        x = r.randint(-20,20)
        if df.at[i,"COORDENADA_X"] + x < 0: 
            y = r.randint(0,30)
            df.at[i,"COORDENADA_X"] += y
            i += 1
        else:
            df.at[i,"COORDENADA_X"]+=x
            i+=1
    j = 0
    while j<=22116:
        x = r.randint(-20,20)
        if df.at[j,"COORDENADA_Y"] + x < 0: 
            y = r.randint(0,30)
            df.at[j,"COORDENADA_Y"] += y
            j += 1
        else:
            df.at[j,"COORDENADA_Y"]+=x
            j+=1

    df.to_csv("demanda_sintetica.csv",sep=";")
    return "demanda_sintetica.csv"






