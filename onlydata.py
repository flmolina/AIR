import matplotlib.pyplot as plt
import numpy as np
import pyaudio
import struct
# Configuración de la grabación
FORMAT = pyaudio.paInt16  # Formato de audio
CHANNELS = 1  # entrada mono // microfono
RATE = 48000  # Tasa de muestreo (muestras por segundo)
CHUNK = int(1024*2)# Número de muestras en el chunk


### (el valor a calibrar depende del puerto)
T=[(0.376/390.3), (0.376/5242.7), 1 ,1 ,1 ,1 ]

## un chunk dura CHUNK/RATE
CHUNK_TIME=CHUNK/RATE
print(CHUNK_TIME)


#Inicializando y abriendo STREAM usando pyaudio

p = pyaudio.PyAudio()
Stream_1 = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK,
                input_device_index=12)



def Catch():
    a=int(100000e25)
    ##Bucle implementado para optimizacion de animacion
    for i in range (0,a,1):
        data= Stream_1.read(CHUNK,exception_on_overflow=False)
        data_int=np.array(struct.unpack(str(CHUNK)+"h",data))  * T[0]
        RMS=np.sqrt(np.mean(np.square(data_int)))
        print(RMS)


Catch()