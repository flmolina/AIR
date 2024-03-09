import tkinter as tk
import classes_n_functions as clnf

Phase_A=clnf.phase(120,0.5,0,0)
Phase_B=clnf.phase(120,0.5,-120,-120)
Phase_C=clnf.phase(120,0.5,120,120)


def actualizar_etiquetas(A,B,C):
    # Aquí puedes definir la lógica para actualizar el contenido de las etiquetas
    etiqueta1.config(text=A)
    etiqueta2.config(text=B)
    etiqueta3.config(text=C)


## ------------Estetica de la interfaz-------------  ##
ventana = tk.Tk()
ventana.title("Ejemplo de GUI con Tkinter")

# Establecer las dimensiones de la ventana (ancho x alto)
ancho_ventana = 1024
alto_ventana = 600
ventana.geometry(f"{ancho_ventana}x{alto_ventana}")  # Ancho: 1024 píxeles, Alto: 600 píxeles

# Configurar la rejilla para que se expanda uniformemente
for i in range(5):
    ventana.grid_rowconfigure(i, weight=1)
    ventana.grid_columnconfigure(i, weight=1)

# Crear las etiquetas
etiqueta1 = tk.Label(ventana, text="Etiqueta 1", width=20, height=5)
etiqueta2 = tk.Label(ventana, text="Etiqueta 2", width=20, height=5)
etiqueta3 = tk.Label(ventana, text="Etiqueta 3", width=20, height=5)


# Ubicar las etiquetas en la ventana
etiqueta1.grid(row=1, column=1, sticky="nsew")
etiqueta2.grid(row=1, column=2, sticky="nsew")
etiqueta3.grid(row=1, column=3, sticky="nsew")
#--------------------------------------------------------------------------#
## ------------Caracteriticas señal de audio------------  ##












#actualizar_etiquetas(Phase_A.mostrar_atributos(),Phase_B.mostrar_atributos(),Phase_C.mostrar_atributos())


# Ejecutar el bucle principal de la aplicación
ventana.mainloop()