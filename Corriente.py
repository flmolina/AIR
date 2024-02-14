import matplotlib.pyplot as plt
import numpy as np
import pyaudio
import struct
# Configuración de la grabación
FORMAT = pyaudio.paInt16  # Formato de audio
CHANNELS = 1  # entrada mono // microfono
RATE = 48000  # Tasa de muestreo (muestras por segundo)
CHUNK = int(1024)# Número de muestras en el chunk


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




fig, ax= plt.subplots()
#ax.set_ylim(-1.1,1.1 )
x =np.arange(0, 2*CHUNK,2)
window=np.linspace(0, CHUNK_TIME,CHUNK)
line,=ax.plot(window,np.random.rand(CHUNK))
ax.set_ylim(-2,2)
label_RMS=ax.text(0.5,1.01,"",transform=ax.transAxes, ha="center")
label_PICO=ax.text(0.5,1.05,"",transform=ax.transAxes, ha="center")
ax.set_ylabel("Amplitude [Volts]")
ax.set_xlabel("Time (secs)")

fig.show()

def Catch():
    a=int(100000e25)
    ##Bucle implementado para optimizacion de animacion
    for i in range (0,a,1):
        data= Stream_1.read(CHUNK,exception_on_overflow=False)
        data_int=np.array(struct.unpack(str(CHUNK)+"h",data))  * T[1]
        line.set_ydata(data_int)
    
        print (i)
        fig.canvas.draw()
        fig.canvas.flush_events()

        RMS=np.sqrt(np.mean(np.square(data_int)))
        label_RMS.set_text("Corriente RMS primario  {}".format(round(RMS,4))+str(" Amperes"))
        label_PICO.set_text("Corriente PICO-PICO primario {}".format(round(max(data_int),3))+str(" Amperes"))

Catch()
