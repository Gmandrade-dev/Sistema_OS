import customtkinter as ctk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def Resumo(content):
    # ----------- CRIANDO DATAFRAME DE EXEMPLO -----------
    dados = {
        "id_os": range(1, 13),
        "data_criacao": pd.date_range("2025-01-10", periods=12, freq="15D"),
        "data_conclusao": pd.date_range("2025-01-20", periods=12, freq="15D"),
        "usuario_responsavel": ["João", "Maria", "Carlos", "João", "Maria", "Maria",
                                "Carlos", "João", "João", "Maria", "Carlos", "João"],
        "cliente": ["ACME", "SoftPlus", "TechMax", "ACME", "TechMax", "SoftPlus",
                    "TechMax", "ACME", "ACME", "SoftPlus", "SoftPlus", "TechMax"]
    }
    df = pd.DataFrame(dados)

    # ----------- ANÁLISES COM PANDAS -----------
    df['data_criacao'] = pd.to_datetime(df['data_criacao'])
    df['data_conclusao'] = pd.to_datetime(df['data_conclusao'])
    df['ano_mes'] = df['data_criacao'].dt.to_period('M')
    df['tempo_execucao'] = (df['data_conclusao'] - df['data_criacao']).dt.days

    os_por_usuario = df.groupby('usuario_responsavel')['id_os'].count().reset_index(name='total_os')
    os_por_cliente = df.groupby('cliente')['id_os'].count().reset_index(name='total_os')
    os_por_mes = df.groupby('ano_mes')['id_os'].count().reset_index(name='total_os')
    tempo_medio_usuario = df.groupby('usuario_responsavel')['tempo_execucao'].mean().reset_index(name='tempo_medio_dias')

    # ----------- INTERFACE PRINCIPAL (SCROLL) -----------
    scroll = ctk.CTkScrollableFrame(content, width=850, height=600)
    scroll.pack(fill="both", expand=True, padx=10, pady=10)

    ctk.CTkLabel(scroll, text="📊 Resumo de Ordens de Serviço", font=("Arial", 28, "bold")).pack(pady=10)

    # Função auxiliar para criar uma mini seção scrollável
    def criar_tabela_scroll(parent, titulo, dados, col1, col2, fmt=None):
        section = ctk.CTkFrame(parent, fg_color="#f2f2f2")
        section.pack(pady=10, fill="x", expand=True)
        ctk.CTkLabel(section, text=titulo, font=("Arial", 20, "bold")).pack(pady=5)
        subscroll = ctk.CTkScrollableFrame(section, height=150)
        subscroll.pack(padx=10, pady=5, fill="x", expand=True)

        # Cabeçalho
        header = ctk.CTkFrame(subscroll, fg_color="#cccccc")
        header.pack(fill="x")
        ctk.CTkLabel(header, text=col1, width=200, anchor="w", font=("Arial", 14, "bold")).pack(side="left", padx=10)
        ctk.CTkLabel(header, text=col2, width=100, anchor="center", font=("Arial", 14, "bold")).pack(side="left")

        # Linhas
        for _, row in dados.iterrows():
            linha = ctk.CTkFrame(subscroll, fg_color="#ffffff")
            linha.pack(fill="x", pady=2)
            ctk.CTkLabel(linha, text=row[col1.lower()], width=200, anchor="w", font=("Arial", 13)).pack(side="left", padx=10)
            val = row[col2.lower()]
            if fmt == "float":
                val = f"{val:.1f}"
            ctk.CTkLabel(linha, text=val, width=100, anchor="center", font=("Arial", 13)).pack(side="left")

    # --- 1️⃣ OS por Usuário ---
    criar_tabela_scroll(scroll, "1️⃣ OS por Usuário", os_por_usuario.rename(columns={
        "usuario_responsavel": "usuario", "total_os": "total"
    }), "Usuario", "Total")

    # --- 2️⃣ OS por Cliente ---
    criar_tabela_scroll(scroll, "2️⃣ OS por Cliente", os_por_cliente.rename(columns={
        "cliente": "cliente", "total_os": "total"
    }), "Cliente", "Total")

    # --- 3️⃣ Tempo médio de execução ---
    criar_tabela_scroll(scroll, "3️⃣ Tempo Médio (dias)", tempo_medio_usuario.rename(columns={
        "usuario_responsavel": "usuario", "tempo_medio_dias": "tempo"
    }), "Usuario", "Tempo", fmt="float")

    # --- 4️⃣ Gráfico de OS por mês ---
    ctk.CTkLabel(scroll, text="4️⃣ OS Criadas por Mês", font=("Arial", 20, "bold")).pack(pady=10)
    fig, ax = plt.subplots(figsize=(6, 3))
    ax.plot(os_por_mes['ano_mes'].astype(str), os_por_mes['total_os'], marker='o', color="#1f77b4")
    ax.set_title("OS por Mês")
    ax.set_xlabel("Mês")
    ax.set_ylabel("Quantidade")
    ax.grid(True)
    canvas = FigureCanvasTkAgg(fig, master=scroll)
    canvas.draw()
    canvas.get_tk_widget().pack(pady=10)


# ----------- JANELA PRINCIPAL -----------
if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    app = ctk.CTk()
    app.title("Resumo OS - Scrollable Sem Treeview")
    app.geometry("900x700")

    frame = ctk.CTkFrame(app)
    frame.pack(fill="both", expand=True, padx=10, pady=10)

    Resumo(frame)

    app.mainloop()
