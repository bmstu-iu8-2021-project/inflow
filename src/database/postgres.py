import psycopg2
from psycopg2 import pool


def get_postgres_conn_pool(params: dict):
    return psycopg2.pool.SimpleConnectionPool(
            1, 42,
            host=params["PG_HOST"],
            port=params["PG_PORT"],
            user=params["PG_USER"],
            password=params["PG_PASS"],
            database=params["PG_DB"]
        )


def create_schema(pool, filepath):
    conn = pool.getconn()

    with open(filepath, 'r') as file:
        with conn.cursor() as cursor:
            schema_sql = file.read()
            print(schema_sql)
            cursor.execute(schema_sql)
            conn.commit()
    
    pool.putconn(conn)

