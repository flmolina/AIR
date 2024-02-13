import matplotlib.pyplot as plt
import numpy as np
import pyaudio
import struct
import time
def open():
    # Configuración de la grabación
    cdef int FORMAT = pyaudio.paInt16  # Formato de audio
    cdef int CHANNELS = 1  # Número de canales (1 para mono, 2 para estéreo)
    cdef int RATE = 41000  # Tasa de muestreo (muestras por segundo)
    cdef CHUNK = 345 

    # Inicializar PyAudio
    p = pyaudio.PyAudio()

    # Abrir un stream para la entrada de audio en tiempo real
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK,
                    input_device_index=1)


    cdef bytes data
    cdef float inicio, final 
    for i in range (100000):
        inicio=time.time()
        data= stream.read(CHUNK,exception_on_overflow=False)
        data_int=struct.unpack(str(CHUNK)+"h",data)
        final=time.time()
        print(str((final-inicio)*1000))
        i+=1