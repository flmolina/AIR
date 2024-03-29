import tkinter as tk
import classes_n_functions as clnf
import numpy as np
import ADS1263
import threading
import time
import RPi.GPIO as GPIO
#Inicializacion de cada una de las fases
Phases=[clnf.phase(110,0.5,0,0),
        clnf.phase(110,0.5,0,0),
        clnf.phase(110,0.5,0,0)]

I_DISPARO=100
I_Ajuste=0.376 #Amperes

#Referencias para la conversion analogico-digital
Fs=19200
CICLOS=2          #Ciclos para muestrear y procesar
REF =2.5            #Tension de alimentacion
                  # Cambiar segun el valor medido en AVDD

N=int(Fs*(CICLOS/60))

#Inializacion del
ADC = ADS1263.ADS1263()
ADC.ADS1263_init_ADC1('ADS1263_19200SPS')
ADC.ADS1263_ConfigADC(7, 0xF)
ADC.ADS1263_SetMode(0) # 0 is singleChannel, 1 is diffChannel9


def actualizar_etiquetas(A,B,C,D):
    # Aquí puedes definir la lógica para actualizar el contenido de las etiquetas
    etiqueta1.config(text=A)
    etiqueta2.config(text=B)
    etiqueta3.config(text=C)
    etiqueta4.config(text=D)
def catch():
    vector=[]
    for i in range(0,int(N)):
        ADC_Value_0 = ADC.ADS1263_GetChannalValue(0)

        #ADC_Value2 = ADC.ADS1263_GetChannalValue(1) # get ADC1 value
        if(ADC_Value_0>>31 ==1):
                        data=(REF*2 - ADC_Value_0 * REF / 0x80000000)
                        #print("ADC1 IN%d = -%lf" %(i, data)) 
        else:
                        data=(ADC_Value_0 * REF / 0x7fffffff)
                        #print("ADC1 IN%d = %lf" %(i, data))   # (32bit)
        vector.append(data) 
    while True:
        old_vector=vector
        vector=[]
        for i in range(0,int(N-10)):
            ADC_Value_0 = ADC.ADS1263_GetChannalValue(0)# get ADC1 value
            #ADC_Value2 = ADC.ADS1263_GetChannalValue(1)
            if(ADC_Value_0>>31 ==1):
                        data=(REF*2 - ADC_Value_0 * REF / 0x80000000)
                        #print("ADC1 IN%d = -%lf" %(i, data)) 
            else:
                        data=(ADC_Value_0 * REF / 0x7fffffff)
                        #print("ADC1 IN%d = %lf" %(i, data))   # (32bit)
            vector.append(data)
        vector=clnf.update(old_vector,vector)       

        FFT=clnf.True_FFT(vector,len(vector))

   
       
        etiqueta1.config(text=Phases[0].mostrar_atributos())
        etiqueta2.config(text=Phases[1].mostrar_atributos())
        etiqueta3.config(text=Phases[2].mostrar_atributos())
        if Phases[0].I>I_DISPARO:
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
