import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv
import os

# Carrega o arquivo .env
load_dotenv()

# Lê as variáveis de ambiente
config = {
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASS")
}

def insert_tkt_id(conn):
    try:
        cur = conn.cursor()

        # Nome da tabela vindo do .env
        table = os.getenv("TKT_TABLE")

        # Monta query parametrizada com segurança
        insert_query = sql.SQL(
            "INSERT INTO {table} (tkt_id, totalInteractions, slachangecount, iscritical) VALUES (%s, %s, %s, %s)"
        ).format(table=sql.Identifier(table))

        # Dados de exemplo
        dados = (1, 123, 2, "False")
        
        print(f"Minha query {insert_query}")

        cur.execute(insert_query, dados)
        conn.commit()

        print("Registro inserido com sucesso!")

    except Exception as e:
        print("Erro ao inserir no banco:", e)

    finally:
        cur.close()


if __name__ == "__main__":
    try:
        # Conecta ao banco
        conn = psycopg2.connect(**config)

        insert_tkt_id(conn)

    finally:
        # Fecha a conexão
        conn.close()
