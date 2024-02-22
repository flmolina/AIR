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
f0=60 #Frecuencia fundamental 
N=int(fs/f0)  ##Numero de muestras por porción



# Inicializar PyAudio
p = pyaudio.PyAudio()

# Abrir un stream para la entrada de audio en tiempo real
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=fs,
                input=True,
                frames_per_buffer=N,
                input_device_index=1)

fig, ax= plt.subplots()
ax.set_ylim(0,10000)
ax.set_xlim(0,100)
x=np.arange(0,int(N/2+1),1)

line,=ax.plot(x,np.random.rand(int(N/2+1)))
fig.show()
while True:
    data= stream.read(N,exception_on_overflow=False)
    data_int= struct.unpack(str(N)+"h",data)

    FFT=cnf.True_FFT(data_int,N)
    print(cnf.data_Mag(FFT))
    line.set_ydata(abs(FFT))
    fig.canvas.draw()
    fig.canvas.flush_events()