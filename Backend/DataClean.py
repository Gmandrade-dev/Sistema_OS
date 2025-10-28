from cnx import carregar_dados
import pandas as pd

def DataClean(tabela):
    df = carregar_dados(tabela)

    if tabela == 'tb_os':
        # Ver informações iniciais
     
        colunas_remover = [
        'id_fatura', 'pagamento_terceiros',
        'id_usuario_externo', 'email_externo', 'telefone_externo',
        'nome_externo','id_funcionario_10','id_funcionario_9','id_funcionario_8',
        'valor_final','data_recebimento','data_solicitacao','envio_email','responsavel_cliente',
        'data_edicao','id_usuario_edicao','id_aceite','id_funcionario_7',
        'data_agendamento'
        ]
    elif tabela == 'tb_usuario':
        colunas_remover = [
            'id_usuario_externo', 'email_externo', 'telefone_externo',
            'nome_externo', 'data_ultimo_login', 'status'
        ]
    else:
        colunas_remover = []
        print("Não achamos dados")

    df = df.drop(columns=colunas_remover, errors='ignore')

    df = df.fillna('0')
    # Ver informações finais
    df.to_excel(f"{tabela}_limpo.xlsx", index=False)
    print(df)
    
    return df


# Teste
tabela = 'tb_os'
DataClean(tabela)
