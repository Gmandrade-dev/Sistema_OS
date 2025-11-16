import pandas as pd
import mysql.connector as sql

def conectar():
    try:
        conexao = sql.connect(
            host='162.241.63.9',
            user='hgin6423_admin',
            password='iway@2023',
            database='hgin6423_inforway'
        )
        # print("Conexão bem-sucedida ao banco de dados.")
        return conexao
    
    except sql.Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return False


def carregar_dados(tabela):
    conexao = conectar()
    if conexao:
        try:
            cursor = conexao.cursor()

            if tabela == 'tb_os':
                query = """
                SELECT 
                    os.id_os,
                    os.data_criacao,
                    os.data_entrada,
                    os.data_inicio,
                    os.data_conclusao,
                    os.status,
                    os.descricao,
                    os.acessorios,
                    os.tipo,
                    os.num_os,
                    os.hh,
                    
                    -- Usuário principal
                    u.nome_usuario AS usuario_responsavel,
                    
                    -- Cliente
                    c.nome_fantasia AS cliente,
                    
                    -- Terceiros / Fornecedor
                    f.nome_fantasia AS terceiros,
                    
                    -- Funcionários envolvidos
                    fu1.nome_usuario AS funcionario_1,
                    fu2.nome_usuario AS funcionario_2,
                    fu3.nome_usuario AS funcionario_3,
                    fu4.nome_usuario AS funcionario_4,
                    fu5.nome_usuario AS funcionario_5,
                    fu6.nome_usuario AS funcionario_6

                FROM tb_os AS os
                LEFT JOIN tb_usuario AS u  ON os.id_usuario = u.id_usuario
                LEFT JOIN tb_cliente AS c   ON os.id_cliente = c.id_cliente
                LEFT JOIN tb_fornecedor AS f ON os.id_terceiros = f.id_cliente

                LEFT JOIN tb_usuario AS fu1 ON os.id_funcionario_1 = fu1.id_usuario
                LEFT JOIN tb_usuario AS fu2 ON os.id_funcionario_2 = fu2.id_usuario
                LEFT JOIN tb_usuario AS fu3 ON os.id_funcionario_3 = fu3.id_usuario
                LEFT JOIN tb_usuario AS fu4 ON os.id_funcionario_4 = fu4.id_usuario
                LEFT JOIN tb_usuario AS fu5 ON os.id_funcionario_5 = fu5.id_usuario
                LEFT JOIN tb_usuario AS fu6 ON os.id_funcionario_6 = fu6.id_usuario
                """
            else:
                query = f"SELECT * FROM {tabela}"

            cursor.execute(query)
            resultados = cursor.fetchall()
            colunas = [desc[0] for desc in cursor.description]
            
            import pandas as pd
            df = pd.DataFrame(resultados, columns=colunas)
            # df.to_excel(f'{tabela}.xlsx', index=False)

            cursor.close()
            conexao.close()

            return df

        except sql.Error as e:
            print(f"Erro ao carregar dados: {e}")


