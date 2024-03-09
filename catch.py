
import matplotlib.pyplot as plt
import numpy as np
import pyaudio
import struct
import classes_n_functions as cnf

# Configuración de la grabación
FORMAT = pyaudio.paInt16  # Formato de audio
CHANNELS = 1  # Número de canales (1 para mono, 2 para estéreo)
fs = 48000  # Tasa de muestreo (muestras por segundo)
N = 1024*2 # Número de muestras por bloque


##Parametros del sistema
tstep=1/fs #Tiempo de muestreo
f0=3600 #Frecuencia fundamental 
N=int(fs/f0)  #Factor de ajuste para la FFT
print (N)


# Inicializar PyAudio
p = pyaudio.PyAudio()

# Abrir un stream para la entrada de audio en tiempo real
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=fs,
                input=True,
                frames_per_buffer=int(N * 10), ##numero de muestras para procesar
                input_device_index=1)

while True:
    data= stream.read(N,exception_on_overflow=False)
    data_int= struct.unpack(str(N)+"h",data)

    FFT=cnf.True_FFT(data_int,N)
    print(cnf.data_Mag(FFT))
