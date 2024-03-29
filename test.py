
#Modulos y librerias a utilizar
import time
import ADS1263
import RPi.GPIO as GPIO
import matplotlib.pyplot as plt
import classes_n_functions as clnf
import numpy as np
import threading
import time
#Inicializacion de cada una de las fases
Phases=[clnf.phase(110,0.5,0,0),
        clnf.phase(110,0.5,0,0),
        clnf.phase(110,0.5,0,0)]
 
#Referencias para la conversion analogico-digital
Fs=19200
CICLOS=3          #Ciclos para muestrear y procesar
REF =5            #Tension de alimentacion
                  # Cambiar segun el valor medido en AVDD
Ajuste_magnitud=9.125
N=int(Fs*(CICLOS/120))
ADC = ADS1263.ADS1263()

ADC.ADS1263_init_ADC1('ADS1263_19200SPS')
ADC.ADS1263_ConfigADC(7, 0xE)
ADC.ADS1263_SetMode(0) # 0 is singleChannel, 1 is diffChannel9

channelList = [0] # The channel must be less than 10
def stream(channel):
    vector=[]
    ##Inicializacion del STREAM de datos
    for i in range(0,int(N)):
        
        ADC_Value = ADC.ADS1263_GetChannalValue(channel)
        if(ADC_Value>>31 ==1):
            data=(ADC_Value * REF / 0x80000000 )
            
            
        else:
            pass
            data=(ADC_Value * REF /0x7fffffff)
        vector.append(data)
    plt.plot(vector)
    plt.show()
        

                        
              
stream(0)


