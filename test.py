##Escrito por: Luis Fernando Molina antequera -github:flmolina
from classes_n_functions import phase, True_FFT, data_Mag, data_angle
import numpy as np
import time

##Parametros del sistema
fs=48e3 ## Frecuencia de muestreo
tstep=1/fs #Tiempo de muestreo
f0=60#Frecuencia de la señal
N=int(fs/f0)  ##Numero de muestras por porción
t = np.linspace(0,((N-1)*tstep), N*4) #Vector de tiempo 

print(N)
print (len(t))

##--------------------###
amplitud=2
angulo=2*np.pi/3

##Definicion de las señales
Voltages =[ amplitud * np.sin((2 * np.pi * f0 * t)) ,
            amplitud * np.sin((2 * np.pi * f0 * t)-angulo),
            amplitud * np.sin((2 * np.pi * f0 * t)+angulo)]


Currents = [amplitud/4 * np.sin((2 * np.pi * f0 * t)),
            amplitud/4 * np.sin((2 * np.pi * f0 * t)-angulo),
            amplitud/4 * np.sin((2 * np.pi * f0 * t)+angulo)]

inicio=time.time()

FFT_V=True_FFT(Voltages,N)
FFT_I=True_FFT(Currents,N)
final=time.time()


Fase_A=phase(V=data_Mag(FFT_V[0]) , I=data_Mag(FFT_I[0]), Theta_I=data_angle(FFT_I[0],FFT_V[0]),Theta_V=data_angle(FFT_V[0],FFT_V[0]))
Fase_B=phase(V=data_Mag(FFT_V[1]/4) , I=data_Mag(FFT_I[1]), Theta_I=data_angle(FFT_I[1],FFT_V[1]),Theta_V=data_angle(FFT_V[0],FFT_V[1]))
Fase_C=phase(V=data_Mag(FFT_V[2]) , I=data_Mag(FFT_I[2]), Theta_I=data_angle(FFT_I[2],FFT_V[2]),Theta_V=data_angle(FFT_V[0],FFT_V[2]))

print(Fase_B.mostrar_atributos())