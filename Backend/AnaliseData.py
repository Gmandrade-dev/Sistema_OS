from Backend.DataClean import DataClean
import pandas as pd
import numpy as np

cache = {}

# -----------------------------------------------------------
# GETDATA — CACHE
# -----------------------------------------------------------
def GetData(tabela):
    global cache

    if tabela in cache:
        return cache[tabela]

    df = DataClean(tabela)
    cache[tabela] = df
    return df



# -----------------------------------------------------------
# RESUMO GERAL
# -----------------------------------------------------------
def AnaliseResumo():
    dfOs = GetData('tb_os')
    totalOS = len(dfOs)
    concluidas = (dfOs['status'] == 'Concluida').sum()

    dfClientes = GetData('tb_cliente')
    clientes = len(dfClientes)

    dfUsuarios = GetData('tb_usuario')
    users = (dfUsuarios['ativo_usuario'] == 1).sum()

    return {
        'totalOs': totalOS,
        'concluidas': concluidas,
        'users': users,
        'clientes': clientes
    }



# -----------------------------------------------------------
# ANÁLISE CLIENTES
# -----------------------------------------------------------
def AnaliseCliente(mes=None, ano=None):

    dfos = GetData('tb_os').copy()
    dfos["data_criacao"] = pd.to_datetime(dfos["data_criacao"], errors="coerce")

    # FILTROS
    if mes and ano:
        dfos = dfos[(dfos["data_criacao"].dt.month == mes) &
                    (dfos["data_criacao"].dt.year == ano)]
    elif ano:
        dfos = dfos[dfos["data_criacao"].dt.year == ano]
    elif mes:
        dfos = dfos[dfos["data_criacao"].dt.month == mes]

    # total geral
    clienteOS = (
        dfos.groupby("cliente")["id_os"]
        .count()
        .sort_values(ascending=False)
        .head(200)
    )

    # BLACK WHITE
    terceirosOS = (
        dfos[dfos["terceiros"] == "BLACK WHITE"]
        .groupby("cliente")["id_os"]
        .count()
        .sort_values(ascending=False)
        .head(200)
    )

    dados = {}
    for cliente, total_os in clienteOS.items():
        dados[cliente] = {
            "total_os": int(total_os),
            "blackwhite": int(terceirosOS.get(cliente, 0))
        }

    return dados


# -----------------------------------------------------------
# ANÁLISE COLABORADORES (NOVO)
# -----------------------------------------------------------
def AnaliseColaboradores(mes=None, ano=None):
    """
    Retorna dict:
    {
      "Nome Usuario": {
          "total_os": int,
          "tempo_medio": "HH:MM"   # média apenas de OS concluídas com data_inicio e data_conclusao válidos
      },
      ...
    }

    Filtra por mes/ano em data_criacao (mes/ano podem ser None).
    """
    dfos = GetData('tb_os').copy()
    # parse datas
    dfos["data_criacao"] = pd.to_datetime(dfos["data_criacao"], errors="coerce")
    dfos["data_inicio"] = pd.to_datetime(dfos["data_inicio"], errors="coerce")
    dfos["data_conclusao"] = pd.to_datetime(dfos["data_conclusao"], errors="coerce")

    # aplicar filtros por mes/ano (se fornecidos) sobre data_criacao
    if mes is not None:
        dfos = dfos[dfos["data_criacao"].dt.month == mes]
    if ano is not None:
        dfos = dfos[dfos["data_criacao"].dt.year == ano]

    # total de OS por usuario_responsavel (conta todas as OS)
    total_por_usuario = (
        dfos.groupby("usuario_responsavel")["id_os"]
        .count()
        .sort_values(ascending=False)
    )

    # Para tempo médio: considerar apenas OS concluídas com data_inicio e data_conclusao válidas
    df_concluidas = dfos[
        (dfos["status"] == "Concluida") &
        (~dfos["data_inicio"].isna()) &
        (~dfos["data_conclusao"].isna())
    ].copy()

    # calcular delta em segundos
    if not df_concluidas.empty:
        df_concluidas["duracao_segundos"] = (df_concluidas["data_conclusao"] - df_concluidas["data_inicio"]).dt.total_seconds()
    else:
        df_concluidas["duracao_segundos"] = pd.Series(dtype=float)

    tempo_medio_por_usuario = (
        df_concluidas.groupby("usuario_responsavel")["duracao_segundos"]
        .mean()
    )

    # montar dicionário final
    dados = {}
    # iterando sobre todos os usuários que apareceram em total_por_usuario (preserva ordenação)
    for usuario, total in total_por_usuario.items():
        duracao_media_seg = tempo_medio_por_usuario.get(usuario, np.nan)

        if pd.isna(duracao_media_seg):
            tempo_medio_str = "—"
        else:
            # formatar como H:MM
            # redondear para inteiro de segundos para formatação limpa
            seg = int(round(duracao_media_seg))
            horas = seg // 3600
            minutos = (seg % 3600) // 60
            tempo_medio_str = f"{horas:02d}:{minutos:02d}"

        dados[usuario] = {
            "total_os": int(total),
            "tempo_medio": tempo_medio_str
        }

    # Se existirem usuários em tempo_medio_por_usuario que não aparecem em total_por_usuario
    # (caso raro), adicioná-los
    for usuario in tempo_medio_por_usuario.index:
        if usuario not in dados:
            seg = int(round(tempo_medio_por_usuario[usuario]))
            horas = seg // 3600
            minutos = (seg % 3600) // 60
            tempo_medio_str = f"{horas:02d}:{minutos:02d}"
            dados[usuario] = {
                "total_os": int(0),
                "tempo_medio": tempo_medio_str
            }

    # ordenar por total_os decrescente antes de retornar
    dados_ordenados = dict(sorted(dados.items(), key=lambda x: x[1]["total_os"], reverse=True))

    return dados_ordenados


# -----------------------------------------------------------
# ANÁLISE MENSAL POR COLABORADOR (NOVO)
# -----------------------------------------------------------
def AnaliseColaboradorMensal(colaborador, ano=None):
    """
    Retorna dict com contagem de OS por mês para um colaborador:
    {
      "Janeiro": 12,
      "Fevereiro": 5,
      ...
    }
    Se colaborador for None ou 'Todos', retorna agregação de todos.
    """
    meses_nome = {
        1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril",
        5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto",
        9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"
    }

    dfos = GetData('tb_os').copy()
    dfos["data_criacao"] = pd.to_datetime(dfos["data_criacao"], errors="coerce")

    # filtro por colaborador (se fornecido)
    if colaborador and colaborador != "Todos":
        dfos = dfos[dfos["usuario_responsavel"] == colaborador]

    # filtro por ano (se fornecido)
    if ano is not None:
        dfos = dfos[dfos["data_criacao"].dt.year == ano]

    # contar por mês (1..12)
    contagem = dfos.groupby(dfos["data_criacao"].dt.month)["id_os"].count().to_dict()

    # montar resultado garantindo todos os meses presentes (0 se faltante)
    resultado = {}
    for m in range(1, 13):
        nome = meses_nome[m]
        resultado[nome] = int(contagem.get(m, 0))

    return resultado
