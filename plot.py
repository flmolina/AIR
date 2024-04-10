#Modulos y librerias a utilizar
import time
import lib.ADS1263 as ADS1263
import RPi.GPIO as GPIO
import matplotlib.pyplot as plt
import lib.classes_n_functions as clnf
import numpy as np
import threading
import time
import matplotlib.pyplot as plt
#Inicializacion de cada una de las fases
Phases=[clnf.phase(110,0.5,0,0),
        clnf.phase(110,0.5,0,0),
        clnf.phase(110,0.5,0,0)]
 
#Referencias para la conversion analogico-digital
Fs=19200
CICLOS=4          #Ciclos para muestrear y procesar
REF =4.92            #Tension de alimentacion
                  # Cambiar segun el valor medido en AVDD


N=int(Fs*(CICLOS/120))
ADC = ADS1263.ADS1263()

ADC.ADS1263_init_ADC1('ADS1263_19200SPS')
ADC.ADS1263_ConfigADC(1, 0xE)
ADC.ADS1263_SetMode(0) # 0 is singleChannel, 1 is diffChannel9




def stream(channel):
    if channel>2: #Medicion de un canal de corriente
        Ajuste_magnitud=((0.376*np.sqrt(2)/0.111))
        Ajuste_magnitud=1
    else:         #MediciÃ³n de un canal de tensiÃ³n
        lb="VRMS :"
        Ajuste_magnitud=((120*np.sqrt(2)/2.89133))
        Ajuste_magnitud=1
        
    vector=[]
    ##Inicializacion del STREAM de datos
    for i in range(0,int(N)):
        ADC_Value = ADC.ADS1263_GetAll([channel])
        data=clnf.fix_data(ADC_Value[0],REF)
        vector.append(data) 
    print(np.mean(vector))
    plt.plot(vector)
    plt.show()
