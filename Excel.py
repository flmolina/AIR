import matplotlib.pyplot as plt
import numpy as np
import pyaudio
import struct
# Configuración de la grabación
FORMAT = pyaudio.paInt16  # Formato de audio
CHANNELS = 1  # entrada mono // microfono
RATE = 44100  # Tasa de muestreo (muestras por segundo)
CHUNK = int(2*RATE/(120))# Número de muestras en el chunk


### (el valor a calibrar depende del puerto)
T=[(0.376/390.3), (0.376/5242.7), 1 ,1 ,1 ,1 ]

## un chunk dura CHUNK/RATE
CHUNK_TIME=CHUNK/RATE



#Inicializando y abriendo STREAM usando pyaudio

p = pyaudio.PyAudio()
Stream_1 = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK,
                input_device_index=11)




print(str("Tiempo de la ventana")+ str(CHUNK_TIME))
data= Stream_1.read(CHUNK,exception_on_overflow=False)
data_int=np.array(struct.unpack(str(CHUNK)+"h",data))  * T[1]

N_muestras=len(data_int)

Muestras_segundo=N_muestras/CHUNK_TIME

print("Numero de muestras por segundo "+ str(Muestras_segundo))


np.savetxt("array.csv", data_int, delimiter=",")

plt.plot(data_int)
plt.show()