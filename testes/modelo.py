import customtkinter as ctk

# ==========================
# Configuração principal
# ==========================
ctk.set_appearance_mode("light")  # Tema claro
ctk.set_default_color_theme("blue")  # Tema de cor

app = ctk.CTk()
app.geometry("1000x600")
app.title("Dashboard - InforWay")

# ==========================
# Funções para trocar telas
# ==========================
def limpar_tela():
    for widget in content.winfo_children():
        widget.destroy()

def mostrar_resumo():
    limpar_tela()
    lbl = ctk.CTkLabel(content, text="📊 Tela de Resumo", font=("Arial", 20))
    lbl.pack(pady=20)

def mostrar_ranking_clientes():
    limpar_tela()
    lbl = ctk.CTkLabel(content, text="🏆 Ranking de Clientes", font=("Arial", 20))
    lbl.pack(pady=20)

def mostrar_ranking_colaboradores():
    limpar_tela()
    lbl = ctk.CTkLabel(content, text="👨‍💻 Ranking de Colaboradores", font=("Arial", 20))
    lbl.pack(pady=20)

def mostrar_analise_temporal():
    limpar_tela()
    lbl = ctk.CTkLabel(content, text="⏳ Análise Temporal", font=("Arial", 20))
    lbl.pack(pady=20)

# ==========================
# Layout principal
# ==========================
frame_dashboard = ctk.CTkFrame(app)
frame_dashboard.pack(fill="both", expand=True)

# Sidebar (menu lateral)
sidebar = ctk.CTkFrame(frame_dashboard, width=200, corner_radius=0)
sidebar.pack(side="left", fill="y")

# Content (área principal)
content = ctk.CTkFrame(frame_dashboard, fg_color="white")
content.pack(side="left", fill="both", expand=True)

# ==========================
# Widgets da sidebar
# ==========================
logo = ctk.CTkLabel(sidebar, text="InforWay\nInformática", font=("Arial Bold", 16))
logo.pack(pady=(30, 50))

btn_resumo = ctk.CTkButton(sidebar, text="Resumo", command=mostrar_resumo)
btn_resumo.pack(pady=10, fill="x", padx=20)

btn_ranking_clientes = ctk.CTkButton(sidebar, text="Ranking Clientes", command=mostrar_ranking_clientes)
btn_ranking_clientes.pack(pady=10, fill="x", padx=20)

btn_ranking_colaboradores = ctk.CTkButton(sidebar, text="Ranking Colaboradores", command=mostrar_ranking_colaboradores)
btn_ranking_colaboradores.pack(pady=10, fill="x", padx=20)

btn_analise_temporal = ctk.CTkButton(sidebar, text="Análise Temporal", command=mostrar_analise_temporal)
btn_analise_temporal.pack(pady=10, fill="x", padx=20)

btn_sair = ctk.CTkButton(sidebar, text="Sair", fg_color="red", command=app.destroy)
btn_sair.pack(side="bottom", pady=20, padx=20, fill="y")

# ==========================
# Tela inicial
# ==========================
mostrar_resumo()

app.mainloop()
