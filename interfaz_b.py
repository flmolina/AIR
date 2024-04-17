import tkinter as tk

class InterfazB(tk.Toplevel):
    def __init__(self, interfaz_a):
        super().__init__(interfaz_a)
        
        self.title("Interfaz B")
        self.geometry("300x200")
        
        self.btn_abrir_a = tk.Button(self, text="Abrir Interfaz A", command=self.abrir_interfaz_a)
        self.btn_abrir_a.pack(pady=20)
        
        self.interfaz_a = interfaz_a  # Guarda una referencia a la instancia de la interfaz A
        
    def abrir_interfaz_a(self):
        self.destroy()  # Destruye la interfaz B
        self.interfaz_a.deiconify()  # Vuelve a mostrar la interfaz A

if __name__ == "__main__":
    app = InterfazB(None)
    app.mainloop()