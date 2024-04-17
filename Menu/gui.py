
# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer


from pathlib import Path
# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage,Toplevel


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("assets/frame0")


def RMS_window(ruta_interfaz):
    global window
    window.withdraw()  # Oculta la ventana actual
    with open(ruta_interfaz, "r") as f:
        codigo_interfaz = f.read()
    exec(codigo_interfaz, globals(), locals())


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()

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

canvas.create_rectangle(
    594.0,
    -1.0,
    595.0,
    60.0,
    fill="#FFFFFF",
    outline="")

canvas.create_rectangle(
    844.0,
    -1.0,
    845.0,
    60.0,
    fill="#FFFFFF",
    outline="")

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: RMS_window("RMS/RMS_gui.py"),
    relief="flat"
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
    relief="flat"
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
    command=lambda: print("button_3 clicked"),
    relief="flat"
)
button_3.place(
    x=438.0,
    y=206.0,
    width=147.0,
    height=180.0
)

window.resizable(False, False)
window.mainloop()
