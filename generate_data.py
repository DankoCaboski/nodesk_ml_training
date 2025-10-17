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

try:
    # Conecta ao banco
    conn = psycopg2.connect(**config)
    cur = conn.cursor()

    # Exemplo de insert
    insert_query = sql.SQL("""
        INSERT INTO minha_tabela (coluna1, coluna2, coluna3)
        VALUES (%s, %s, %s)
    """)
    dados = ("valor1", 123, "outro valor")

    cur.execute(insert_query, dados)
    conn.commit()

    print("✅ Registro inserido com sucesso!")

except Exception as e:
    print("❌ Erro ao inserir no banco:", e)

finally:
    if conn:
        cur.close()
        conn.close()
