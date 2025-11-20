import customtkinter as ctk
from Backend.AnaliseData import AnaliseResumo, GetData
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd


def Resumo(content, limpar_tela):
    print("Resumo chamado")
    limpar_tela()

    # ---------------- TÍTULO ----------------
    ctk.CTkLabel(
        content,
        text="📊 Tela de Resumo",
        font=("Arial", 30, "bold")
    ).pack(pady=20)

    # ----------------   FUNÇÃO: CARD ----------------
    def criar_card(parent, titulo, valor, coluna):
        card = ctk.CTkFrame(parent, fg_color="#f2f3f2", height=85, corner_radius=12)
        card.grid(row=0, column=coluna, padx=20, pady=20, sticky="nsew")
        card.pack_propagate(False)

        ctk.CTkLabel(card, text=titulo, font=("Arial", 20, "bold"), text_color="#2B2B2B").pack(pady=5)
        ctk.CTkLabel(card, text=valor, font=("Arial Bold", 30, "bold"), text_color="#2B2B2B").pack()

    # ----------------   CARDS SUPERIORES ----------------
    area1 = ctk.CTkFrame(content, fg_color="#FFFFFF", height=85)
    area1.pack(pady=10, padx=20, fill="x")
    area1.grid_columnconfigure((0, 1, 2, 3), weight=1)

    resumo = AnaliseResumo()
    criar_card(area1, "Total de OS", resumo['totalOs'], 0)
    criar_card(area1, "OS Concluídas", resumo['concluidas'], 1)
    criar_card(area1, "Colaboradores", resumo['users'], 2)
    criar_card(area1, "Clientes", resumo['clientes'], 3)

    # ----------------   ÁREA GRÁFICO + LISTAS ----------------
    area2 = ctk.CTkFrame(content, fg_color="#FFFFFF")
    area2.pack(pady=10, padx=20, fill="both", expand=True)

    area2.grid_columnconfigure(0, weight=1)
    area2.grid_rowconfigure((0, 1), weight=1)

    # ----------------   GRÁFICO DE OS POR MÊS ----------------
    frame_grafico = ctk.CTkFrame(area2, fg_color="#FFFFFF")
    frame_grafico.grid(row=0, column=0, padx=20, pady=(10, 5), sticky="nsew")

    df = GetData("tb_os").copy()
    df["data_criacao"] = pd.to_datetime(df["data_criacao"], errors="coerce")
    df = df[df["data_criacao"].dt.year == 2025]
    df["mes"] = df["data_criacao"].dt.month

    meses_pt = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun",
                "Jul", "Ago", "Set", "Out", "Nov", "Dez"]

    os_por_mes = df["mes"].value_counts().sort_index()
    os_por_mes.index = [meses_pt[m - 1] for m in os_por_mes.index]

    fig, ax = plt.subplots(figsize=(7, 2.4), dpi=100)
    ax.plot(os_por_mes.index, os_por_mes.values, marker="o", linewidth=2)

    ax.set_title("OS Criadas por Mês (2025)", fontsize=10, pad=10)
    ax.set_ylabel("Quantidade", fontsize=10)
    ax.grid(alpha=0.3)

    grafico_canvas = FigureCanvasTkAgg(fig, master=frame_grafico)
    grafico_canvas.draw()
    grafico_canvas.get_tk_widget().pack(fill="both", expand=True)

    # ----------------   LISTAS (TOP CLIENTES E TOP USUÁRIOS) ----------------
    frame_listas = ctk.CTkFrame(area2, fg_color="#FFFFFF")
    frame_listas.grid(row=1, column=0, padx=20, pady=(5, 10), sticky="nsew")
    frame_listas.grid_columnconfigure((0, 1), weight=1)

    # ----------------   FUNÇÃO CORRETA: LISTA TOP (SÓ GRID) ----------------
    def criar_lista(parent, titulo, serie, col):
        frame = ctk.CTkFrame(parent, fg_color="#f2f3f2", corner_radius=10)
        frame.grid(row=0, column=col, padx=10, pady=10, sticky="nsew")
        frame.grid_columnconfigure((0, 1), weight=1)

        # título — usando grid corretamente
        ctk.CTkLabel(
            frame,
            text=titulo,
            font=("Arial", 18, "bold")
        ).grid(row=0, column=0, columnspan=2, pady=10)

        # itens — a partir da linha 1
        for i, (nome, total) in enumerate(serie.items(), start=1):
            ctk.CTkLabel(
                frame, text=nome, font=("Arial", 17)
            ).grid(row=i, column=0, sticky="w", padx=20, pady=3)

            ctk.CTkLabel(
                frame, text=f"{total} OS", font=("Arial", 17)
            ).grid(row=i, column=1, sticky="e", padx=20, pady=3)

    # --- TOP CLIENTES ---
    df_cliente = (
        df.groupby("cliente")["id_os"]
        .count()
        .sort_values(ascending=False)
        .head(5)
    )

    criar_lista(
        frame_listas,
        "🏆 Top 5 Clientes com Mais OS",
        df_cliente,
        col=0
    )

    # --- TOP COLABORADORES ---
    df_users = (
        df.groupby("usuario_responsavel")["id_os"]
        .count()
        .sort_values(ascending=False)
        .head(5)
    )

    criar_lista(
        frame_listas,
        "👷 Top 5 Colaboradores com Mais OS",
        df_users,
        col=1
    )
