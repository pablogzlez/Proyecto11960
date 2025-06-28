#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 30 00:57:13 2025

@author: pablogonzalez
"""
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patheffects as mpe
import pandas as pd
import math
from matplotlib.pyplot import plot, savefig

#Progama que genera espirales de ciclo de eclipses y grafíca eclipses lunares y solares
#de la base de datos del Five Millennium

Maya     = 11960
Saros    = 6585 
Inex     = 10572
Exeligmos= 19756
Metonico = 6939
sec_dresde = [177, 177, 148,
              177, 177, 177, 178, 177, 177, 177, 177, 177, 148,
              178, 177, 177, 177, 177, 148,
              177, 177, 177, 178, 177, 177, 148,
              177, 177, 178, 177, 177, 177, 177, 177, 177, 148,
              178, 177, 177, 177, 177, 148,
              177, 177, 177, 177, 177, 177, 148,
              177, 177, 178, 177, 177, 177, 177, 177, 148,
              177, 178, 177, 177, 177, 177, 148,
              177, 177, 177, 177
              ]
sec_anti = [29, 177, 148, 29, 177, 148, 29, 148, 29, 148, 177,
            177, 177, 148, 29, 177, 148, 29, 148, 29, 148, 177,
            177, 177, 148, 29, 177, 148, 29, 148, 177, 177, 177,
            177, 148, 29, 177, 148, 29, 148, 177, 177, 177, 177,
            148, 29, 148, 29, 148, 29, 148
            ]
sigma = ['Σ', 'Σ', 'Σ', 'Σ', 'Σ', 'Σ', 'Σ', 'Σ', 'Σ', 'Σ', 'Σ', 'Σ', 'Σ', 'Σ', 'Σ', 'Σ', 'Σ', 'Σ', 'Σ', 'Σ', 'Σ', 'Σ', 'Σ', 'Σ', 'Σ', 'Σ', 'Σ', 'Σ', 'Σ', 'Σ', 'Σ', 'Σ', 'Σ', 'Σ', 'Σ', 'Σ', 'Σ', 'Σ', 'Σ']
sigma_orden=[2, 8, 14, 20, 26, 32, 37, 43, 49, 55, 61, 67, 73, 79, 84, 90, 96, 102, 108, 114, 120, 125, 126, 131, 137, 143, 149, 155, 161, 167, 172, 178, 184, 190, 196, 202, 208, 214, 219]

helios=['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H']
helios_orden=[8, 13, 25, 31, 37, 43, 55, 60, 72, 78, 84, 90, 102, 107, 119, 125, 137, 154, 166, 172, 178, 184, 201, 207, 213, 219]

d1 = {
      "m" : 'Maya', 
      "s": 'Saros',
      "i" : 'Inex',
      "e" : 'Exeligmos',
      "o" : 'Metónico'
}
d2 = {
      "m" : Maya, 
      "s" : Saros,
      "i" : Inex,
      "e" : Exeligmos,
      "o" : Metonico
}
rotar_90 = input('¿Rotar 90° izquierda? (s/n): ').lower() == 's'
invertir_espejo = input('¿Invertir en espejo? (s/n): ').lower() == 's'
catalogo = input('¿Gráficar del catálogo? (s/n): ').lower() == 's'
if catalogo == True:
    solares = input('¿Gráficar SOLARES? (s/n): ').lower() == 's'
    lunares = input('¿Gráficar LUNARES? (s/n): ').lower() == 's'
else:
    secuencia = input('¿Gráficar secuencia Antikythera o Dresde? (a/d/n): ')
    glifos_resp = input('¿Gráficar secuencia Antikythera? (s/n): ').lower() == 's'
    
print("m - Maya 11,960d\n" + "s - Saros 6,585d\n" + "i - Inex 10,571d\n"+"e - Exeligmos 19,756d")
opcion = input("Elija el ciclo(m,s,i...):")
for k in d1:  
    if opcion == k:
        print("Elección:", k)
        nomciclo = d1[k]
        print(nomciclo,"\n")          
for m in d2:
    if opcion == m:
        ciclo = d2[m]
        print("Ciclo:",ciclo)      
ajuste = 0
if opcion == 'm':
    ciclo = 11960
    ciclo0 = ciclo
    ajuste = 0.012
    ruedas = 5
    lun0=405
    lun = 405
    LINEWIDTH=19
    LINEBORDER = 2
elif opcion == 's':
    ciclo =  6615
    ciclo0 = ciclo
    ajuste = 0.018
    ruedas = 4
    lun0=223
    lun = 224
    LINEWIDTH=20.5
    LINEBORDER = 2
elif opcion == 'i':
    ciclo = 10631
    ciclo0 = ciclo
    ajuste = 0.014
    ruedas = 5
    lun0=358
    lun = 360   
    LINEWIDTH=18.9
    LINEBORDER = 2
elif opcion == 'e':
    ciclo = 19785
    ciclo0 = ciclo
    ajuste = 0.0074
    ruedas = 5
    lun0=669
    lun = 670 
    LINEWIDTH=18.75
    LINEBORDER = 2.5
elif opcion == 'o':
    ciclo = 6939
    ciclo0 = ciclo
    ajuste = 0.02
    ruedas = 5
    lun0= 235
    lun = 235
    LINEWIDTH=19
    LINEBORDER = 2

if catalogo==True:
    if solares==True:
        df= pd.read_csv('FiveMillenniumCSolar-Deltas.txt', sep = ",",  names=['Catnum', 'Date', 'Td','Delta', 'Type'])
        print(df)
        fivemlista= df['Delta'].tolist()
        leyenda = ''
        tipos = df['Type'].tolist()    
    if lunares==True:
        dfl= pd.read_csv('FiveMillenniumCLunar-Deltas.txt', sep = ",",  names=['Catnum', 'Date', 'Td','Delta', 'Type'])
        print(dfl)
        fivemlistal= dfl['Delta'].tolist()
        tiposl = dfl['Type'].tolist()
else:
    if secuencia=='a':
        sec = sec_anti
        leyenda = 'Secuencia del Antikythera'
        color='purple'
    if secuencia=='d':
        sec = sec_dresde
        leyenda = 'Secuencia del Dresde'
        color='purple' 
        
CAPSTYLE="projecting"

# PARAMETROS fijos#
nv = 7
vuelta = ciclo

fig = plt.figure(figsize=(9, 9))
ax = fig.add_subplot(projection = "polar")
fullt = np.linspace(nv, nv+ruedas, vuelta)
theta = 2 * np.pi * fullt
ax.plot(theta, fullt, lw=LINEWIDTH, dashes=[vuelta,0.00], color='white',
        path_effects=[mpe.Stroke(linewidth=LINEWIDTH+LINEBORDER, foreground='black'), mpe.Normal()])

print ('Ruedas: ', ruedas)
print ('tu espiral completa: ', ciclo)

#DIVISION SEGMENTOS ===
alpha = 360./(lun/ruedas)
rlinea = math.radians(0) 
nl = 0
    
while rlinea < math.radians(360):   
    ax.vlines(rlinea, (nv-0.5)+nl*ajuste, (nv-0.5+ruedas)+nl*ajuste, colors='black', zorder=3, linewidth = 0.5, linestyle='solid' )
    rlinea =  rlinea + math.radians(alpha)
    nl+=1

# Parámetros base (ajustados a mi espiral original)
theta_fine = np.linspace(nv * 2 * np.pi, (nv + ruedas) * 2 * np.pi, vuelta)  # Ángulo fino
r_fine = theta_fine / (2 * np.pi)  # Radio convertido de 'fullt' a 'r'

# Graficar la espiral como línea delgada
ax.plot(theta_fine, r_fine, lw=.0,color='gray', label='Espiral de línea fina', zorder=5)

# introducir la lista de las fechas de los eclipses:
def posicion_a_theta(n, total_puntos=ciclo0):
    theta_inicio =  nv*2*np.pi
    theta_final = (nv+ruedas)*2*np.pi
    return theta_inicio + (n / total_puntos) * (theta_final - theta_inicio)

#Grafica los dias en la espiral: n es un valor en dias
def graficar_punto(n, color, size, label, offset=(0, 0)):
    theta = posicion_a_theta(n)
    r = theta / (2*np.pi)
    ax.scatter([theta], [r], color=color, s=size, label=label, zorder=5)
    if label is not None:
        ax.annotate(
            label,
            xy=(theta, r),
            xytext=(offset[0], offset[1]),  # Desplazamiento (dx, dy)
            textcoords="offset points", 
            fontsize=13,
            color=color
            )
    return theta, r

# Función para graficar puntos y añadir texto
def graficar_punto_con_etiqueta(n, color, size, label):
    theta = nv*2*np.pi + (n / ciclo0) * ((nv+ruedas)*2*np.pi - nv*2*np.pi)
    r = theta / (2*np.pi)
    ax.scatter([theta], [r], color=color, s=size, zorder=5)
    if label is not None:
        ax.annotate(
            label,
            xy=(theta, r),
            xytext=(theta + 0.05, r + 0.05),  # Posición del texto
            arrowprops=dict(arrowstyle='->', color=color),
            fontsize=12
            )     
print(ciclo0)

def GraficarCatalogo(ajustar, fivemlista, color, tipos):
    #Grafica de eclipses del catálogo
    suma = ajustar #días entre eclipses solares y lunares
    n = int(input('ingrese numero de eclipse: ')) #n es numero de eclipse
    x = 0 # x es el Delta de tiempo
    while suma <= ciclo0:
        graficar_punto(suma, color, size=22, label=tipos[n-1])
        n=n+1
        x = fivemlista[n-1]
        suma = x + suma
        
if catalogo==True:
    if solares==True:
        GraficarCatalogo(0, fivemlista, 'red', tipos)
    if lunares==True:
        GraficarCatalogo(15, fivemlistal, 'blue', tiposl)
        
elif secuencia=='d':
    nota="""Secuencia del Dresde"""
    #ciclo para las secuencias    
    sumad=0
    n=0
    x=0
    while sumad <=ciclo0:
        if n==0:
            pass
        else:
            graficar_punto(sumad, color, size=25, label=None)
        print(sumad, n, x)
        n=n+1
        if n <= 69:
            x = sec[n-1]
            sumad = x + sumad
        else:
            break
        
elif secuencia=='a':
    nota="""Secuencia del Antikythera"""
    #ciclo para las secuencias    
    i=0
    j=0
    n=0
    m=0
    for i in sigma_orden:
        graficar_punto(i*29.53-14.765, color='blue',size=0, label=sigma[n], offset=(0, 0))
        n=n+1
    for j in helios_orden:
        graficar_punto(j*29.53-14.765, color='red', size=0, label=helios[m], offset=(0, -8))
        m=m+1 

        
# para corroborar espirales
# for p in range(0,lun0+1):
#     graficar_punto(p*29.53, color, size=10, label=str(p),color='blue')
    
graficar_punto_con_etiqueta(0, color='black', size=10, label='0d')
graficar_punto_con_etiqueta(ciclo0, color='black', size=10, label=f'{ciclo0}d')  

# Aplicar transformaciones (agregado)
if rotar_90:
    ax.set_theta_offset(np.pi/2)  # Rota 90° a la izquierda
if invertir_espejo:
    ax.set_theta_direction(-1)    # Invierte dirección (espejo)

legend = nota

# Mostrar leyenda con estilo de cuadro
plt.text(0.5, 13.5, legend, 
         ha='left', va='top',
         bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5'))

#Salida de archivos
plt.title(label=f"{nomciclo}",fontsize=15)
#plt.title(label=f"{nomciclo}: {tipoec}\n",fontsize=15)
plt.grid(True)
plt.savefig('Espiral.png', format = 'png', transparent=True, dpi=400)





