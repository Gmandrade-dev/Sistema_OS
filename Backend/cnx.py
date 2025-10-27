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
            query = f"SELECT * FROM {tabela}"
            cursor.execute(query)
            resultados = cursor.fetchall()
                  
            colunas = [desc[0] for desc in cursor.description]
            df = pd.DataFrame(resultados, columns=colunas)
            
            # Salva em Excel
            df.to_excel(f"{tabela}.xlsx", index=False)
            print(df)
            
            cursor.close()
            conexao.close()
        except sql.Error as e:
            print(f"Erro ao carregar dados: {e}")

# Exemplo de uso

# carregar_dados('tb_usuario')

carregar_dados('tb_os')