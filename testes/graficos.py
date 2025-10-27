import customtkinter as ctk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random

# ======================
# Configurações gerais
# ======================
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("1100x650")
app.title("Dashboard - InforWay")

# ======================
# Função para limpar conteúdo
# ======================
def limpar_tela():
    for widget in content.winfo_children():
        widget.destroy()

# ======================
# Telas
# ======================
def mostrar_resumo():
    limpar_tela()

    # Frame para cards de resumo
    cards_frame = ctk.CTkFrame(content, fg_color="transparent")
    cards_frame.pack(fill="x", padx=20, pady=(20, 10))

    # Criar 3 cards
    card1 = ctk.CTkFrame(cards_frame, fg_color="#3B8ED0", corner_radius=10)
    card1.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
    ctk.CTkLabel(card1, text="Total de OS", font=("Arial", 16, "bold")).pack(pady=(10,0))
    ctk.CTkLabel(card1, text="128", font=("Arial", 24)).pack()

    card2 = ctk.CTkFrame(cards_frame, fg_color="#1F6AA5", corner_radius=10)
    card2.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
    ctk.CTkLabel(card2, text="OS Concluídas", font=("Arial", 16, "bold")).pack(pady=(10,0))
    ctk.CTkLabel(card2, text="115", font=("Arial", 24)).pack()

    card3 = ctk.CTkFrame(cards_frame, fg_color="#144870", corner_radius=10)
    card3.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")
    ctk.CTkLabel(card3, text="Tempo Médio", font=("Arial", 16, "bold")).pack(pady=(10,0))
    ctk.CTkLabel(card3, text="3.2h", font=("Arial", 24)).pack()

    # Faz os 3 cards se ajustarem igualmente
    cards_frame.grid_columnconfigure((0,1,2), weight=1)

    # Frame para gráficos
    graficos_frame = ctk.CTkFrame(content, fg_color="transparent")
    graficos_frame.pack(fill="both", expand=True, padx=20, pady=(10, 20))

    # Gráfico 1 - Barras
    fig1 = Figure(figsize=(4,3), dpi=100)
    ax1 = fig1.add_subplot(111)
    ax1.bar(["Seg", "Ter", "Qua", "Qui", "Sex"], [random.randint(5,20) for _ in range(5)])
    ax1.set_title("OS por dia")
    canvas1 = FigureCanvasTkAgg(fig1, master=graficos_frame)
    canvas1.draw()
    canvas1.get_tk_widget().grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

    # Gráfico 2 - Pizza
    fig2 = Figure(figsize=(4,3), dpi=100)
    ax2 = fig2.add_subplot(111)
    ax2.pie([60, 30, 10], labels=["Concluídas", "Pendentes", "Canceladas"], autopct="%1.1f%%")
    ax2.set_title("Status das OS")
    canvas2 = FigureCanvasTkAgg(fig2, master=graficos_frame)
    canvas2.draw()
    canvas2.get_tk_widget().grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

    # Permite expansão dos gráficos
    graficos_frame.grid_columnconfigure((0,1), weight=1)
    graficos_frame.grid_rowconfigure(0, weight=1)

def mostrar_outro_exemplo():
    limpar_tela()
    ctk.CTkLabel(content, text="Outra Tela (em construção)", font=("Arial", 20)).pack(pady=50)

# ======================
# Layout principal
# ======================
frame_dashboard = ctk.CTkFrame(app)
frame_dashboard.pack(fill="both", expand=True)

# Sidebar (menu lateral)
sidebar = ctk.CTkFrame(frame_dashboard, width=200, corner_radius=0)
sidebar.pack(side="left", fill="y")

# Content (área principal)
content = ctk.CTkFrame(frame_dashboard, fg_color="white")
content.pack(side="left", fill="both", expand=True)

# ======================
# Sidebar widgets
# ======================
logo = ctk.CTkLabel(sidebar, text="InforWay\nInformática", font=("Arial Bold", 16))
logo.pack(pady=(30, 50))

btn_resumo = ctk.CTkButton(sidebar, text="Resumo", command=mostrar_resumo)
btn_resumo.pack(pady=10, fill="x", padx=20)

btn_analise = ctk.CTkButton(sidebar, text="Outra Tela", command=mostrar_outro_exemplo)
btn_analise.pack(pady=10, fill="x", padx=20)

btn_sair = ctk.CTkButton(sidebar, text="Sair", fg_color="red", command=app.destroy)
btn_sair.pack(side="bottom", pady=20, padx=20, fill="x")

# ======================
# Tela inicial
# ======================
mostrar_resumo()

app.mainloop()
