import customtkinter as ctk
from view.components.AnaliseTemporal import AnaliseTemporal
from view.components.Colaboradores import Colaboradores
from view.components.Clientes import Clientes
from view.components.Resumo import Resumo




def AreaSidebar(sidebar,content, limpar_tela):

    logo = ctk.CTkLabel(sidebar, text="Sistema de OS", font=("Arial Bold", 35,'bold'))
    logo.pack(pady=(70, 50))

    btn_resumo = ctk.CTkButton(sidebar, text="Resumo",height=70,fg_color="#2b2b2b",hover_color="#1f1f1f", font=("Arial", 16),
                                command=lambda: Resumo(content,lambda: (limpar_tela(content))))
    btn_resumo.pack(pady=10, fill="x", padx=20)
    
    btn_rclientes = ctk.CTkButton(sidebar, text="Ranking Clientes",height=70,fg_color="#2b2b2b",hover_color="#1f1f1f",font=("Arial", 16), command=lambda: Clientes(content,lambda: (limpar_tela(content))))
    btn_rclientes.pack(pady=10, fill="x", padx=20)

    btn_rcolaboradores = ctk.CTkButton(sidebar, text="Ranking Colaboradores",height=70,fg_color="#2b2b2b",hover_color="#1f1f1f",font=("Arial", 16), command=lambda: Colaboradores(content,lambda: (limpar_tela(content))))
    btn_rcolaboradores.pack(pady=10, fill="x", padx=20)

    btn_atemporal = ctk.CTkButton(sidebar, text="Análise Temporal",height=70,fg_color="#2b2b2b",hover_color="#1f1f1f", font=("Arial", 16), command=lambda: AnaliseTemporal(content,lambda: (limpar_tela(content))))
    btn_atemporal.pack(pady=10, fill="x", padx=20)


    