#!/usr/bin/python
# -*- coding:utf-8 -*-
##INSTRUCCIONES##
#los canales del 0 al 2 corresponden a tensiones 1,2,3
#los canales del 3 al 5 corresponden a las corrientes 1,2,3
"------------------------------------------------------------------"

#Todos los parametros configurables del ADC se encuentran enel
#Archivo ADS1263.py

"--------------------------------------------------------------------"
import lib.ADS1263 as ADS1263
import time
import matplotlib.pyplot as plt
import lib.classes_n_functions as clnf
import numpy as np
N=40
REF = 5.08    
      # Modify according to actual voltage
                    # external AVDD and AVSS(Default), or internal 2.5V
ADC = ADS1263.ADS1263()
if (ADC.ADS1263_init_ADC1('ADS1263_38400SPS') == -1):
    exit()
ADC.ADS1263_SetMode(0) 
fig, ax=plt.subplots()
ax.set_ylim(-5,5)
fig.show()
lines=[]

line0,=ax.plot(np.random.rand(N))
while(1):
    
    ADC_Data=clnf.get_data(ADC,REF,N)
    line0.set_ydata(ADC_Data[3])

    fig.canvas.draw()
    fig.canvas.flush_events()


