import customtkinter as ctk
from view.components.AreaSidebar import AreaSidebar
from view.components.Resumo import Resumo

def Dashboard(app, limpar_tela):

    frame_dashboard = ctk.CTkFrame(app)
    frame_dashboard.pack(fill="both", expand=True)
    
    sidebar = ctk.CTkFrame(frame_dashboard, width=300,corner_radius=0)
    sidebar.pack(side="left", fill="y" )
    sidebar.pack_propagate(False)

    content = ctk.CTkFrame(frame_dashboard, fg_color="white")
    content.pack(side="left", fill="both", expand=True)

    AreaSidebar(sidebar,content,limpar_tela)
    Resumo(content,lambda: (limpar_tela(content)))

    


  

