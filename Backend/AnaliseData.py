from Backend.DataClean import DataClean

def GetData(tabela):
    if not tabela:
        print(" Nenhuma tabela informada.")
        return None

    tabelas_validas = ['tb_os', 'tb_usuario', 'tb_cliente', 'tb_fornecedor']

    if tabela not in tabelas_validas:
        print(f" Tabela '{tabela}' não reconhecida. Opções válidas: {tabelas_validas}")
        return None

    df = DataClean(tabela)
    return df


def AnaliseResumo():
    dfOs = GetData('tb_os')
    dfClientes = GetData('tb_cliente')
    dfUsuarios = GetData('tb_usuario')
    dados = {}

    totalOS = len(dfOs)
    concluidas = (dfOs['status'] == 'Concluida').sum()
    users = (dfUsuarios['ativo_usuario'] == 1).sum()
    clientes = len(dfClientes)
    

    dados = {
        'totalOs': totalOS,
        'concluidas': concluidas,
        'users': users,
        'clientes': clientes
    }

    return dados
    






