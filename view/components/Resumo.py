import customtkinter as ctk
from Backend.AnaliseData import AnaliseResumo, GetData
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd


def Resumo(content, limpar_tela):
    limpar_tela()

    lbl = ctk.CTkLabel(content, text="📊 Tela de Resumo",
                       font=("Arial", 30, "bold"))
    lbl.pack(pady=(20, 10))

    # -------------------- CARDS SUPERIORES -------------------------
    area_cards = ctk.CTkFrame(content, fg_color="#FFFFFF", height=80)
    area_cards.pack(pady=10, padx=20, fill="x")
    area_cards.grid_columnconfigure((0, 1, 2, 3), weight=1)

    def criar_card(parent, titulo, valor, coluna):
        card = ctk.CTkFrame(parent, fg_color="#f7f7f7", height=100, corner_radius=12)
        card.grid(row=0, column=coluna, padx=12, pady=20, sticky="nsew")
        card.pack_propagate(False)

        ctk.CTkLabel(card, text=titulo,
                     font=("Arial", 16, "bold"),
                     text_color="#333").pack(pady=(10, 3))

        ctk.CTkLabel(card, text=valor,
                     font=("Arial Black", 30),
                     text_color="#111").pack(pady=4)

    resumo = AnaliseResumo()

    criar_card(area_cards, "Total de OS", resumo["totalOs"], 0)
    criar_card(area_cards, "OS Concluídas", resumo["concluidas"], 1)
    criar_card(area_cards, "Colaboradores", resumo["users"], 2)
    criar_card(area_cards, "Clientes", resumo["clientes"], 3)

    # --------------------- ÁREA PRINCIPAL --------------------------
    area_principal = ctk.CTkFrame(content, fg_color="#F5F5F5")
    area_principal.pack(pady=10, padx=20, fill="both", expand=True)

    area_principal.grid_columnconfigure((0, 1), weight=1)

    # Linha 0 não cresce (gráfico)
    area_principal.grid_rowconfigure(0, weight=0)

    # Linha 1 cresce (scrolls)
    area_principal.grid_rowconfigure(1, weight=1)

    # ------------------------ GRÁFICO -------------------------------
    frame_grafico = ctk.CTkFrame(area_principal, fg_color="#FFFFFF",
                                 corner_radius=12, height=230)
    frame_grafico.grid(row=0, column=0, columnspan=2,
                       padx=20, pady=(20, 10), sticky="nsew")
    frame_grafico.pack_propagate(False)

    df = GetData("tb_os").copy()
    df["data_criacao"] = pd.to_datetime(df["data_criacao"], errors="coerce")
    df = df[df["data_criacao"].dt.year == 2025]
    df["mes"] = df["data_criacao"].dt.month

    meses_pt = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun",
                "Jul", "Ago", "Set", "Out", "Nov", "Dez"]

    os_mes = df["mes"].value_counts().sort_index()
    os_mes.index = [meses_pt[m - 1] for m in os_mes.index]

    # Gráfico estilizado
    fig, ax = plt.subplots(figsize=(8, 1.8), dpi=100)
    ax.plot(os_mes.index, os_mes.values, marker="o", linewidth=2)
    ax.set_title("OS Criadas por Mês (2025)", fontsize=13, pad=10)
    ax.grid(alpha=0.3)

    fig.tight_layout()

    graf_canvas = FigureCanvasTkAgg(fig, master=frame_grafico)
    graf_canvas.draw()
    graf_canvas.get_tk_widget().pack(fill="both", expand=True)

    # -------------------- TOP CLIENTES -----------------------------
    frame_clientes = ctk.CTkScrollableFrame(area_principal,
                                            fg_color="#FFFFFF",
                                            corner_radius=12,
                                            height=260)
    frame_clientes.grid(row=1, column=0,
                        padx=(20, 10), pady=20, sticky="nsew")
    frame_clientes.pack_propagate(False)
    frame_clientes.configure(width=350)

    ctk.CTkLabel(frame_clientes, text="🏆 Top 5 Clientes",
                 font=("Arial", 18, "bold")).pack(pady=10)

    top_clientes = (df.groupby("cliente")["id_os"]
                    .count()
                    .sort_values(ascending=False)
                    .head(5))

    for nome, total in top_clientes.items():
        ctk.CTkLabel(frame_clientes,
                     text=f"{nome} — {total} OS",
                     font=("Arial", 15),
                     text_color="#333").pack(anchor="w", padx=20, pady=4)

    # -------------------- TOP COLABORADORES ------------------------
    frame_users = ctk.CTkScrollableFrame(area_principal,
                                         fg_color="#FFFFFF",
                                         corner_radius=12,
                                         height=260)
    frame_users.grid(row=1, column=1,
                     padx=(10, 20), pady=20, sticky="nsew")
    frame_users.pack_propagate(False)
    frame_users.configure(width=350)

    ctk.CTkLabel(frame_users, text="👷 Top 5 Colaboradores",
                 font=("Arial", 18, "bold")).pack(pady=10)

    top_users = (df.groupby("usuario_responsavel")["id_os"]
                 .count()
                 .sort_values(ascending=False)
                 .head(5))

    for nome, total in top_users.items():
        ctk.CTkLabel(frame_users,
                     text=f"{nome} — {total} OS",
                     font=("Arial", 15),
                     text_color="#333").pack(anchor="w", padx=20, pady=4)
