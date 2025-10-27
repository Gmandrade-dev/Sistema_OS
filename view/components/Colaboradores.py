import customtkinter as ctk

def Colaboradores(content,limpar_tela):
    limpar_tela()
    lbl = ctk.CTkLabel(content, text="👥 Ranking de Colaboradores", font=("Arial", 20))
    lbl.pack(pady=20)