#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 29 18:56:33 2025

@author: juanpablo
"""
import pandas as pd
import numpy as np
import datetime
import os
import juliandate as jd
from datetime import datetime

# Lectura DataFrame
df = pd.read_csv('FiveMillenniumCatalogofSolarEclipses.csv', sep = ",",index_col=None)

inicio = datetime.now()
MAYA     = np.timedelta64(11960, 'D')
SAROS    = np.timedelta64(6585 , 'D') 
INEX     = np.timedelta64(10571, 'D')
TRITOS   = np.timedelta64(3986 , 'D')
METONICO = np.timedelta64(6939 , 'D') 
EXELIGMOS= np.timedelta64(19756, 'D')
d = np.timedelta64(86400, 's')

d1 = {
      "0" : 'MAYA', "1" : 'SAROS',"2" : 'INEX', "3" : 'TRITOS', "4" : 'METONICO', "5" : 'EXELIGMOS'
      }
d2 = {
      "0" : MAYA, "1" : SAROS, "2" : INEX, "3" : TRITOS, "4" : METONICO, "5" : EXELIGMOS
      }
meses = { #obtener numero de mes
    'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6,
    'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12
}

def crear_fecha_np(ano, mes, dia, tiempo="00:00:00"): #convierte el formato de fecha
    h, m, s = map(int, tiempo.split(':'))
    fecha_str = f"{ano:04d}-{mes:02d}-{dia:02d}T{h:02d}:{m:02d}:{s:02d}"
    return np.datetime64(fecha_str)

def Indice(fecha, df=df): #np.datetime64 a indice
    indice = df.index[df['GregorianDate'].values.astype('datetime64[D]') == fecha.astype('datetime64[D]')].tolist()
    return indice[0]

def ExisteFecha(fecha, margen=2, df=df): #verifica Eclipse fecha=np.datetime64() 
    resp = any(abs(df['GregorianDate'].values.astype('datetime64[D]') - fecha.astype('datetime64[D]')) <= np.timedelta64(margen, 'D'))
    if resp == True:
        indices = df.index[
        np.abs(
            df['GregorianDate'].values.astype('datetime64[D]') - np.datetime64(fecha, 'D')
        ) <= np.timedelta64(margen, 'D')
        ].tolist()
        i = int(indices[0])
    else:
        i = None
    return resp, i

def Conversion_a_Greg(ano, mes, dia, T="00:00:00"):
    if crear_fecha_np(ano, mes, dia) < crear_fecha_np(1582, 10, 15):   
        juld = jd.from_julian(ano, mes, dia)
        g = jd.to_gregorian(juld)
        f = crear_fecha_np(int(g[0]), int(g[1]), int(g[2]), T)
    else:
        f = crear_fecha_np(ano, mes, dia, T)
    return f

# Creacion Fecha formtato Gregoriano
df['GregorianDate'] = [Conversion_a_Greg(a, meses.get(m), d, t) for a,m,d,t in zip (df['Year'], df['Month'], df['Day'], df['TDofGreatestEclipse'])]
print(df)

def Deltas(df):     # Crear columna de Deltas(tipo Pandas)
    df['DeltaT'] = df['GregorianDate'].diff().astype('timedelta64[s]')
    df['DeltaT'] = df['DeltaT'].fillna(0)
Deltas(df)

def Deltas2(df):    # Crear columna de Deltas2(decimales)
    diferencias = np.diff(df['GregorianDate'].values)
    df['DeltaT2']=np.insert(diferencias.astype('timedelta64[s]').astype(float), 0, np.nan)
    df['DeltaT2']=df['DeltaT2']/86400
    df['DeltaT2'] = df['DeltaT2'].fillna(0)
Deltas2(df)

def Registro(i, df_serie, df=df):
    df_serie = pd.concat([df_serie, df.iloc[[i]]], ignore_index=True)#Agrega a la serie
    return df_serie
#%% Exporta el DF a .CSV, Carpeta
df.to_csv('datos.csv', index=False)
opciones=[MAYA, SAROS, INEX, TRITOS, METONICO, EXELIGMOS]
opciones_nombre=['MAYA', 'SAROS', 'INEX', 'TRITOS', 'METONICO', 'EXELIGMOS']

print("0 - Maya 11,960d\n" + "1 - Saros 6,585d\n" + "2 - Inex 10,571d\n"+"3 - Tritos 3,986d\n"+"4 - Metónico 6,939d\n"+"5 - Exeligmos 19,756d\n")
opcion = int(input("Elija el ciclo:"))
        
r = int(input("inicio(num de catalogo): ")) 
rf = int(input("final(num de catalogo): "))

ciclo=opciones[x:=opcion] # ELIGE EL CICLO
nomciclo=opciones_nombre[x]
carpeta = nomciclo+"-datos"
os.makedirs(carpeta, exist_ok=True)

filtro=[]
i=r
f0 = df['GregorianDate'].iloc[i]
df_serie=df
df_serie=df_serie.iloc[0:0]
#%% Ciclo
while r <= rf:
    
    pase=False  #Filtro
    while pase==False:
        if (r in filtro):
            print('esta repetido', r)
            pase==False
            r+=1
        else:
            pase=True
            
    print('SERIE: ', r)
    if r>11897:
        break
    f1 = f0 = df['GregorianDate'].iloc[r]
    i = r 
    
    for k in range (0,2): 
        if k==0:
            n = 1
        elif k==1:
            n, i, f0  = -1, i-1,f1 - ciclo
            
        continua=True
        while continua==True:
            if ExisteFecha(f0)[0]==True: #Caso A: HAY fecha
                i = ExisteFecha(f0)[1]
                df_serie=Registro(i, df_serie) #Registra eclipse en la serie
                f0 = df['GregorianDate'].iloc[i]
                continua = True
                f0=f0+n*ciclo #Fecha siguiente a buscar 
            elif ExisteFecha(f0)[0]==False: #Caso B: No hay fecha, busca par
                ultimafecha = df_serie['GregorianDate'].iloc[-1]
                i = Indice(ultimafecha)
                if abs(ultimafecha - df['GregorianDate'].iloc[i-n])/d <30: 
                    i = i-n           #Caso B.1: HAY fecha par
                    df_serie=Registro(i, df_serie)
                    f0 = df['GregorianDate'].iloc[i]
                    continua = True
                    f0=f0+n*ciclo
                else:                 #Caso B.2 No hay fecha par
                    continua = False  #
                    break             #
    
    df_serie = df_serie.sort_values('CatNum', ignore_index=True) #ordena las filas
    Deltas(df_serie)    #actualiza deltas
    Deltas2(df_serie)   #
    ruta_csv = os.path.join(carpeta, nomciclo+str(r+1)+'.csv')  #salida del archivo
    df_serie.to_csv(ruta_csv, index=False)                      #
    lista=(df_serie['CatNum']-1).tolist()   #actualiza filtro
    filtro = list(set(filtro) | set(lista)) #
    filtro.sort()                           #
    df_serie = df_serie.iloc[0:0]           #
    r+=1
#%% tiempo de ejecución
fin = datetime.now()
print(f"Duración: {fin - inicio}")



