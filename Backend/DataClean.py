from Backend.cnx import carregar_dados
import pandas as pd

def DataClean(tabela):
    df = carregar_dados(tabela)

    if tabela == 'tb_os':
        colunas_remover = [
            'id_fatura', 'pagamento_terceiros',
            'id_usuario_externo', 'email_externo', 'telefone_externo',
            'nome_externo','id_funcionario_10','id_funcionario_9','id_funcionario_8',
            'valor_final','data_recebimento','data_solicitacao','envio_email','responsavel_cliente',
            'data_edicao','id_usuario_edicao','id_aceite','id_funcionario_7',
            'data_agendamento','crio','orcamento','compra','cadastro','qualidade','marketing',
            'os','id_colaborador','data_envio_terceiros','data_retorno_terceiros','motivo_cancelamento','nome_razao',
            'funcionario_1','funcionario_2','funcionario_3','funcionario_4','funcionario_5','funcionario_6'
        ]

        if 'hh' in df.columns:
            df['hh'] = pd.to_timedelta(df['hh'], unit='d', errors='coerce')
            df['hh'] = df['hh'].astype(str).str.split().str[-1]
            df['hh'] = df['hh'].replace('00:00:00', '00:12:00')
        df['terceiros'].fillna('IW')

    elif tabela == 'tb_usuario':
        colunas_remover = [
            'perm_os','perm_frota','perm_adm','perm_modulos',
            'perm_almox','perm_manut','perm_doc','perm_req_material',
            'perm_financeiro','somente_leitura','perm_ti','limite_compra',
            'perm_lider','unidade','perm_logistica','perm_os_oficina',
            'perm_combustivel','perm_dashboard','extorno','del_os',
            'boss', 'perm_liberar_sol','perm_retroativo','del_prod',
            'perm_medicao','perm_ext_can','almox_master','crio','orcamento',
            'cadastro','qualidade','fabrica','marketing','id_colaborador','compra','os'
        ]

        
        for col in ['ultimo_login', 'data_nascimento']:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors='coerce').fillna(pd.Timestamp('2025-02-02'))
                df[col] = df[col].dt.strftime('%Y-%m-%d')

        if 'senha_usuario' in df.columns:
            df['senha_usuario'] = '******'

    elif tabela == 'tb_cliente':
        colunas_remover = [
            'ie','im','cep','contato_1','contato_2','email','email_a1','email_a2','email_a3',
            'contribuinte','segmento','cnae_principal','cnae_secundario','id_tipo','observacao',
            'tipo_cliente','senhas_obs','apelido','ativo_envio_email','email_envio','bairro'
        ]

    elif tabela == 'tb_fornecedor':
        colunas_remover = [ 
            'ie','im','cep','contato_1','contato_2','email','contribuinte','segmento',
            'cnae_principal','cnae_secundario','id_tipo','observacao','tipo_fornecedor',
            'senhas_obs','apelido','ativo_envio_email','email_envio','numero','complemento',
            'email_a1','email_a2','email_a3','logradouro','bairro','cidade','contato_nome','tipo'
        ]

    else:
        colunas_remover = []
        print("Tabela não reconhecida.")

   
    df = df.drop(columns=colunas_remover, errors='ignore')
    return df



