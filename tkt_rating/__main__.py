import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv
import os

load_dotenv()

config = {
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASS")
}

def tkt_rating(conn):
    try:
        cur = conn.cursor()
        
        tkt_table = os.getenv("TKT_TABLE")
        ratings_table = os.getenv("RATINGS_TABLE")
        
        rating = sql.SQL(
            """
            INSERT INTO {ratings_table} (
                tkt_id,
                clientid,
                totalinteractions_score,
                sla_score,
                criticality_score,
                resolution_time_score
            )
            SELECT
                data.tkt_id,
                data.clientid,
                
                CASE 
                    WHEN data.totalinteractions <= 3 THEN 20
                    WHEN data.totalinteractions > 3 and data.totalinteractions <= 5 THEN 15
                    WHEN data.totalinteractions > 5 and data.totalinteractions <= 7 THEN 7
                    ELSE 0
                end as totalinteractions_score,
                
                CASE 
                    WHEN data.slachangecount < 3 THEN 20
                    WHEN data.slachangecount = 3 THEN 15
                    ELSE 10
                end as sla_score,

                
                CASE WHEN data.iscritical THEN 0 ELSE 10 END AS criticality_score,
                
                GREATEST(0, 20 - (EXTRACT(EPOCH FROM data.timetoresolve) / 3600) / 16.8) AS resolution_time_score
            FROM {tkt_table} AS data
            """
        ).format(
            ratings_table=sql.Identifier(ratings_table),
            tkt_table=sql.Identifier(tkt_table)
        )
        
        cur.execute(rating)
        conn.commit()
        cur.close()
        
        print("Ticket ratings inseridos com sucesso.")
    
    except Exception as e:
        print("Erro ao inserir ticket ratings:", e)
        conn.rollback()
        
        
if __name__ == "__main__":
    try:
        # Conecta ao banco
        conn = psycopg2.connect(**config)
        tkt_rating(conn)
    finally:
        # Fecha a conexão
        conn.close()
