
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
REF =4.92            #Tension de alimentacion
                  # Cambiar segun el valor medido en AVDD
Ajuste_magnitud=((0.376*np.sqrt(2))/0.19)
print(Ajuste_magnitud)
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
        data=(ADC_Value * REF / 0x7fffffff)
        #print("ADC1 IN%d = %lf" %(i, data))   # (32bit)
        vector.append(data) 

    while True:
        #inicio=time.time()
        old_vector=vector
        vector=[]
        for i in range(0,N-1) :
            ADC_Value = ADC.ADS1263_GetChannalValue(channel)# get ADC1 value
            data=(ADC_Value * REF / 0x7fffffff) * Ajuste_magnitud
            vector.append(data)
           

        vector=clnf.update(old_vector,vector)       
        FFT=clnf.True_FFT(vector,len(vector))       
        Phases[0].I=round(clnf.data_Mag(FFT,CICLOS),3)
        #final=time.time() 
        #print(str(final-inicio)*1000)
        str1=Phases[channel].mostrar_atributos
        print(("I_RMS: ")+str(round(Phases[channel].I/np.sqrt(2),3)), end='\r', flush=True)

hilo=threading.Thread(target=stream,args=[0,])



hilo.start()


hilo.join()
