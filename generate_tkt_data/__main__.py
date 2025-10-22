import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv
from random import randint
from datetime import timedelta
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
        
        tkk_id = 1
        
        clients_count = 400
        
        for client_id in range(1, clients_count + 1):
            for ii in range(90, 500):
                
                insert_query = sql.SQL(
                    "INSERT INTO {table} (tkt_id, clientid, totalInteractions, slachangecount, iscritical, timetoresolve) VALUES (%s, %s, %s, %s, %s, %s)"
                ).format(table=sql.Identifier(table))
                
                totalInteractions = randint(3,12)
                
                slachangecount = randint(1,4)
                
                int_is_critical = randint(1,10)
                bool_is_critical = int_is_critical == 1
                
                horas = randint(0,168)
                minutos = randint(0,59)
                
                teste = f"{horas}:{minutos}"
        
                tkt_data = (tkk_id, client_id, totalInteractions, slachangecount, bool_is_critical, teste)
                
                tkk_id += 1
                
                cur.execute(insert_query, tkt_data)
        
        
            
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
