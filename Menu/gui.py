
from pathlib import Path
from tkinter import Tk, Canvas, Button, PhotoImage,Toplevel,Label,ttk,messagebox
import datetime
import pandas as pd
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("assets/frame0")
import lib.classes_n_functions as clnf
import lib.config
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
I_Medidor=[1.992, 4.634,2.126]
I_Rele=[0.18,0.43,0.2]
V_Medidor=[127.44,121.54,124.75]
V_Rele=[0.71, 0.72, 0.8]
N=24
REF = 5.08          # Modify according to actual voltage
                    # external AVDD and AVSS(Default), or internal 2.5V
#inicialización del ADC
ADC = ADS1263.ADS1263()
if (ADC.ADS1263_init_ADC1('ADS1263_38400SPS') == -1):
    exit()
ADC.ADS1263_SetMode(0) 

def registrar_evento(Date,Time, IA,IB,IC,VA,VB,VC):
    df=pd.DataFrame(pd.read_excel(relative_to_assets("Events.xlsx"),index_col=False))
    df = df.drop(columns=['Unnamed: 0'])
    nueva_fila = ["Trigger",Date, Time, VA, VB, VC, IA, IB, IC]
    df.loc[len(df)] = nueva_fila
    df.to_excel(relative_to_assets("Events.xlsx"),index_label=False)

def borrar_eventos():
    df=pd.DataFrame(pd.read_excel(relative_to_assets("Events.xlsx"),index_col=False))
    df = df.drop(columns=['Unnamed: 0'])
    df=df.iloc[[0]]
    df.to_excel(relative_to_assets("Events.xlsx"),index_label=False)

def cerrar_procesos(ventana):
        ventana.destroy()
        mostrar_ventana(window)

"CONFIGURACIÓN DE LA VENTANA PHASORS"
"----------------------------------------------"
def phasor_window():
    ocultar_ventana(window)
    import threading
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    import random
    import time
    def actualizar_etiqueta_atributos(A,B,C,D,E,F,G,H,I,J,K,L):
            textos=[A,B,C,D,E,F,G,H,I,J,K,L]
            for i in range(0,12):
                    nuevo_texto = textos[i]
                    Labels[i].config(text=str(nuevo_texto))

    def catch_fasor():
         while(1):
            ADC_Data=clnf.get_data(ADC,REF,N)
            FFT=clnf.True_FFT_phase(ADC_Data,24)
            A=np.round(clnf.data_Mag(FFT[0],3) * (V_Medidor[0]/V_Rele[0]),2)  
            B=np.round(clnf.data_Mag(FFT[1],3) * (V_Medidor[1]/V_Rele[1]),2)  
            C=np.round(clnf.data_Mag(FFT[2],3) * (V_Medidor[2]/V_Rele[2]),2) 
            D=np.round(clnf.data_Mag(FFT[3],3) * (I_Medidor[0]/I_Rele[0]),2)
            E=np.round(clnf.data_Mag(FFT[4],3) * (I_Medidor[1]/I_Rele[1]),2) 
            F=np.round(clnf.data_Mag(FFT[5],3) * (I_Medidor[2]/I_Rele[2]),2) 
            G=np.round(clnf.data_angle(FFT[0],FFT[0],3),1)
            H=(np.round(clnf.data_angle(FFT[0],FFT[1],3)- 7,1)) 
            I=(np.round(clnf.data_angle(FFT[0],FFT[2],3)-14,1)) 
            J=np.round(clnf.data_angle(FFT[0],FFT[3],3),1)
            K=(np.round(clnf.data_angle(FFT[0],FFT[4],3)-7,1)) 
            L=(np.round(clnf.data_angle(FFT[0],FFT[5],3)-13,1))
            Angulos=[G,H,I,J,K,L]
            global Angulos_globales
            Angulos_globales=Angulos
            actualizar_etiqueta_atributos(A,B,C,D,E,F,G,H,I,J,K,L)
                #actualizar_grafica(G,H,I,J,K,L)
    # Función para graficar un fasor en coordenadas polares con una flecha
    def graficar_fasor_polar_arrow(ax, angulo, color):
        magnitud = 1  # Magnitud fija
        ax.plot([angulo], [magnitud], color=color)
        ax.annotate('', xy=(angulo, magnitud), xytext=(0, 0),
                     arrowprops=dict(facecolor=color, shrink=0.005,width=1.8,headwidth=7))

    # Función para graficar los fasores
    def graficar_fasores(ax,angulos_grados):
        ax.clear()
        ax.set_theta_direction(1)  # Sentido horarioc
        #ax.set_theta_zero_location('N')  # Norte arriba

        # Convertir ángulos de grados a radianes
        angulos_radianes = np.radians(angulos_grados)

        # Colores de los fasores


        # Graficar cada fasor con una flecha
        for i, angulo in enumerate(angulos_radianes):


            graficar_fasor_polar_arrow(ax, angulo, colores[i])
        canvas.draw()
        canvas.flush_events()

    colores = ['k','r','c' ,'y', 'b','g','m']
    # Función para actualizar los ángulos y la gráfica
    def actualizar_grafica():
        while(1):
                print("graficando")    
                global Angulos_globales
                angulos_grados=Angulos_globales
                #graficar_fasores(ax, angulos_grados)
                time.sleep(3)
    def close_window():
        proc=0
        global proceso
        proceso=proc
        cerrar_procesos(window_fasor)
        
    
        

    window_fasor = Toplevel()
    proceso=1
    window_fasor.geometry("1024x600")
    window_fasor.configure(bg = "#212E4D")
    canvas = Canvas(
        window_fasor,
        bg = "#212E4D",
        height = 600,
        width = 1024,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )

    canvas.place(x = 0, y = 0)
    canvas.create_rectangle(
        39.0,
        60.0,
        985.0,
        540.0,
        fill="#D9D9D9",
        outline="")

    canvas.create_text(
        39.0,
        24.0,
        anchor="nw",
        text="Phasor",
        fill="#D9D9D9",
        font=("Inter", 30 * -1)
    )

    canvas.create_text(
        641.0,
        113.0,
        anchor="nw",
        text="VA",
        fill="#000000",
        font=("Inter Bold", 30 * -1)
    )

    canvas.create_text(
        793.0,
        114.0,
        anchor="nw",
        text="V",
        fill="#000000",
        font=("Inter Bold", 30 * -1)
    )

    canvas.create_text(
        789.0,
        443.0,
        anchor="nw",
        text="A",
        fill="#000000",
        font=("Inter Bold", 30 * -1)
    )

    canvas.create_text(
        790.0,
        376.0,
        anchor="nw",
        text="A",
        fill="#000000",
        font=("Inter Bold", 30 * -1)
    )

    canvas.create_text(
        791.0,
        309.0,
        anchor="nw",
        text="A",
        fill="#000000",
        font=("Inter Bold", 30 * -1)
    )

    canvas.create_text(
        793.0,
        181.0,
        anchor="nw",
        text="V",
        fill="#000000",
        font=("Inter Bold", 30 * -1)
    )

    canvas.create_text(
        792.0,
        243.0,
        anchor="nw",
        text="V",
        fill="#000000",
        font=("Inter Bold", 30 * -1)
    )

    canvas.create_text(
        939.0,
        114.0,
        anchor="nw",
        text="°",
        fill="#000000",
        font=("Inter Bold", 30 * -1)
    )

    canvas.create_text(
        935.0,
        443.0,
        anchor="nw",
        text="°",
        fill="#000000",
        font=("Inter Bold", 30 * -1)
    )

    canvas.create_text(
        936.0,
        376.0,
        anchor="nw",
        text="°",
        fill="#000000",
        font=("Inter Bold", 30 * -1)
    )

    canvas.create_text(
        937.0,
        309.0,
        anchor="nw",
        text="°",
        fill="#000000",
        font=("Inter Bold", 30 * -1)
    )

    canvas.create_text(
        939.0,
        181.0,
        anchor="nw",
        text="°",
        fill="#000000",
        font=("Inter Bold", 30 * -1)
    )

    canvas.create_text(
        938.0,
        243.0,
        anchor="nw",
        text="°",
        fill="#000000",
        font=("Inter Bold", 30 * -1)
    )

    canvas.create_text(
        641.0,
        180.0,
        anchor="nw",
        text="VB",
        fill="#000000",
        font=("Inter Bold", 30 * -1)
    )

    canvas.create_text(
        640.0,
        242.0,
        anchor="nw",
        text="VC",
        fill="#000000",
        font=("Inter Bold", 30 * -1)
    )

    canvas.create_text(
        639.0,
        307.0,
        anchor="nw",
        text="IA",
        fill="#000000",
        font=("Inter Bold", 30 * -1)
    )

    canvas.create_text(
        641.0,
        372.0,
        anchor="nw",
        text="IB",
        fill="#000000",
        font=("Inter Bold", 30 * -1)
    )

    canvas.create_text(
        641.0,
        439.0,
        anchor="nw",
        text="IC",
        fill="#000000",
        font=("Inter Bold", 30 * -1)
    )

    canvas.create_rectangle(
        0.0,
        60.0,
        91.0,
        540.0,
        fill="#E8CA2A",
        outline="")

    button_image_1 = PhotoImage(
        file=relative_to_assets("back.png"))
    button_1 = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        master=window_fasor,
        command=lambda: close_window(),
        relief="flat"
    )
    button_1.place(
        x=0.0,
        y=60.0,
        width=91.0,
        height=91.0
    )

    canvas.create_rectangle(
        538.5,
        59.499969482421875,
        539.0000000000002,
        540.0374755859375,
        fill="#000000",
        outline="")

    canvas.create_rectangle(
        584.0,
        110.0,
        624.0,
        143.0,
        fill="#000000",
        outline="")

    canvas.create_rectangle(
        584.0,
        439.0,
        624.0,
        472.0,
        fill="#21F100",
        outline="")

    canvas.create_rectangle(
        584.0,
        372.0,
        624.0,
        405.0,
        fill="#1650D9",
        outline="")

    canvas.create_rectangle(
        584.0,
        305.0,
        624.0,
        338.0,
        fill="#E8CA2A",
        outline="")

    canvas.create_rectangle(
        584.0,
        239.0,
        624.0,
        272.0,
        fill="#1DBB9E",
        outline="")

    canvas.create_rectangle(
        584.0,
        177.0,
        624.0,
        210.0,
        fill="#CD0000",
        outline="")

    canvas.create_rectangle(
        92.0,
        60.0,
        570.0,
        540.0,
        fill="#FFFFFF",
        outline="")


    ##Labels de magnitud en RMS
    label_font = font=("Inter Light", 25 * -1)
    label_0 =Label(canvas, text=str(100.25),font=label_font,bg="#D9D9D9")##VA
    label_id_0 = canvas.create_window(740, 130, window=label_0, anchor="center")

    label_1 =Label(canvas, text=str(100.25),font=label_font,bg="#D9D9D9")##VB
    label_id_1 = canvas.create_window(740, 196, window=label_1, anchor="center")

    label_2 =Label(canvas, text=str(100.25),font=label_font,bg="#D9D9D9")##VC
    label_id_2 = canvas.create_window(740, 262, window=label_2, anchor="center")

    label_3 =Label(canvas, text=str(100.25),font=label_font,bg="#D9D9D9")##IA
    label_id_3 = canvas.create_window(740, 328, window=label_3, anchor="center")

    label_4 =Label(canvas, text=str(100.25),font=label_font,bg="#D9D9D9")##IB
    label_id_4 = canvas.create_window(740, 394, window=label_4, anchor="center")

    label_5 =Label(canvas, text=str(100.25),font=label_font,bg="#D9D9D9")##IC
    label_id_5 = canvas.create_window(740, 460, window=label_5, anchor="center")

    ##Labels de Angulos
    label_6 =Label(canvas, text=str(120.22),font=label_font,bg="#D9D9D9")##VA
    label_id_6 = canvas.create_window(895, 130, window=label_6, anchor="center")

    label_7 =Label(canvas, text=str(120.22),font=label_font,bg="#D9D9D9")##VB
    label_id_7 = canvas.create_window(895, 196, window=label_7, anchor="center")

    label_8 =Label(canvas, text=str(120.22),font=label_font,bg="#D9D9D9")##VC
    label_id_8 = canvas.create_window(895, 262 , window=label_8, anchor="center")

    label_9 =Label(canvas, text=str(120.22),font=label_font,bg="#D9D9D9")##IA
    label_id_9 = canvas.create_window(895,  328, window=label_9, anchor="center")

    label_10=Label(canvas, text=str(120.22),font=label_font,bg="#D9D9D9")##IB
    label_id_10 = canvas.create_window(895,  394, window=label_10, anchor="center")

    label_11=Label(canvas, text=str(120.22),font=label_font,bg="#D9D9D9")##IB
    label_id_11 = canvas.create_window(895,  460, window=label_11, anchor="center")

    Labels= [label_0,label_1,label_2,label_3,label_4,label_5,label_6,label_7,
             label_8,label_9,label_10,label_11]


    
    x_pos, y_pos = 50, 50
    width, height = 400, 400
    # Crear el gráfico dentro de un rectángulo de dimensiones específicas
    fig = plt.figure(figsize=(6, 6))  # Ajustar el tamaño de la figura aquí
    ax = fig.add_subplot(111, polar=True)
    canvas = FigureCanvasTkAgg(fig, master=window_fasor)
    canvas.get_tk_widget().place(x=120, y=100, width=width, height=height)

    # Inicializar la gráfica con ángulos aleatorios
    angulos_iniciales = np.random.randint(0, 360, size=4)
    graficar_fasores(ax, angulos_iniciales)


    thread_catch_fasor=threading.Thread(target=catch_fasor)
    thread_catch_fasor.daemon=True

    thread_phasors=threading.Thread(target=actualizar_grafica)
    thread_phasors.daemon=True

    thread_catch_fasor.start()
    time.sleep(1)
    thread_phasors.start()
    window_fasor.protocol("WM_DELETE_WINDOW", close_window)
    window_fasor.resizable(False, False)
    window_fasor.mainloop()



"CONFIGURACIÓN DE LA VENTANA EVENTS"
"---------------------------------------------------------------------------------------------------"
def Events_window():
    df = pd.DataFrame(pd.read_excel(relative_to_assets("Events.xlsx")))
    df = df.drop(columns=['Unnamed: 0'])
    df=df.iloc[::-1]
    ocultar_ventana(window)
    Events_window = Toplevel()
    Events_window.geometry("1024x600")
    Events_window.configure(bg="#212E4D")

    canvas = Canvas(
        Events_window,
        bg="#212E4D",
        height=600,
        width=1024,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )
    canvas.place(x=0, y=0)

    # Mantener los elementos del código original
    canvas.create_rectangle(
        39.0,
        60.0,
        985.0,
        540.0,
        fill="#D9D9D9",
        outline=""
    )

    canvas.create_text(
        39.0,
        24.0,
        anchor="nw",
        text="Events",
        fill="#D9D9D9",
        font=("Inter Light", 30 * -1)
    )

    canvas.create_rectangle(
        0.0,
        60.0,
        91.0,
        540.0,
        fill="#E8CA2A",
        outline=""
    )

    button_back_events_image = PhotoImage(
        file=relative_to_assets("back.png"))
    button_back_events = Button(
        image=button_back_events_image,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: cerrar_procesos(Events_window),
        master=Events_window,
        relief="flat"
    )
    button_back_events.place(
        x=0.0,
        y=60.0,
        width=91.0,
        height=91.0
    )

    button_trash_image = PhotoImage(
        file=relative_to_assets("Trash.png"))
    button_trash = Button(
        image=button_trash_image,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: borrar_eventos() & cerrar_procesos(Events_window),
        master=Events_window,
        relief="flat"
    )
    button_trash.place(
        x=0.0,
        y=445.0,
        width=91.0,
        height=91.0
    )

    # Función para cargar el DataFrame en un Treeview
    def load_dataframe(tree, dataframe):
        tree["columns"] = list(dataframe.columns)
        tree.heading("#0", text="Índice", anchor="w")
        for column in dataframe.columns:
            tree.heading(column, text=column, anchor="w")
        for i, row in dataframe.iterrows():
            tree.insert("", "end", text=i, values=list(row))

    # Crear Treeview
    tree_view = ttk.Treeview(Events_window, style="Custom.Treeview")

    tree_view.place(x=90, y=60, width=895, height=480)

    # Definir estilo para el Treeview
    style = ttk.Style()
    style.configure("Custom.Treeview", font=("Inter Light", 15 * -1))

    # Cargar DataFrame en el Treeview
    load_dataframe(tree_view, df)

    # Ajustar tamaño de columnas
    for column in df.columns:
        tree_view.column(column, width=100, anchor="center")

    # Ajustar estilo de fuente y tamaño para los encabezados y elementos
    style.configure("Custom.Treeview.Heading", font=("Arial", 12, "bold"))
    style.configure("Custom.Treeview.Row", font=("Arial", 12))

    # Ajustar otros estilos
    style.map("Custom.Treeview", background=[("selected", "#0078D7")])
    style.map("Custom.Treeview", foreground=[("selected", "white")])

    # Bloquear la edición del Treeview
    tree_view["show"] = "headings"
    tree_view.bind("<Button-1>", lambda event: tree_view.focus_set())
    tree_view.bind("<Key>", lambda event: "break")

    Events_window.resizable(False, False)
    Events_window.mainloop()


".................................................................................................."

"CONFIGURACIÓN DE LA VENTANA RMS"
"--------------------------------------------------------------------------------------------------"
def RMS_window():
    ocultar_ventana(window)
    import random
    import threading

        
    def actualizar_fecha_hora():
    # Obtener la fecha y hora actual
        fecha_hora_actual = datetime.datetime.now()

    # Actualizar el contenido del Label con la fecha y hora actual
        label_fecha_hora.config(text=fecha_hora_actual.strftime("%Y-%m-%d // %H:%M:%S"))

    # Programar la próxima actualización después de 1000 milisegundos (1 segundo)
        window_RMS.after(1000, actualizar_fecha_hora)
        
    def actualizar_etiqueta_atributos(A,B,C,D,E,F):
        textos=[A,B,C,D,E,F]
        for i in range(0,6):
                nuevo_texto = textos[i]
                if i <3:
                    Labels[i].config(text=str(nuevo_texto)+str( " V"))
                else:
                    Labels[i].config(text=str(nuevo_texto)+str( " A"))

    def catch():
         while(1):
            ADC_Data=clnf.get_data(ADC,REF,N)
            FFT=clnf.True_FFT_phase(ADC_Data,24)
            A=np.round(clnf.data_Mag(FFT[0],3) *(V_Medidor[0]/V_Rele[0]),2)  
            B=np.round(clnf.data_Mag(FFT[1],3) *(V_Medidor[1]/V_Rele[1]),2)  
            C=np.round(clnf.data_Mag(FFT[2],3) *(V_Medidor[2]/V_Rele[2]),2) 
            D=np.round(clnf.data_Mag(FFT[3],3) *(I_Medidor[0]/I_Rele[0]),2)
            E=np.round(clnf.data_Mag(FFT[4],3) *(I_Medidor[1]/I_Rele[1]),2) 
            F=np.round(clnf.data_Mag(FFT[5],3) *(I_Medidor[2]/I_Rele[2]),2) 
            G=np.round(clnf.data_angle(FFT[0],FFT[0],3),1)
            H=np.round(clnf.data_angle(FFT[0],FFT[1],3),1)
            I=np.round(clnf.data_angle(FFT[0],FFT[2],3),1)
            J=np.round(clnf.data_angle(FFT[0],FFT[3],3),1)
            K=np.round(clnf.data_angle(FFT[0],FFT[4],3),1)
            L=np.round(clnf.data_angle(FFT[0],FFT[5],3),1)

            actualizar_etiqueta_atributos(A,B,C,D,E,F)
            if E>7:
                #1. enviar señal de disparo
                ADC.trigger()
                #2 registrar evento
                label_Falla.config(text="Falla")
                registrar_evento((datetime.datetime.now().strftime("%Y-%m-%d")),
                                 (datetime.datetime.now().strftime("%H:%M:%S")),
                                  A,B,C,D,E,F)
                #3:Aviso
                messagebox.showinfo("Alert", "Fault Detected")
                cerrar_procesos(window_RMS)
                
            else:
                ADC.close()
                label_Falla.config(text="Normal")
    window_RMS = Toplevel()
    window_RMS.geometry("1024x600")
    window_RMS.overrideredirect(False)
    window_RMS.configure(bg = "#212E4D")

    label_font = font=("Inter Light", 30 * -1)
    canvas = Canvas(
        window_RMS,
        bg = "#212E4D",
        height = 600,
        width = 1024,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )

    canvas.place(x = 0, y = 0)
    canvas.create_rectangle(
        39.0,
        60.0,
        985.0,
        540.0,
        fill="#D9D9D9",
        outline="")

    canvas.create_rectangle(
        91.0,
        222.0,
        985.0,
        374.0,
        fill="#BECDDA",
        outline="")

    canvas.create_text(
        39.0,
        24.0,
        anchor="nw",
        text="RMS Value",
        fill="#D9D9D9",
        font=("Inter Light", 30 * -1)
    )

    canvas.create_text(
        156.0,
        113.0,
        anchor="nw",
        text="IA",
        fill="#212E4D",
        font=("Inter Bold", 50 * -1)
    )

    canvas.create_text(
        156.0,
        270.0,
        anchor="nw",
        text="IB",
        fill="#212E4D",
        font=("Inter Bold", 50 * -1)
    )

    canvas.create_text(
        156.0,
        443.0,
        anchor="nw",
        text="IC",
        fill="#212E4D",
        font=("Inter Bold", 50 * -1)
    )

    canvas.create_text(
        600.0,
        113.0,
        anchor="nw",
        text="VA",
        fill="#212E4D",
        font=("Inter Bold", 50 * -1)
    )

    canvas.create_text(
        600.0,
        270.0,
        anchor="nw",
        text="VB",
        fill="#212E4D",
        font=("Inter Bold", 50 * -1)
    )

    canvas.create_text(
        600.0,
        443.0,
        anchor="nw",
        text="VC",
        fill="#212E4D",
        font=("Inter Bold", 50 * -1)
    )

    canvas.create_rectangle(
        509.0,
        57.0,
        512.0,
        540.0,
        fill="#000000",
        outline="")



    canvas.create_rectangle(
        0.0,
        60.0,
        91.0,
        540.0,
        fill="#E8CA2A",
        outline="")

    back_image = PhotoImage(
        file=relative_to_assets("back.png"))
    back_button = Button(window_RMS,
        image=back_image,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: cerrar_procesos(window_RMS),
        relief="flat"
    )
    back_button.place(
        x=0.0,
        y=60.0,
        width=91.0,
        height=91.0
    )

    canvas.create_rectangle(
        235.0,
        107.0,
        444.0,
        174.0,
        fill="#D9D9D9",
        outline="")

    canvas.create_rectangle(
        704.0,
        107.0,
        913.0,
        174.0,
        fill="#D9D9D9",
        outline="")

    canvas.create_rectangle(
        235.0,
        443.0,
        444.0,
        510.0,
        fill="#D9D9D9",
        outline="")

    label_0 =Label(canvas, text=str(0.0)+str(" [V]"),font=label_font,bg="#D9D9D9")
    label_id_0 = canvas.create_window(775, 144, window=label_0, anchor="center")

    label_1 =Label(canvas, text=str(0.0)+str(" [V]"),font=label_font,bg="#BECDDA")
    label_id_1 = canvas.create_window(775, 300, window=label_1, anchor="center")

    label_2=Label(canvas, text=str(0.0)+str(" [V]"),font=label_font,bg="#D9D9D9")
    label_id_2 = canvas.create_window(775, 474, window=label_2, anchor="center")

    label_3 =Label(canvas, text=str(0.0)+str(" [A]"),font=label_font,bg="#D9D9D9")
    label_id_3 = canvas.create_window(300, 144, window=label_3, anchor="center")

    label_4 =Label(canvas, text=str(0.0)+str(" [A]"),font=label_font,bg="#BECDDA")
    label_id_4 = canvas.create_window(300, 300, window=label_4, anchor="center")

    label_5 =Label(canvas, text=str(0.0)+str(" [A]"),font=label_font,bg="#D9D9D9")
    label_id_5 = canvas.create_window(300, 474, window=label_5, anchor="center")

    Labels=[label_0,label_1,label_2,label_3,label_4,label_5]
    canvas.create_rectangle(
        700.0,
        443.0,
        909.0,
        510.0,
        fill="#D9D9D9",
        outline="")
    canvas.create_text(
    700,
    564.0,
    anchor="nw",
    text="Estado:",
    fill="#D9D9D9",
    font=("Inter Light", 30 * -1)
    )
    canvas.create_rectangle(
        241.0,
        264.0,
        450.0,
        331.0,
        fill="#BECDDA",
        outline="")

    canvas.create_rectangle(
        704.0,
        265.0,
        913.0,
        332.0,
        fill="#BECDDA",
        outline="")

    label_fecha_hora = Label(window_RMS, 
                         font=label_font,
                         bg="#212E4D",
                         fg="#D9D9D9",)

    label_fecha_hora.place(x=675,y=18)

    label_Falla = Label(window_RMS, 
                         font=label_font,
                         bg="#212E4D",
                         fg="#D9D9D9",)                        
    label_Falla.place(x=800,y=560)
    actualizar_fecha_hora()
    window.resizable(False, False)
    thread=threading.Thread(target=catch)
    thread.daemon=True
    thread.start()
    window_RMS.resizable(False, False)
    window_RMS.mainloop()

"--------------------------------------------------------------------------------------------------"


"CONFIGURACIÓN DE LA VENTANA PRINCIPAL"
def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def mostrar_ventana(ventana):
    ventana.deiconify()  # Mostrar la ventana

def ocultar_ventana(ventana):
    ventana.withdraw() 
window = Tk()


def actualizar_fecha_hora():
    # Obtener la fecha y hora actual
    fecha_hora_actual = datetime.datetime.now()

    # Actualizar el contenido del Label con la fecha y hora actual
    label_fecha_hora.config(text=fecha_hora_actual.strftime("%Y-%m-%d // %H:%M:%S"))

    # Programar la próxima actualización después de 1000 milisegundos (1 segundo)
    window.after(1000, actualizar_fecha_hora)

window.geometry("1024x600")
window.configure(bg = "#212E4D")


canvas = Canvas(
    window,
    bg = "#212E4D",
    height = 600,
    width = 1024,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
canvas.create_rectangle(
    39.0,
    60.0,
    985.0,
    540.0,
    fill="#D9D9D9",
    outline="")

canvas.create_text(
    39.0,
    24.0,
    anchor="nw",
    text="Artificial Intelligence Relay  ",
    fill="#D9D9D9",
    font=("Inter Light", 30 * -1)
)

canvas.create_text(
    39.0,
    564.0,
    anchor="nw",
    text="Select an option",
    fill="#D9D9D9",
    font=("Inter Light", 30 * -1)
)


button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: RMS_window(),
    relief="flat",
    bg="#D9D9D9"
)
button_1.place(
    x=193.0,
    y=206.0,
    width=147.0,
    height=180.0
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda :phasor_window(),
    relief="flat",
    bg="#D9D9D9"
)
button_2.place(
    x=694.0,
    y=206.0,
    width=147.0,
    height=180.0
)

button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: Events_window(),
    relief="flat",
    bg="#D9D9D9"
)
button_3.place(
    x=438.0,
    y=206.0,
    width=147.0,
    height=180.0
)
label_font = font=("Inter Light", 30 * -1)
label_fecha_hora = Label(window, 
                         font=label_font,
                         bg="#212E4D",
                         fg="#D9D9D9",)


label_fecha_hora.place(x=675,y=18)

actualizar_fecha_hora()
window.resizable(False, False)
window.mainloop()
