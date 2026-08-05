import tkinter as tk

def al_presionar():
    global contador
    contador += 1
    etiqueta.config(text=f"Presionaste {contador} veces")

contador = 0
root = tk.Tk()
root.title("MiPrimerPrograma")
root.geometry("400x300")

etiqueta = tk.Label(root, text="Bienvenido a MiPrimerPrograma\nHecho con SiPi", font=("Segoe UI", 14))
etiqueta.pack(pady=40)

boton = tk.Button(root, text="Presioname", command=al_presionar, font=("Segoe UI", 12))
boton.pack()

root.mainloop()
