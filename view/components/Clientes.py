import customtkinter as ctk
from Backend.AnaliseData import AnaliseCliente

# Matplotlib para gráfico
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt


def Clientes(content, limpar_tela):
    limpar_tela()

    lbl = ctk.CTkLabel(content, text="👥 Tela de Clientes", font=("Arial", 20))
    lbl.pack(pady=20)

    # ================== CONTAINER PRINCIPAL ==================
    container = ctk.CTkFrame(content, fg_color="transparent")
    container.pack(pady=10, padx=0, fill="both", expand=True)

    container.grid_columnconfigure((0, 1), weight=1)
    container.grid_rowconfigure(0, weight=1)

    # ================== LEFT BOX ==================
    boxleft = ctk.CTkFrame(container, fg_color="#f2f3f2")
    boxleft.grid(row=0, column=0, padx=1, pady=10, sticky="ns")
    boxleft.configure(width=480)

    boxleft.grid_rowconfigure(1, weight=1)
    boxleft.grid_columnconfigure(0, weight=1)

    Tituloleft = ctk.CTkLabel(boxleft, text="Top 10 Clientes", font=("Arial", 22))
    Tituloleft.grid(row=0, column=0, pady=10)

    frameGrafico = ctk.CTkFrame(boxleft, fg_color="#e6e6e6", height=450)
    frameGrafico.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

    # ================== RIGHT BOX ==================
    boxright = ctk.CTkFrame(container, fg_color="#FFFFFF")
    boxright.grid(row=0, column=1, padx=0, pady=10, sticky="nsew")

    boxright.grid_columnconfigure((0, 1, 2), weight=1)
    boxright.grid_rowconfigure(1, weight=1)

    # ================= RIGHT HEADER =================
    headerright = ctk.CTkFrame(boxright, fg_color="#FFFFFF")
    headerright.grid(row=0, column=0, columnspan=3, sticky="nsew")

    headerright.columnconfigure((0, 1, 2), weight=1)
    headerright.rowconfigure((0, 1), weight=1)

    TituloRight = ctk.CTkLabel(headerright, text="Ranking dos Clientes", font=("Arial", 22))
    TituloRight.grid(row=0, column=0, columnspan=3, pady=10)

    # ComboBox Mês
    selecionarMes = ctk.CTkComboBox(
        headerright, height=50,
        values=[
            "Todos", "Janeiro", "Fevereiro", "Março", "Abril", "Maio",
            "Junho", "Julho", "Agosto", "Setembro", "Outubro",
            "Novembro", "Dezembro"
        ]
    )
    selecionarMes.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
    selecionarMes.set("Todos")

    # ComboBox Ano — agora com "Todos"
    selecionarAno = ctk.CTkComboBox(headerright, height=50, values=["Todos", "2025", "2024"])
    selecionarAno.grid(row=1, column=1, padx=20, pady=10, sticky="nsew")
    selecionarAno.set("Todos")

    buscarBtn = ctk.CTkButton(headerright, text="Buscar")
    buscarBtn.grid(row=1, column=2, padx=20, pady=10, sticky="nsew")

    # ================= RIGHT TABLE =================
    frametextosright = ctk.CTkScrollableFrame(boxright, fg_color="#FFFFFF")
    frametextosright.grid(row=1, column=0, columnspan=3, sticky="nsew")
    frametextosright.columnconfigure((0, 1, 2), weight=1)

    # ================= GRÁFICO =================
    def desenhar_grafico(dados):
        for w in frameGrafico.winfo_children():
            w.destroy()

        top10 = list(dados.items())[:10]
        clientes = [c for c, _ in top10]
        valores = [v["total_os"] for _, v in top10]

        fig, ax = plt.subplots(figsize=(5.7, 4.5))
        fig.patch.set_facecolor("#e6e6e6")

        ax.barh(clientes, valores)
        ax.tick_params(axis='y', labelsize=8)

        # deixa espaço para nomes grandes
        fig.subplots_adjust(left=0.40)

        ax.set_xlabel("OS Concluídas")
        ax.invert_yaxis()
        ax.grid(axis="x", linestyle="--", alpha=0.4)

        canvas = FigureCanvasTkAgg(fig, master=frameGrafico)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    # ---------- CABEÇALHO DA TABELA ----------
    def criar_cabecalho():
        for w in frametextosright.winfo_children():
            w.destroy()

        ctk.CTkLabel(frametextosright, text="Cliente", height=50,
                     font=("Arial", 14), fg_color="#f2f3f2").grid(row=0, column=0, sticky="nsew")

        ctk.CTkLabel(frametextosright, text="OS",
                     font=("Arial", 14), fg_color="#f2f3f2").grid(row=0, column=1, sticky="nsew")

        ctk.CTkLabel(frametextosright, text="Terceiros",
                     font=("Arial", 14), fg_color="#f2f3f2").grid(row=0, column=2, sticky="nsew")

    # ---------- PREENCHER TABELA ----------
    def preencher_tabela(dados):
        criar_cabecalho()

        for idx, (cliente, info) in enumerate(dados.items(), start=1):
            ctk.CTkLabel(frametextosright, text=cliente, font=("Arial", 13)).grid(
                row=idx, column=0, padx=10, pady=10, sticky="nsew"
            )
            ctk.CTkLabel(frametextosright, text=str(info["total_os"]), font=("Arial", 13)).grid(
                row=idx, column=1, padx=20, pady=10, sticky="nsew"
            )
            ctk.CTkLabel(frametextosright, text=str(info["blackwhite"]), font=("Arial", 13)).grid(
                row=idx, column=2, padx=20, pady=10, sticky="nsew"
            )

    # ================= FILTRO ==================

    meses_dict = {
        "Janeiro": 1, "Fevereiro": 2, "Março": 3, "Abril": 4,
        "Maio": 5, "Junho": 6, "Julho": 7, "Agosto": 8,
        "Setembro": 9, "Outubro": 10, "Novembro": 11, "Dezembro": 12
    }

    def aplicar_filtro():
        nome_mes = selecionarMes.get()
        ano_text = selecionarAno.get()

        mes = None
        ano = None

        if nome_mes != "Todos":
            mes = meses_dict.get(nome_mes)

        if ano_text != "Todos":
            ano = int(ano_text)

        # Agora SEMPRE aplicamos mes/ano corretamente
        dados = AnaliseCliente(mes=mes, ano=ano)

        preencher_tabela(dados)
        desenhar_grafico(dados)

    buscarBtn.configure(command=aplicar_filtro)

    # ================ EXIBIÇÃO INICIAL ================
    dados_iniciais = AnaliseCliente()
    preencher_tabela(dados_iniciais)
    desenhar_grafico(dados_iniciais)
