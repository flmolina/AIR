import tkinter as tk
import lib.classes_n_functions as clnf
import numpy as np
import lib.ADS1263 as ADS1263
import threading
import time
import RPi.GPIO as GPIO
#Inicializacion de cada una de las fases
Phases=[clnf.phase(110,0.5),
        clnf.phase(110,0.5),
        clnf.phase(110,0.5)]

I_DISPARO=100
I_Ajuste=0.376 #Amperes
T_Ajuste=120 #Volts

N=24
REF = 5.08          # Modify according to actual voltage
                    # external AVDD and AVSS(Default), or internal 2.5V
ADC = ADS1263.ADS1263()
if (ADC.ADS1263_init_ADC1('ADS1263_38400SPS') == -1):
    exit()
ADC.ADS1263_SetMode(0) 

def actualizar_etiquetas(A,B,C,D):
    # Aquí puedes definir la lógica para actualizar el contenido de las etiquetas
    etiqueta1.config(text=A)
    etiqueta2.config(text=B)
    etiqueta3.config(text=C)
    etiqueta4.config(text=D)
def catch():
    while(1):
        ADC_Data=clnf.get_data(ADC,REF,N)
        for z in range (0,3):
            Phases[z].V=clnf.RMS(ADC_Data[z]) 
            Phases[z].I=clnf.RMS(ADC_Data[z+3]) 
            Phases[z].S=Phases[z].V*Phases[z].I
            Phases[z].Z=Phases[z].V/Phases[z].I
        etiqueta1.config(text=Phases[0].mostrar_atributos())
        etiqueta2.config(text=Phases[1].mostrar_atributos())
        etiqueta3.config(text=Phases[2].mostrar_atributos())
        if Phases[0].V<100:
                etiqueta4.config(text="FALLA")
        else:
                etiqueta4.config(text="NO FALLA")



## ------------Estetica de la interfaz-------------  ##
ventana = tk.Tk()
ventana.title("AIR")
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
