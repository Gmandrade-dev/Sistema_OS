from Backend.DataClean import DataClean
import pandas as pd
cache = {} 

def GetData(tabela):
    global cache

    if tabela in cache:
        return cache[tabela]

    df = DataClean(tabela)
    cache[tabela] = df
    return df


def AnaliseResumo():
    dfOs = GetData('tb_os')
    totalOS = len(dfOs)
    concluidas = (dfOs['status'] == 'Concluida').sum()

    dfClientes = GetData('tb_cliente')
    clientes = len(dfClientes)

    dfUsuarios = GetData('tb_usuario')
    users = (dfUsuarios['ativo_usuario'] == 1).sum()
    
    dados = {
        'totalOs': totalOS,
        'concluidas': concluidas,
        'users': users,
        'clientes': clientes
    }

    return dados
    
def AnaliseCliente(mes=None, ano=None):

    dfos = GetData('tb_os')

    # Converter data (correção do seu erro)
    dfos["data_criacao"] = pd.to_datetime(dfos["data_criacao"], errors="coerce")

    # Aplicar filtro somente se mês e ano forem informados
    if mes is not None and ano is not None:
        dfos = dfos[
            (dfos["data_criacao"].dt.month == mes) &
            (dfos["data_criacao"].dt.year == ano)
        ]

    # Quantidade total de OS por cliente
    clienteOS = (
        dfos.groupby("cliente")["id_os"]
        .count()
        .sort_values(ascending=False)
        .head(200)
    )

    # Quantas vezes foi para "BLACK WHITE"
    terceirosOS = (
        dfos[dfos["terceiros"] == "BLACK WHITE"]
        .groupby("cliente")["id_os"]
        .count()
        .sort_values(ascending=False)
        .head(200)
    )

    dados = {}

    # Montar estrutura final
    for cliente, total_os in clienteOS.items():
        dados[cliente] = {
            "total_os": int(total_os),
            "blackwhite": int(terceirosOS.get(cliente, 0))
        }

    return dados
