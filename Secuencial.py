import matplotlib.pyplot as plt
import numpy as np
import pyaudio
import struct
from multiprocessing import Process
import time

IDX1=11 ##Tarjeta de audio 1
IDX2=12 ##Tarjeta de audio 2
#el valor a calibrar depende del puerto 
T=[(0.376/390.3), (0.376/5242.7), 1 ,1 ,1 ,1 ] #Constantes para calibracion de la medida


def catch():  # Dev_idx es el index del dispositivo a utilizar

    FORMAT = pyaudio.paInt16  # Formato de audio
    CHANNELS = 1  # entrada mono // microfono
    RATE = 48000  # Tasa de muestreo (muestras por segundo)
    CHUNK = int(1024*8)# Número de muestras en el chunk
    # Configuración de la grabación
    ## un chunk dura CHUNK/RATE
    CHUNK_TIME=CHUNK/RATE
    p = pyaudio.PyAudio()
    Stream_1 = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK,
                    input_device_index=11)
    
    Stream_2=   p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK,
                    input_device_index=12)
    
    #Ajuste general grafica
    fig, ax= plt.subplots()
    x =np.arange(0, 2*CHUNK,2)
    window=np.linspace(0, CHUNK_TIME,CHUNK)
    line,=ax.plot(window,np.random.rand(CHUNK))
    line2,=ax.plot(window,np.random.rand(CHUNK),color="red")
    label_RMS1=ax.text(0.5,1.01,"",transform=ax.transAxes, ha="center")
    ax.set_ylabel("Amplitude [A]")
    ax.set_xlabel("Time (secs)")
    
    fig.show()
    
    while True:
        #Adquisicion y procesado de las entradas de audio
        data= Stream_1.read(CHUNK,exception_on_overflow=False)
        data2=Stream_2.read(CHUNK,exception_on_overflow=False)
        data_int= np.array(struct.unpack(str(CHUNK)+"h",data)) *T[1]
        data_int2=np.array(struct.unpack(str(CHUNK)+"h",data2))*T[0]
        ##Ajuste grafica 
    
        RMS1=np.sqrt(np.mean(np.square(data_int)))
        line.set_ydata(data_int)
        line2.set_ydata(data_int2)
        label_RMS1.set_text("Valor RMS {}".format(RMS1))
     
        ##Bucle implementado para optimizacion de animacion
        fig.canvas.draw()
        fig.canvas.flush_events()

     

catch()
            


