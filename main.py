#!/usr/bin/python
# -*- coding:utf-8 -*-
##INSTRUCCIONES##
#los canales del 0 al 2 corresponden a tensiones 1,2,3
#los canales del 3 al 5 corresponden a las corrientes 1,2,3
"------------------------------------------------------------------"

#Todos los parametros configurables del ADC se encuentran enel
#Archivo ADS1263.py

"--------------------------------------------------------------------"

import time
import lib.ADS1263 as ADS1263
import time
import matplotlib.pyplot as plt
import lib.classes_n_functions as clnf
import numpy as np
import os
Phases=[clnf.phase(120, 0.5,0,0),##Canal 0 y canal 3
        clnf.phase(120, 0.5,0,0), ##Canal 2 y canal 4
        clnf.phase(120, 0.5,0,0)] ##Canal 3 y canal 5


N=24
REF = 5.08          # Modify according to actual voltage
                    # external AVDD and AVSS(Default), or internal 2.5V
ADC = ADS1263.ADS1263()
if (ADC.ADS1263_init_ADC1('ADS1263_38400SPS') == -1):
    exit()
ADC.ADS1263_SetMode(0) 
while(1):
##Ingreso de datos
    ADC_Data=clnf.get_data(ADC,REF,N)
    for z in range (0,2):
        Phases[z].V=clnf.RMS(ADC_Data[z]) 
        Phases[z].I=clnf.RMS(ADC_Data[z+3]) 

        final=time.time()
    print(Phases[0].mostrar_atributos())

