import customtkinter as ctk
from Backend.AnaliseData import AnaliseColaboradores, AnaliseColaboradorMensal
# Matplotlib para gráfico
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt


def Colaboradores(content, limpar_tela):
    limpar_tela()

    lbl = ctk.CTkLabel(content, text="👨‍🔧 Tela de Colaboradores", font=("Arial", 20))
    lbl.pack(pady=20)

    # ================== CONTAINER PRINCIPAL ==================
    container = ctk.CTkFrame(content, fg_color="transparent")
    container.pack(pady=10, padx=0, fill="both", expand=True)

    container.grid_columnconfigure((0, 1), weight=1)
    container.grid_rowconfigure(0, weight=1)

    # ================== LEFT BOX (GRÁFICO) ==================
    boxleft = ctk.CTkFrame(container, fg_color="#f2f3f2")
    boxleft.grid(row=0, column=0, padx=1, pady=10, sticky="nsew")
    boxleft.configure(width=740)

    boxleft.grid_rowconfigure((1, 2), weight=1)
    boxleft.grid_columnconfigure(0, weight=1)

    TituloLeft = ctk.CTkLabel(boxleft, text="Performance Mensal", font=("Arial", 22))
    TituloLeft.grid(row=0, column=0, pady=8)

    # area do gráfico (com botões em cima)
    graf_top = ctk.CTkFrame(boxleft, fg_color="#FFFFFF")
    graf_top.grid(row=1, column=0, padx=10, pady=(0, 5), sticky="ew")
    graf_top.grid_columnconfigure((0, 1), weight=1)

    # ================== RIGHT BOX (TABELA) ==================
    boxright = ctk.CTkFrame(container, fg_color="#FFFFFF")
    boxright.grid(row=0, column=1, padx=0, pady=10, sticky="nsew")

    boxright.grid_columnconfigure((0, 1, 2), weight=1)
    boxright.grid_rowconfigure(1, weight=1)

    # ================= RIGHT HEADER (filtros) =================
    headerright = ctk.CTkFrame(boxright, fg_color="#FFFFFF")
    headerright.grid(row=0, column=0, columnspan=3, sticky="nsew", pady=(0, 5))

    headerright.columnconfigure((0, 1, 2), weight=1)
    headerright.rowconfigure((0, 1), weight=1)

    TituloRight = ctk.CTkLabel(headerright, text="Ranking dos Colaboradores", font=("Arial", 22))
    TituloRight.grid(row=0, column=0, columnspan=3, pady=10)

    # ComboBox Mês
    selecionarMes = ctk.CTkComboBox(
        headerright, height=45,
        values=[
            "Todos", "Janeiro", "Fevereiro", "Março", "Abril", "Maio",
            "Junho", "Julho", "Agosto", "Setembro", "Outubro",
            "Novembro", "Dezembro"
        ]
    )
    selecionarMes.grid(row=1, column=0, padx=12, pady=6, sticky="nsew")
    selecionarMes.set("Todos")

    # ComboBox Ano
    selecionarAno = ctk.CTkComboBox(headerright, height=45, values=["Todos", "2025", "2024"])
    selecionarAno.grid(row=1, column=1, padx=12, pady=6, sticky="nsew")
    selecionarAno.set("Todos")

    buscarBtn = ctk.CTkButton(headerright, text="Buscar", height=45)
    buscarBtn.grid(row=1, column=2, padx=12, pady=6, sticky="nsew")

    # ================= RIGHT TABLE (scroll) =================
    frametextosright = ctk.CTkScrollableFrame(boxright, fg_color="#FFFFFF")
    frametextosright.grid(row=1, column=0, columnspan=3, sticky="nsew")
    frametextosright.columnconfigure((0, 1, 2), weight=1)

    # ================== FRAME DO GRAFICO ==================
    frameGrafico = ctk.CTkFrame(boxleft, fg_color="#e6e6e6", height=380)
    frameGrafico.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
    frameGrafico.grid_columnconfigure(0, weight=1)
    frameGrafico.grid_rowconfigure(0, weight=1)

    # ---------------- Botão Atualizar + Select ----------------
    btn_refresh = ctk.CTkButton(graf_top, text="Atualizar", height=36, width=100)
    btn_refresh.grid(row=0, column=0, padx=6, pady=6, sticky="w")

    selecionarNome = ctk.CTkComboBox(graf_top, height=36, values=["Todos"])
    selecionarNome.grid(row=0, column=1, padx=12, pady=6, sticky="e")
    selecionarNome.set("Todos")

    # ================= Funções =================
    meses_dict = {
        "Janeiro": 1, "Fevereiro": 2, "Março": 3, "Abril": 4,
        "Maio": 5, "Junho": 6, "Julho": 7, "Agosto": 8,
        "Setembro": 9, "Outubro": 10, "Novembro": 11, "Dezembro": 12
    }

    def desenhar_grafico_mensal(colaborador=None, ano=None):
        for w in frameGrafico.winfo_children():
            w.destroy()

        ano_int = None
        if ano and ano != "Todos":
            try:
                ano_int = int(ano)
            except:
                ano_int = None

        dados_mensais = AnaliseColaboradorMensal(colaborador if colaborador != "Todos" else None, ano=ano_int)
        meses = list(dados_mensais.keys())
        valores = list(dados_mensais.values())

        fig, ax = plt.subplots(figsize=(8.5, 3.8))
        fig.patch.set_facecolor("#e6e6e6")

        ax.plot(meses, valores, marker='o')
        ax.set_ylabel("OS")
        ax.set_xlabel("")
        ax.set_xticks(range(len(meses)))
        ax.set_xticklabels(meses, rotation=45, fontsize=9)
        ax.grid(axis="y", linestyle="--", alpha=0.4)

        fig.subplots_adjust(left=0.05, right=0.99, top=0.92, bottom=0.28)

        canvas = FigureCanvasTkAgg(fig, master=frameGrafico)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def criar_cabecalho_tabela():
        for w in frametextosright.winfo_children():
            w.destroy()

        ctk.CTkLabel(frametextosright, text="Colaborador", height=50,
                     font=("Arial", 14), fg_color="#f2f3f2").grid(row=0, column=0, sticky="nsew")
        ctk.CTkLabel(frametextosright, text="OS",
                     font=("Arial", 14), fg_color="#f2f3f2").grid(row=0, column=1, sticky="nsew")
        ctk.CTkLabel(frametextosright, text="Tempo Médio",
                     font=("Arial", 14), fg_color="#f2f3f2").grid(row=0, column=2, sticky="nsew")

    def preencher_tabela(dados):
        criar_cabecalho_tabela()

        for idx, (usuario, info) in enumerate(dados.items(), start=1):
            ctk.CTkLabel(frametextosright, text=usuario, font=("Arial", 13), fg_color="#FFFFFF").grid(
                row=idx, column=0, padx=10, pady=6, sticky="nsew"
            )
            ctk.CTkLabel(frametextosright, text=str(info["total_os"]), font=("Arial", 13), fg_color="#FFFFFF").grid(
                row=idx, column=1, padx=20, pady=6, sticky="nsew"
            )
            ctk.CTkLabel(frametextosright, text=str(info["tempo_medio"]), font=("Arial", 13), fg_color="#FFFFFF").grid(
                row=idx, column=2, padx=20, pady=6, sticky="nsew"
            )

    # ================= FILTRO ==================
    def aplicar_filtro():
        nome_mes = selecionarMes.get()
        ano_text = selecionarAno.get()

        mes = None
        ano = None

        if nome_mes != "Todos":
            mes = meses_dict.get(nome_mes)

        if ano_text != "Todos":
            try:
                ano = int(ano_text)
            except:
                ano = None

        dados = AnaliseColaboradores(mes=mes, ano=ano)
        preencher_tabela(dados)

        colaboradores = ["Todos"] + list(dados.keys())
        selecionarNome.configure(values=colaboradores)

        if selecionarNome.get() not in colaboradores:
            selecionarNome.set("Todos")

        desenhar_grafico_mensal(colaborador=selecionarNome.get(), ano=ano_text)

    def on_selecionar_nome_change(choice=None):
        nome = selecionarNome.get()
        ano_text = selecionarAno.get()
        desenhar_grafico_mensal(colaborador=nome, ano=ano_text)

    buscarBtn.configure(command=aplicar_filtro)
    selecionarNome.configure(command=on_selecionar_nome_change)
    btn_refresh.configure(command=aplicar_filtro)

    # ================ EXIBIÇÃO INICIAL ================
    dados_iniciais = AnaliseColaboradores()
    preencher_tabela(dados_iniciais)

    colaboradores_init = ["Todos"] + list(dados_iniciais.keys())
    selecionarNome.configure(values=colaboradores_init)
    selecionarNome.set("Todos")

    desenhar_grafico_mensal(colaborador="Todos", ano="Todos")
