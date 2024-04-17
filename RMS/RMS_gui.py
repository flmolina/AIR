
# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer

import random
from pathlib import Path
import threading

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage,Toplevel,Label


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("assets/frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def actualizar_etiqueta(A,B,C,D,E,F):
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
        actualizar_etiqueta(A,B,C,D,E,F)
window_RMS = Tk()

window_RMS.geometry("1024x600")
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
    text="RMS",
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
    text="IA",
    fill="#212E4D",
    font=("Inter Bold", 50 * -1)
)

canvas.create_text(
    156.0,
    443.0,
    anchor="nw",
    text="IA",
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
    594.0,
    -1.0,
    595.0,
    60.0,
    fill="#FFFFFF",
    outline="")

canvas.create_rectangle(
    509.0,
    57.0,
    512.0,
    540.0,
    fill="#000000",
    outline="")

canvas.create_rectangle(
    844.0,
    -1.0,
    845.0,
    60.0,
    fill="#FFFFFF",
    outline="")

canvas.create_rectangle(
    0.0,
    60.0,
    91.0,
    540.0,
    fill="#E8CA2A",
    outline="")

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_1 clicked"),
    relief="flat"
)
button_1.place(
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

thread=threading.Thread(target=catch)
thread.daemon=True
thread.start()


window_RMS.resizable(False, False)
window_RMS.mainloop()
