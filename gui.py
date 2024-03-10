import tkinter as tk
import classes_n_functions as clnf
import numpy as np
import pyaudio
import struct
import threading
import time

Phase_A=clnf.phase(110,0.5,0,0)
Phase_B=clnf.phase(110,0.5,-120,-120)
Phase_C=clnf.phase(110,0.5,120,120)

I_DISPARO=100


def actualizar_etiquetas(A,B,C,D):
    # Aquí puedes definir la lógica para actualizar el contenido de las etiquetas
    etiqueta1.config(text=A)
    etiqueta2.config(text=B)
    etiqueta3.config(text=C)
    etiqueta4.config(text=D)
def catch():
    global Phase_A
    FORMAT = pyaudio.paInt16  # Formato de audio
    CHANNELS = 1  # Número de canales (1 para mono, 2 para estéreo)
    fs = 48000  # Tasa de muestreo (muestras por segundo)
    ##Parametros del sistema
    tstep=1/fs #Tiempo de muestreo
    f0=60 #Frecuencia fundamental 
    CICLOS=4
    N=int(fs/f0) * CICLOS #Numero de muestras
    # Inicializar PyAudio
    p = pyaudio.PyAudio()
    # Abrir un stream para la entrada de audio en tiempo real
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=fs,
                    input=True,
                    frames_per_buffer=N, ##numero de muestras para procesar (tiempo procesado)
                    input_device_index=1)
    while True:
        inicio=time.time()
        data= stream.read(N,exception_on_overflow=False)
        data_int= struct.unpack(str(N)+"h",data)
        FFT=clnf.True_FFT(data_int,N)

        Phase_A.I=round(clnf.data_Mag(FFT,CICLOS),3)
       
        etiqueta1.config(text=Phase_A.mostrar_atributos())
        etiqueta2.config(text=Phase_B.mostrar_atributos())
        etiqueta3.config(text=Phase_C.mostrar_atributos())
        if Phase_A.I>I_DISPARO:
            etiqueta4.config(text="FALLA")
        else:
            etiqueta4.config(text="NO FALLA")
        final=time.time()

        #print((final-inicio)*1000)



## ------------Estetica de la interfaz-------------  ##
ventana = tk.Tk()
ventana.title("Ejemplo de GUI con Tkinter")
ventana.configure(bg="#5585D1")
# Establecer las dimensiones de la ventana (ancho x alto)
ancho_ventana = 1024
alto_ventana = 600
ventana.geometry(f"{ancho_ventana}x{alto_ventana}")  # Ancho: 1024 píxeles, Alto: 600 píxeles

# Configurar la rejilla para que se expanda uniformemente


for i in range(5):
    ventana.grid_rowconfigure(i, weight=1)
    ventana.grid_columnconfigure(i, weight=1)

# Crear las etiquetas
font_style = ("FixedSys", 20)  # Cambiar la fuente y el tamaño aquí
etiqueta1 = tk.Label(ventana, text="Etiqueta 1", font=font_style, width=20, height=5)
etiqueta2 = tk.Label(ventana, text="Etiqueta 2", font=font_style, width=20, height=5)
etiqueta3 = tk.Label(ventana, text="Etiqueta 3", font=font_style, width=20, height=5)
etiqueta4= tk.Label(ventana, text="Etiqueta 3", font=font_style, width=20, height=5)


# Ubicar las etiquetas en la ventana
etiqueta1.grid(row=1, column=1, sticky="nsew")
etiqueta2.grid(row=1, column=2, sticky="nsew")
etiqueta3.grid(row=1, column=3, sticky="nsew")
etiqueta4.grid(row=2, column=2, sticky="nsew")
#--------------------------------------------------------------------------#
## ------------Operacion señales------------  ##

thread=threading.Thread(target=catch)
thread.daemon=True
thread.start()


ventana.mainloop()



#actualizar_etiquetas(Phase_A.mostrar_atributos(),Phase_B.mostrar_atributos(),Phase_C.mostrar_atributos())


# Ejecutar el bucle principal de la aplicación
