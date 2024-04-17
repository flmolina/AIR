import tkinter as tk
from interfaz_b import InterfazB

class InterfazA(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Interfaz A")
        self.geometry("300x200")
        
        self.btn_abrir_b = tk.Button(self, text="Abrir Interfaz B", command=self.abrir_interfaz_b)
        self.btn_abrir_b.pack(pady=20)
        
    def abrir_interfaz_b(self):
        self.withdraw()  # Oculta la interfaz A
        self.interfaz_b = InterfazB(self)  # Crea la instancia de la interfaz B
        self.interfaz_b.protocol("WM_DELETE_WINDOW", self.cerrar_interfaz_b)  # Define una acción cuando se cierre la interfaz B
        
    def cerrar_interfaz_b(self):
        self.deiconify()  # Vuelve a mostrar la interfaz A
        self.interfaz_b.destroy()  # Destruye la interfaz B

if __name__ == "__main__":
    app = InterfazA()
    app.mainloop()