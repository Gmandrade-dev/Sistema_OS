import customtkinter as ctk
from view.Dashboard import Dashboard


app = ctk.CTk()
app.title("Sistema de OS")
app.geometry("1280x700")
app.maxsize(1920, 1080)
app.minsize(1000, 700)
frame_container = ctk.CTkFrame(app)
frame_container.pack(fill="both", expand=True)

def limpar_tela(frame_selecionado):
    for widget in frame_selecionado.winfo_children():
        widget.destroy()

def mostrar_dashboard():
    limpar_tela(frame_container)
    Dashboard(frame_container,limpar_tela)
  
mostrar_dashboard()
app.mainloop()


   
