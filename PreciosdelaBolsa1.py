#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  6 16:43:10 2021

@author: fernando
"""

#1COMO DESCARGAR LOS DATOS DE PRECIO DE UN ACTIVO FINANCIERO,EN ESTE CASO LAS ACCIONES 
#DE APPLE Y GUARDAR EL DATAFRAME

#libreria para leer dataç

import pandas_datareader.data as we 
#Libreria para acotar la fecha
import datetime as dt

#Vamos a bajar informacion de este intervalo de tiempo
#año,mes,dia 
start = dt.datetime(2015,3,1)
end = dt.datetime(2020,3,1)

#Vamos a leer la informacion de la parte de finanzas
#de yahoo, informacion sobre las acciones de apple
#Es un dataframe
df = we.DataReader('AAPL','yahoo',start,end)


#2INDICADOR DE CRUCE DE MEDIAS MOVILES (USANDO EL DATA QUE GUARDAMOS)

#Nuestras medias moviles;


#Queremos que nos vaya haciendo una media del numero de muestras 
#Media movile de 42 dias(una muestra de precio por dia)
#Desde la primera muestra min=0
df['42ma']= df['Close'].rolling(window= 42,min_periods=0).mean() #42 por que es el numero de dias que opera la bolsa en dos mese 

#En la siguiente; queremos una muestra de 252 dias(a cada muestra nos dara la media de las 252)
df['252ma']= df['Close'].rolling(window= 252,min_periods=0).mean()
#252 dias opera la bolsa en un año
#Vamos a crear una columna para identificar cuando la media movil baja
#esta por encima de la larga y viceversa. La diferencia entre ambas
df['diferencia']=df['42ma'] - df['252ma']

from numpy import where

#Regime es una columna que va alojar la señal de compra y venta
#Necesitaremos el where de la liberia numpy
#Dentro del where va la señal de compra venta
#where(condicion,valor toma el elemento cuando la condicion se cumpla,parametro que indica que no cumple la condicion)
#cuando el valor de la media movil corta este por encima del valor de la media larga, queremos que 
#nuestro programa comunique una señal de compra (compra = 1)
df['Regime'] = where(df['diferencia']>0,1,0)
#y al contrario, cuando el valor de la media movil larga este por encima del valor de la media movil corta,
#queremos que venda(venta = -1)
df['Regime'] = where(df['diferencia']<0,-1,df['Regime'])
#Cuando tengan el mismo valor nuestro programa queremos que este fuera del mercado(=0)

#Vamos a graficar el precio de cierre de la accion
#Las dos medias moviles
df[['Close','42ma','252ma']].plot(grid=True)

#Vamos a hacer una dataframe con las varaibles que nos interesan
df2 = df.filter(['Close','42ma','252ma','diferencia','Regime'])

#2.1VAMOS APRENDER A GRAFICAR VELAS (LA INTERPRETACION ESTA EN LAS NOTAS)

#Tomaremos la informacion de las acciones de Mincrosoft
#Graficaremos por dia, tambien es posible hacer grafica de velas por meses o años
start = dt.datetime(2020,6,1)
end = dt.datetime(2020,7,1)
df3 = we.DataReader('MSFT','yahoo',start,end)

#Vamos a utilizar la libreria mplfinance mac(pip install mplfinance), window(pip.exe install mplfinance)
import mplfinance as mpf
#Graficamos de la siguiente manera
#Candle es para las velas y el estilo es charles que es para que te las ponga verde y rojo
mpf.plot(df3,type='candle', style='charles',title='Microsoft daily',ylabel='Price ($)')


