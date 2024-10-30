import tkinter as tk
from tkinter import ttk
from ui import crear_interfaz

if __name__ == "__main__":
    ventana = tk.Tk()
    ventana.title("Gestor de Archivos Excel")
    ventana.geometry("1360x700")
    
    crear_interfaz(ventana)
    ventana.mainloop()