#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 21 14:55:02 2024

@author: pablogonzalez
"""

#   Este programa utiliza como base de datos el archivo: GREGORIANO.csv
#   , que es el 'Five Millenium Catalog of Solar Eclipses' convertido completamente
#   a calendario gregoriano, para obtener familias de eclipses según el ciclo elegido
#   generando los archivos de salida para cada eclipse en el catálogo

import pandas as pd
import pandas as read_csv
import numpy as np
import datetime
import time
import os
import csv
from datetime import date
import juliandate as jd
from astropy.time import Time
import operator

#======= Constantes ===========
ciclo    = np.timedelta64(0,'D')
MAYA     = np.timedelta64(11960,'D')
SAROS    = np.timedelta64(6585, 'D') 
INEX     = np.timedelta64(10571, 'D')
TRITOS   = np.timedelta64(3986, 'D')
METONICO  = np.timedelta64(6939, 'D') 
EXELIGMOS   = np.timedelta64(19756, 'D') 


eclipse_1  = np.datetime64("2024-01-01")
limite_sup = np.datetime64("2100-10-19")
limite_inf = np.datetime64("0001-06-10")
margen     = np.timedelta64(1,"D")
lunacion    = np.timedelta64(30, "D")
cuatromeses = lunacion*4.
d = np.timedelta64(1,"D")

#=====FUNCIONES=======

#Función que busca una fecha en el catálogo
def BuscaFecha(fechaintro):
    fechaintro_str = str(fechaintro)
    fechaintro = fechaintro_str.rsplit("-", 2)
    anobuscado = [int(fechaintro[0])]
    mesentexto = mesAString(fechaintro[1])
    mesbuscado = [mesentexto]
    diabuscado = [int(fechaintro[2])]
    resultado = dataframe[dataframe['Year'].isin(anobuscado) & dataframe['Month'].isin(mesbuscado) & dataframe['Day'].isin(diabuscado)]
    if pd.DataFrame(resultado).empty == False :
        Existe = True
        #print(resultado[["CatNum","Year", "Month","Day"]])
    elif pd.DataFrame(resultado).empty == True :
        Existe = False
    return Existe

#Convierte el mes de 'numero' a 'nombre'
def mesAString(mes):
    mestring = str(mes)
    m = {
        '01': "Jan",
        '02': "Feb",
        '03': "Mar",
        '04': "Apr",
        '05': "May",
        '06': "Jun",
        '07': "Jul",
        '08': "Aug",
        '09': "Sep",
        '10': "Oct",
        '11': "Nov",
        '12': "Dec"
        }
    try:
        out = str(m[mestring])
    except:
        raise ValueError('No es un mes')
    return out

#Convierte el 'el mes de 'nombre' a 'numero'
def mesANumeroInt(mes):
    m = {
        'Jan': "01",
        'Feb': "02",
        'Mar': "03",
        'Apr': "04",
        'May': "05",
        'Jun': "06",
        'Jul': "07",
        'Aug': "08",
        'Sep': "09",
        'Oct': "10",
        'Nov': "11",
        'Dec': "12"
        }
    try:
        out = int(m[mes])
    except:
        raise ValueError('No es un mes')
    return out

# Funcion que toman el índice 'i' y devuelve la fecha que corresponde en el catálogo
def ObtenFecha(k):
    anodat = str(dataframe.iloc[k,2])
    mesdat = str(mesANumeroInt(dataframe.iloc[k,3])).zfill(2)
    diadat = str(dataframe.iloc[k,4]).zfill(2)
    fechada1 = np.datetime64(anodat + "-" + mesdat + "-" + diadat)
    return fechada1

# Función que introduce un índice y devuelve la fecha completa(A/M/D/h/m/s)
def FechaCompletaPorIndice(k):
    anodat = str(dataframe.iloc[k,2])
    mesdat = str(mesANumeroInt(dataframe.iloc[k,3])).zfill(2)
    diadat = str(dataframe.iloc[k,4]).zfill(2)
    horadat = str(dataframe.iloc[k,5])
    fechada1 = np.datetime64(anodat + "-" + mesdat + "-" + diadat+"T"+horadat.zfill(8))
    return fechada1

# Función que introduce una fecha y devuelve su índice del catálogo
def ObtenIndice(fecha):
    fecha_str = str(fecha)
    fecha_lista = fecha_str.rsplit("-",2)
    ano = fecha_lista[0]
    mesentexto = mesAString(fecha_lista[1])
    mes = mesentexto
    dia = fecha_lista[2]
    elemento = dataframe.index[(dataframe["Year"] == int(ano)) & (dataframe["Month"] == str(mes)) & (dataframe["Day"] == int(dia))]
    index_value = elemento[0] 
    return index_value

# Función que calcula la direncia en días de las fechas
def CalculaDiferencia(fechain, fechaultima): #obtiene A, A_ant, y resta --> obtiene la fecha actual, la ultima y la diferencia en dias(el ciclo) 
    A = FechaCompletaPorIndice(ObtenIndice(fechain)) #X
    A_ant = FechaCompletaPorIndice(ObtenIndice(fechaultima))#X
    resta = (A - A_ant)/np.timedelta64(1,"D")#X
    return resta

# Función que agrega la lista [num,date,Td,..] de información de la fecha como  una fila al DataFrame
def AgregaFecha_a_DataFrame(dfm, fechain, resta):
    dfmcatnum = dataframe.iloc[ObtenIndice(fechain),0]
    dfmdate = str(fechain)
    dfmhour = dataframe.iloc[ObtenIndice(fechain),5]
    dfmtype = dataframe.iloc[ObtenIndice(fechain),9]
    dfmdt = resta
    dfmlista = [dfmcatnum, dfmdate, dfmhour, dfmtype, dfmdt]
    dfm.loc[len(dfm)] = dfmlista
    
#Funcion que amplia el margen de busqueda a +- 2días    
def Usa_Margen(fechain, fechaultima, dfm, signo):
    MargenError = MargenError = [fechain-d*2, fechain-d, fechain+d, fechain+d*2]
    for r in MargenError:
        if BuscaFecha(r) == True:
            Margen = True
            fechain = r
            resta = CalculaDiferencia(fechain, fechaultima)
            AgregaFecha_a_DataFrame(dfm, fechain, abs(resta))
            fechaultima = fechain
            fechain = fechain + (signo*ciclo)
            break
    else:
        Margen = False         
    return fechain, fechaultima, Margen

#Funcion que busca si es diferencia Anterior o diferenciaPosterior
def Fecha_Par(DF, dif, fechaCentro, fechaX, signo):
    if dif<lunacion+d:
        resta = abs(CalculaDiferencia(fechaCentro, fechaX)) 
        fecha = fechaX
        AgregaFecha_a_DataFrame(DF, fecha, resta)
        fecha = fecha + (signo*ciclo)
        Existencia = True
    else:
        fecha = "SinFecha"
        Existencia = False
    return fecha, Existencia

#Funcion que busca el eclipse par
def Busca_EclipsePar(DF, fechaultima, signo):
    ObtenIndice(fechaultima)
    i = ObtenIndice(fechaultima)
    fechaCentro = ObtenFecha(i)
    fechaAnterior = ObtenFecha(i-1)
    fechaPosterior = ObtenFecha(i+1)
    
    difA = fechaCentro - fechaAnterior
    difP = fechaPosterior - fechaCentro
    
    DiferenciaA = Fecha_Par(DF, difA, fechaCentro, fechaAnterior,signo)
    DiferenciaP = Fecha_Par(DF, difP, fechaCentro, fechaPosterior,signo)

    if DiferenciaA[1] == True:
        fecha = DiferenciaA[0]
        Existencia = True     
    elif DiferenciaP[1]== True:
        fecha = DiferenciaP[0]
        Existencia = True
    else:
        fecha = 'SinFecha'
        Existencia = False
    return fecha, Existencia

#Función de la iteración para buscar ciclos de eclipses
def Ciclo(dfm, fechalimite, fechain, fechaultima, signo, comparacion):
    
    operador_funcion=operator.le if comparacion==True else operator.ge
    
    while operador_funcion(fechain, np.datetime64(fechalimite)):
    
        if BuscaFecha(fechain) == True: #Caso 1: Fecha encontrada
            resta = CalculaDiferencia(fechain, fechaultima)    
            AgregaFecha_a_DataFrame(dfm, fechain, abs(resta))
            fechaultima = fechain
            fechain = fechain + signo*ciclo
            
        elif BuscaFecha(fechain) == False: #Caso 2: No encontrada --> extiende margen
            resultados = Usa_Margen(fechain, fechaultima, dfm, signo)
            fechain = resultados[0]
            fechaultima = resultados[1]
            
            if resultados[2] == False: #Caso 2.1: No se encuentra con margen(busca eclipse par)
                resultado_eclipse_par = Busca_EclipsePar(dfm, fechaultima, signo)
                if resultado_eclipse_par[1] == True:
                    fechain = resultado_eclipse_par[0]
                else: #Caso 2.1.2: No se encuentra eclipse para --> Corta el ciclo      
                  break   
            else:
                pass
            
#Funcion que convierte las fechas anteriores a 1582-10-15 de calendario 
#gregoriano a calendario juliano            
def Conversion_Calendario_a_JULIANO(fecha):
    fecha_np = np.datetime64(fecha)
    f_lista = fecha.rsplit('-',2)
    if fecha_np <= np.datetime64('1582-10-15'):
        juld= jd.from_gregorian(int(f_lista[0]), int(f_lista[1]), int(f_lista[2]))
        jul = jd.to_julian(juld)
        fecha_conv=str(jul[0])+'-'+str(jul[1]).zfill(2)+'-'+str(jul[2]).zfill(2)
    else:
        fecha_conv = fecha
    return fecha_conv

#===========================================================================
                    #= DATAFRAME DE ECLIPSES =
print('\n~ IMPRESIÓN DE LAS COLUMNAS DEL CATÁLOGO''\n'
      'DE ECLIPSES ~\n')
dataframe = pd.read_csv('GREGORIANO.csv', sep = ",")
print(dataframe[["CatNum","Year", "Month","Day"]])
index = dataframe.index

#introduce la fecha en número entero# inyear = "2024"# inmonth = "04"# inday = "08"     
# fechain = np.datetime64(inyear +"-"+ inmonth + "-"+ inday)# fechainp = fechain
# print('tú fecha elegida es: ', fechain)
d1 = {
      "m" : 'MAYA', 
      "s" : 'SAROS',
      "i" : 'INEX',
      "t" : 'TRITOS',
      "o" : 'METONICO',
      "e" : 'EXELIGMOS'
}
d2 = {
      "m" : MAYA, 
      "s" : SAROS,
      "i" : INEX,
      "t" : TRITOS,
      "o" : METONICO,
      "e" : EXELIGMOS
}

print("m - Maya 11,960d\n" + "s - Saros 6,585d\n" + "i - Inex 10,571d\n"+"t - Tritos 3,986d\n"+"o - Metónico 6,939d\n"+"e - Exeligmos 19,756d\n")
opcion = input("Elija el ciclo(m,s,i,o,e...):")

for k in d1:  
    if opcion == k:
        print("Eleccion:", k)
        nomciclo = d1[k]
        print(nomciclo,"\n")          
for m in d2:
    if opcion == m:
        ciclo = d2[m]
        print("Ciclo:",ciclo)
        
pi = int(input("inicio(num de catalogo): ")) 
pf = int(input("final(num de catalogo): "))
n = 0
p = int(pi)-1 # p es el indice inicial ' i-1 ' del catalogo

opcion_salida=int(input('''\n¿En qué calendario desea las fechas de salida del archivo?:\n
    0 - Gregoriano
    1 - Juliano(fechas < 1582/oct) y Gregoriano
    '''))
listanegra = []
numeros = []
eclipses_rep =[]

for n in range (pi-1,pf):
    numeros.append(n)


while p <= int(pf)-1:    
    repetido = True
    while repetido == True:
        if p in listanegra:
            repetido = True
            p+=1
        else:
            repetido = False 
            
    #Dataframae para las fechas      
    dfm = pd.DataFrame() #crea Dataframe para las series
    dfm = pd.DataFrame(columns=['catnum', 'date', 'hour', 'type', 'deltaT'])
    fechain = ObtenFecha(p)
    fechainicial = fechain
    fechaultima = fechain
    
    #Ciclo para fechas hacia el futuro
    Ciclo(dfm, np.datetime64("3000-10-19"), fechain, fechaultima, 1, True)
          
    Existedfmp = False
    
    #Dataframae para fechas del PASADO   
    if fechainicial - ciclo >= np.datetime64("-1999-05-26"):
        fechainp = fechainicial
        fechainp = fechainp
        fechaultimap = fechainp
        dfmp = pd.DataFrame() #crea Dataframe para las familias
        dfmp = pd.DataFrame(columns=['catnum', 'date', 'hour', 'type', 'deltaT'])
        fechainp = ObtenFecha(p)
        fechainicial = fechainp
        fechaultimap = fechainp
        
        #Ciclo para fechas hacia el pasado
        Ciclo(dfmp, np.datetime64("-1999-05-26"), fechainp, fechaultimap, -1, False)
        
        dfmp = dfmp.loc[::-1].reset_index(drop=True) #ordena las fechas
        Existedfmp = True
    ind=len(dfm.index)
    
#### Filtración y salida de los datos
    
    if ind > 5: #FILTRAR FAMILIAS
    
        if Existedfmp == True:
            pasado = pd.Series(dfmp['catnum'].tolist())
            futuro = pd.Series(dfm['catnum'].tolist())
            del futuro[0]
            listaTot = pd.concat([pasado, futuro], ignore_index=True)          
            listaTotal = pd.DataFrame()
            listaTotal["catnum"] = listaTot
        else:
            listaFut = dfm[["catnum"]]      
            listaTotal = listaFut  
        lista_terminada = list(listaTotal['catnum'])
        lista_terminada_N = []
        for y in lista_terminada:
            lista_terminada_N.append(y-1)          
        for s in lista_terminada_N:
            if s in listanegra:
                repite1 = True
                eclipses_rep.append(s)
                break
            else:
                repite1 = False 
                
        #Escritura de archivos
        arc=open(nomciclo+"-familia#"+str(p+1)+".txt","w")
        if Existedfmp == True: #Agrega los elem. posteriores
            for m in range(len(dfmp.index)-1):
                fecha_escribir = str(dfmp.iloc[m,1])
                if opcion_salida==1:
                    fecha_escribir = Conversion_Calendario_a_JULIANO(fecha_escribir)
                arc.write(str(dfmp.iloc[m,0])+","+fecha_escribir+","+str(dfmp.iloc[m,2])+","+str(dfmp.iloc[m,3])+","+str(dfmp.iloc[m,4])+"\n")       
        for n in range(ind) : #Agrega Elem. anteriores
            fecha_escribir2=str(dfm.iloc[n,1])
            if opcion_salida==1:
                fecha_escribir2 = Conversion_Calendario_a_JULIANO(fecha_escribir2)
            arc.write(str(dfm.iloc[n,0])+","+fecha_escribir2+","+str(dfm.iloc[n,2])+","+str(dfm.iloc[n,3])+","+str(dfm.iloc[n,4])+"\n") 
        arc.close() 
        
    #Serie demasiado corta:
    elif ind<5 : 
        dfm = dfm[0:0]
        
    numeros_borrar = list(listaTotal['catnum'])      
    numeros_borrarN = []
    for m in numeros_borrar:
        numeros_borrarN.append(m-1)
    for x in numeros_borrarN:
        if x not in listanegra:
            listanegra.append(x)
    listanegra.sort()
    p+=1
    print(p)

print('PARES: ', eclipses_rep)



















