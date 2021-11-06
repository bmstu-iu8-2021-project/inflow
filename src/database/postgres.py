import psycopg2


def get_postgres_conntection(params: dict):
    return psycopg2.connect(
            host=params["PG_HOST"],
            port=params["PG_PORT"],
            user=params["PG_USER"],
            password=params["PG_PASS"],
            database=params["PG_DB"]
        )


def create_schema(conn, filepath):
    cursor = conn.cursor()

    with open(filepath, 'r') as file:
        schema_sql = file.read()
        cursor.execute(schema_sql)
