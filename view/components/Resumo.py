import customtkinter as ctk
from Backend.AnaliseData import AnaliseResumo


def Resumo(content, limpar_tela):
    limpar_tela()
    lbl = ctk.CTkLabel(content, text="📊 Tela de Resumo", font=("Arial", 30, "bold"))
    lbl.pack(pady=20)
    area1 = ctk.CTkFrame(content, fg_color="#FFFFFF", height=150)
    area1.pack(pady=10, padx=20, fill="x")

    area1.grid_columnconfigure((0, 1, 2, 3), weight=1)
    area1.grid_rowconfigure(0, weight=1)

    def criar_card(parent, titulo, valor, coluna):
        card = ctk.CTkFrame(parent, fg_color="#f2f3f2", width=200, height=80)
        card.grid(row=0, column=coluna, padx=20, pady=20, sticky="nsew")
        card.pack_propagate(False)

        lbl_titulo = ctk.CTkLabel(card, text=titulo, font=("Arial", 18, "bold"), text_color="#2B2B2B")
        lbl_titulo.pack(pady=5)
        lbl_valor = ctk.CTkLabel(card, text=valor, font=("Arial Bold", 26, "bold"), text_color="#2B2B2B")
        lbl_valor.pack()
    resumo = AnaliseResumo()
    

    # Cria os 4 cards centralizados
    criar_card(area1, "Total de OS", resumo['totalOs'] , 0)
    criar_card(area1, "OS Concluidas", resumo['concluidas'], 1)
    criar_card(area1, "Colaboradores", resumo['users'], 2)
    criar_card(area1, "Clientes", resumo['clientes'], 3)
