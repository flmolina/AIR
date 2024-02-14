import matplotlib.pyplot as plt
import numpy as np
import pyaudio
import struct
from multiprocessing import Process
import time

IDX1=11 ##USB Audio 1
IDX2=12 ##USB Audio 2


def Proceso():
    #Inicializando y abriendo STREAM usando pyaudio
    def catch(Dev_idx):  # Dev_idx es el index del dispositivo a utilizar

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
                        input_device_index=Dev_idx)

        #Ajuste general grafica
        fig, ax= plt.subplots()
        ax.set_ylim(12000*1.1, -12000*1.1)
        x =np.arange(0, 2*CHUNK,2)
        window=np.linspace(0, CHUNK_TIME,CHUNK)
        line,=ax.plot(window,np.random.rand(CHUNK))
        label_RMS1=ax.text(0.5,1.01,"",transform=ax.transAxes, ha="center")
        ax.set_ylabel("Amplitude [A]")
        ax.set_xlabel("Time (secs)")
        
        fig.show()


        
        while True:
            #Adquisicion y procesado de las entradas de audio
            data= Stream_1.read(CHUNK,exception_on_overflow=False)
            data_int= np.array(struct.unpack(str(CHUNK)+"h",data))



            ##Ajuste grafica 
        
            RMS1=np.sqrt(np.mean(np.square(data_int)))
            line.set_ydata(data_int)
            label_RMS1.set_text("Valor RMS {}".format(RMS1))
         


            ##Bucle implementado para optimizacion de animacion
            fig.canvas.draw()
            fig.canvas.flush_events()

     


            



    ##Implementacion de los hilos de procesamiento 
    HILO_1=Process(target=catch, args=(IDX1,))
    HILO_2=Process(target=catch, args=(IDX2,))


    HILO_2.start()
    ##-------------------------------------------------------------------##
    print("Iniciando segundo proceso")
    time.sleep(0.5) # tiempo de espera para que cada stream pueda empezar
    ##-------------------------------------------------------------------#
    HILO_1.start()

    HILO_1.join()
    HILO_2.join()


Proceso()