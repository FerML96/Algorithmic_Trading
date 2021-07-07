#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  6 21:32:18 2021

@author: fernando
"""

import matplotlib.pyplot as plt
from numpy import where
import pandas_datareader.data as we
import datetime as dt
import mplfinance as mpf

start = dt.datetime(2020,3,1)
end = dt.datetime(2020,9,19)

df = we.DataReader('GDL','yahoo',start,end)
df['ma'] = df['Close'].rolling(window = 10, min_periods=0).mean()

mc = mpf.make_marketcolors(up = 'tab:green',down='tab:red', wick={'up':'green','down':'red'})

s = mpf.make_mpf_style(base_mpl_style= "seaborn",mavcolors=["orange"],marketcolors=mc)

mpf.plot(df,type='candle',style=s,mav=10,title='GLD')


#AHORA VAMOS A APLICAR UNA ESTRATEGIA DE REGRESION A LA MEDIA PARA EL REGIMEN CICLICO
#DE ACUERDO AL HISTORICO SABEMOS QUE ESTA ESTRATEGIA ES ADECUADA PARA EL ORO (GDL)

startt = dt.datetime(2000,10,1)
endd = dt.datetime(2020,10,1)
data = we.DataReader('GDL','yahoo',startt,endd)
data['price']= data['Adj Close']

#Nuestra media movil de 25 dias:
SMA = 25

#Estamos haciendo la columna que nos guarde la media 
data['SMA'] = data['price'].rolling(window=SMA).mean()
#El valor de la distancia del precio respecto a la media movil sera la desviacion standar
#Creamos una columna que nos guarde el valor de la media standar
N =1#Como parametro del sistema, vamos a tomar el numero de desviaciones standar
# de distancia que le estamos exigiendo al sistema puede ser 1 o 2 N=1
data['STD'] = N*data['price'].rolling(window=SMA).std()

#Agregamos dos columnas una con la suma de SMA+STD y la otraa con la diferencia SMA-STD
#Estas son las distancias
data['SMA+STD'] = data['SMA']+ data['STD']
data['SMA-STD'] = data['SMA']- data['STD']

#Vamos a graficar el precio de nuestro instrumento en azul, junto con las ultimas dos columnas 
#que son las distancias
#Si se supera la linea verde se entrara en corto(esta por encima de la media movil)
#Si se supera la linea roja por debajo por lo que entraremos en largo 
plt.style.use('seaborn')
data[['price','SMA+STD','SMA-STD']].plot(figsize=(10,6))

#Ahora vamos a programar las señales para que entre en corto o largo
data['position'] = where(data['price'] > data['SMA+STD'],-1,0)
data['position'] = where(data['price'] < data['SMA+STD'],1,data['position'])

data['position'] = data['price'].fillna(0)

#Por ultimo veremos el rendimiento que nos da esta estrategia
#en un periodo seleccionado
data['returns'] = data['price']/data['price'].shift(1)
data['strategy'] = data['returns'] ** data['position'].shift(1)
data[['returns','strategy']].dropna().cumprod().plot(figsize=(10,6))


