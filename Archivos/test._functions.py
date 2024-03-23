##Escrito por: Luis Fernando Molina antequera -github:flmolina
from classes_n_functions import phase, True_FFT, data_Mag, data_angle, True_FFT_phase
import numpy as np
import time
import matplotlib.pyplot as plt
##Parametros del sistema
fs=48e3 ## Frecuencia de muestreo
tstep=1/fs #Tiempo de muestreo
f0=60#Frecuencia de la señal
CICLOS=4
N=int(fs/f0)*CICLOS ##Numero de muestras por porción

t = np.linspace(0,((N-1)*tstep), N) #Vector de tiempo 

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

FFT_V=True_FFT_phase(Voltages,N)
FFT_I=True_FFT_phase(Currents,N)
final=time.time()


Fase_A=phase(V=data_Mag(FFT_V[0],CICLOS) , I=data_Mag(FFT_I[0],CICLOS), 
            Theta_I=data_angle(FFT_I[0],FFT_V[0],CICLOS),Theta_V=data_angle(FFT_V[0],FFT_V[0],CICLOS))
Fase_B=phase(V=data_Mag(FFT_V[1],CICLOS) , I=data_Mag(FFT_I[1],CICLOS), 
            Theta_I=data_angle(FFT_I[1],FFT_V[1],CICLOS),Theta_V=data_angle(FFT_V[0],FFT_V[1],CICLOS))
Fase_C=phase(V=data_Mag(FFT_V[2],CICLOS) , I=data_Mag(FFT_I[2],CICLOS), 
            Theta_I=data_angle(FFT_I[2],FFT_V[2],CICLOS),Theta_V=data_angle(FFT_V[0],FFT_V[2],CICLOS))

print(Fase_C.mostrar_atributos())

plt.plot(t, Voltages[0] )
plt.show()
plt.stem(abs(FFT_V[2]))
plt.show()