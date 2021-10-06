import psycopg2

class Tag:

    def __init__(self, id, label, color):
        self.id = id
        self.label = label
        self.color = color


    def __str__(self):
        return "tag[{}]({}, {})".format(self.id, self.label, self.color)

    def __repr__(self):
        return str(self)


class TagService:

    def __init__(self, db_vars):
        self.connection = psycopg2.connect(
            host=db_vars["PG_HOST"],
            port=db_vars["PG_PORT"],
            user=db_vars["PG_USER"],
            password=db_vars["PG_PASS"],
            database=db_vars["PG_DB"]
        )

    def all(self):
        cursor = self.connection.cursor()
    
        cursor.execute("SELECT id, label, color FROM tags")

        return [Tag(*row) for row in cursor.fetchall()]
 

