import matplotlib.pyplot as plt
import numpy as np
import pyaudio
import struct
import time
import numpy.fft as fft
def open():
    # Configuración de la grabación
    FORMAT = pyaudio.paInt16  # Formato de audio
    CHANNELS = 1  # Número de canales (1 para mono, 2 para estéreo)
    RATE = 41000  # Tasa de muestreo (muestras por segundo)
    CHUNK = 345 # Número de muestras por bloque

    # Inicializar PyAudio
    p = pyaudio.PyAudio()

    # Abrir un stream para la entrada de audio en tiempo real
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK,
                    input_device_index=7)

    x =np.arange(0, 2*CHUNK,2)
    fig, ax= plt.subplots()
    ax.set_ylim(12000*1.1, -12000*1.1)
    x =np.arange(0, 2*CHUNK,2)
    line,=ax.plot(x,np.random.rand(CHUNK))
    fig.show()

    for i in range (1000000):
        inicio=time.time()
        data= stream.read(CHUNK,exception_on_overflow=False)
        data_int=struct.unpack(str(CHUNK)+"h",data)
        FFT=fft.fft(data_int)
        idx=np.where(np.abs(FFT)==max(np.abs(FFT)))[0]
        line.set_ydata(data_int)
        fig.canvas.draw()
        fig.canvas.flush_events()
        final=time.time()
        print(str((final-inicio)*1000))
        i+=1

open()