
from pathlib import Path
from tkinter import Tk, Canvas, Button, PhotoImage,Toplevel,Label,ttk,messagebox
import datetime
import pandas as pd
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("assets/frame0")


def registrar_evento(Date,Time, IA,IB,IC,VA,VB,VC):
    df=pd.DataFrame(pd.read_excel(relative_to_assets("Events.xlsx"),index_col=False))
    df = df.drop(columns=['Unnamed: 0'])
    nueva_fila = ["Trigger",Date, Time, IA, IB, IC, VA, VB, VC]
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
def RMS_window(ruta_interfaz):
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
        textos=[A,B,C,D,E,E,F]
        for i in range(0,6):
                nuevo_texto = textos[i]
                if i <3:
                    Labels[i].config(text=str(nuevo_texto)+str( " V"))
                else:
                    Labels[i].config(text=str(nuevo_texto)+str( " A"))

    def catch():
         while(1):
            A=random.randint(1,10)
            B=random.randint(1,10)
            C=random.randint(1,10)
            D=random.randint(1,10)
            E=random.randint(1,10)
            F=random.randint(1,10)

            actualizar_etiqueta_atributos(A,B,C,D,E,F)
            if A>5:
                #1. enviar señal de disparo
                #2 registrar evento
                label_Falla.config(text="Falla")
                registrar_evento((datetime.datetime.now().strftime("%Y-%m-%d")),
                                 (datetime.datetime.now().strftime("%H:%M:%S")),
                                  A,B,C,D,E,F)
                #3:Aviso
                messagebox.showinfo("Alert", "Fault Detected")
            else:
                label_Falla.config(text="Normal")
    window_RMS = Toplevel()
    window_RMS.geometry("1024x600")
    window_RMS.overrideredirect(True)
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

    label_fecha_hora.place(x=680,y=18)

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
    command=lambda: RMS_window("RMS/RMS_gui.py"),
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
    command=lambda: print("button_2 clicked"),
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


label_fecha_hora.place(x=680,y=18)

actualizar_fecha_hora()
window.resizable(False, False)
window.mainloop()
