import time
import ADS1263
import RPi.GPIO as GPIO
import matplotlib.pyplot as plt
import classes_n_functions as cnf
import matplotlib.pyplot as plt
import numpy as np
REF = 5.08          # Modify according to actual voltage
                    # external AVDD and AVSS(Default), or internal 2.5V
N=int(7200*3/60)
fig, ax = plt.subplots()
line, = ax.plot(np.random.rand(int(N)))
fig.show()

ADC = ADS1263.ADS1263()

ADC.ADS1263_init_ADC1('ADS1263_38400SPS')
    # The faster the rate, the worse the stability
    # and the need to choose a suitable digital filter(REG_MODE1)
ADC.ADS1263_ConfigADC(7, 0xF)
ADC.ADS1263_SetMode(0) # 0 is singleChannel, 1 is diffChannel9

channelList = [0] # The channel must be less than 10
vector=[]

##Inicializacion del STREAM de datos
for i in range(0,int(N)):
    ADC_Value = ADC.ADS1263_GetChannalValue(0)
    ADC_Value2 = ADC.ADS1263_GetChannalValue(1) # get ADC1 value
    if(ADC_Value>>31 ==1):
                    data=(REF*2 - ADC_Value * REF / 0x80000000)
                    #print("ADC1 IN%d = -%lf" %(i, data)) 
    else:
                    data=(ADC_Value * REF / 0x7fffffff)
                    #print("ADC1 IN%d = %lf" %(i, data))   # (32bit)
    vector.append(data) 
print("entrando al while")
while True:
    old_vector=vector
    vector=[]
    for i in range(0,int(N-10)):
        ADC_Value = ADC.ADS1263_GetChannalValue(0)# get ADC1 value
        ADC_Value2 = ADC.ADS1263_GetChannalValue(1)
        if(ADC_Value>>31 ==1):
                    data=(REF*2 - ADC_Value * REF / 0x80000000)
                    #print("ADC1 IN%d = -%lf" %(i, data)) 
        else:
                    data=(ADC_Value * REF / 0x7fffffff)
                    #print("ADC1 IN%d = %lf" %(i, data))   # (32bit)
        vector.append(data)
    vector=cnf.update(old_vector,vector)
    line.set_ydata(vector)

    fig.canvas.draw()
    fig.canvas.flush_events()
