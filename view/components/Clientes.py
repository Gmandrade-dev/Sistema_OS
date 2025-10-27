import customtkinter as ctk

def Clientes(content,limpar_tela):
    limpar_tela()
    lbl = ctk.CTkLabel(content, text="👥 Tela de Clientes", font=("Arial", 20))
    lbl.pack(pady=20)