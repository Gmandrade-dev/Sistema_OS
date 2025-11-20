import customtkinter as ctk
from Backend.AnaliseData import AnaliseCliente

def Clientes(content, limpar_tela):
    limpar_tela()
    lbl = ctk.CTkLabel(content, text="👥 Tela de Clientes", font=("Arial", 20))
    lbl.pack(pady=20)

    container = ctk.CTkFrame(content, fg_color="transparent")
    container.pack(pady=10, padx=10, fill="both", expand=True)

    boxleft = ctk.CTkFrame(container, fg_color="#f2f3f2", width=200)
    boxleft.grid(row=0, column=0, padx=(8,10), pady=10, sticky="nsew")

    boxright = ctk.CTkFrame(container, fg_color="#FFFFFF")
    boxright.grid(row=0, column=1, padx=(10,8), pady=10, sticky="nsew")

    container.grid_columnconfigure((0,1), weight=1)
    container.grid_rowconfigure(0, weight=1)

    Tituloleft = ctk.CTkLabel(boxleft, text="Lista de Clientes", font=("Arial", 22))
    Tituloleft.pack(pady=10)

    # ------------------ RIGHT HEADER ------------------
    headerright = ctk.CTkFrame(boxright, fg_color="#ffffff")
    headerright.grid(row=0, column=0, columnspan=3, sticky="nsew")
    headerright.columnconfigure((0,1,2), weight=1)
    headerright.rowconfigure((0,1), weight=1)

    TituloRight = ctk.CTkLabel(headerright, text="Ranking dos Clientes", font=("Arial", 22))
    TituloRight.grid(row=0, column=0, columnspan=3, pady=10)

    selecionarMes = ctk.CTkComboBox(
        headerright, height=50,
        values=["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
                "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
    )
    selecionarMes.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")

    selecionarAno = ctk.CTkComboBox(headerright, height=50, values=["2025"])
    selecionarAno.grid(row=1, column=1, padx=20, pady=10, sticky="nsew")

    buscarBtn = ctk.CTkButton(headerright, text="Buscar")
    buscarBtn.grid(row=1, column=2, padx=20, pady=10, sticky="nsew")

    boxright.grid_columnconfigure((0,1,2), weight=1)
    boxright.grid_rowconfigure(1, weight=1)

    # ------------------ TABLE AREA (SCROLLABLE) ------------------
    frametextosright = ctk.CTkScrollableFrame(boxright, fg_color="#ffffff")
    frametextosright.grid(row=1, column=0, columnspan=3, sticky="nsew")
    frametextosright.columnconfigure((0,1,2), weight=1)

    # helper: (re)cria cabeçalho da "tabela"
    def criar_cabecalho():
        # limpa só os widgets do frame (se houver)
        for w in frametextosright.winfo_children():
            w.destroy()

        # cabeçalho (linha 0)
        textocliente = ctk.CTkLabel(frametextosright, text="Cliente", height=50,
                                    font=("Arial", 20), fg_color="#f2f3f2")
        textocliente.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")

        textoOs = ctk.CTkLabel(frametextosright, text="OS", font=("Arial", 20), fg_color="#f2f3f2")
        textoOs.grid(row=0, column=1, padx=0, pady=0, sticky="nsew")

        textoTerceiros = ctk.CTkLabel(frametextosright, text="Terceiros", font=("Arial", 20), fg_color="#f2f3f2")
        textoTerceiros.grid(row=0, column=2, padx=0, pady=0, sticky="nsew")

    # helper: preenche a tabela a partir do dict retornado por AnaliseCliente
    def preencher_tabela(dados):
        criar_cabecalho()
        for idx, (cliente, info) in enumerate(dados.items(), start=1):
            # Nome do cliente
            dados_cliente = ctk.CTkLabel(frametextosright, text=cliente, font=("Arial", 17))
            dados_cliente.grid(row=idx, column=0, padx=20, pady=10, sticky="nsew")

            # Total OS
            dados_os = ctk.CTkLabel(frametextosright, text=str(info.get("total_os", 0)), font=("Arial", 17))
            dados_os.grid(row=idx, column=1, padx=20, pady=10, sticky="nsew")

            # BlackWhite count
            dados_terceiros = ctk.CTkLabel(frametextosright, text=str(info.get("blackwhite", 0)), font=("Arial", 17))
            dados_terceiros.grid(row=idx, column=2, padx=20, pady=10, sticky="nsew")

    # map months to numbers
    meses_dict = {
        "Janeiro": 1, "Fevereiro": 2, "Março": 3, "Abril": 4,
        "Maio": 5, "Junho": 6, "Julho": 7, "Agosto": 8,
        "Setembro": 9, "Outubro": 10, "Novembro": 11, "Dezembro": 12
    }

    # função do botão Buscar: aplica filtro (ou mostra tudo se nada selecionado)
    def aplicar_filtro():
        nome_mes = selecionarMes.get()
        ano_text = selecionarAno.get()

        # se mês/ano não preenchidos, mostra sem filtro
        if not nome_mes or not ano_text:
            dados_filtrados = AnaliseCliente()  # sem filtro
        else:
            mes = meses_dict.get(nome_mes)
            try:
                ano = int(ano_text)
            except Exception:
                # se ano inválido, não filtra
                dados_filtrados = AnaliseCliente()
            else:
                dados_filtrados = AnaliseCliente(mes, ano)

        preencher_tabela(dados_filtrados)

    # conecta o botão ao comando
    buscarBtn.configure(command=aplicar_filtro)

    # ------------------ EXIBIÇÃO INICIAL (sem filtro) ------------------
    dados_iniciais = AnaliseCliente()  # sem mês/ano: mostra tudo
    preencher_tabela(dados_iniciais)
