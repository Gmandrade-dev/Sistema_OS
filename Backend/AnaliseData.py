from Backend.DataClean import DataClean

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
    






