import customtkinter as ctk

def AnaliseTemporal(content,limpar_tela):
    limpar_tela()
    lbl = ctk.CTkLabel(content, text="📊 Analise temporal", font=("Arial", 20))
    lbl.pack(pady=20)
    