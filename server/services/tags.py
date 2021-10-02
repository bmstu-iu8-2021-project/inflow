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
            host=db_vars["PG_HOST"], user=db_vars["PG_USER"],
            password=db_vars["PG_PASS"], port=db_vars["PG_PORT"],
            database=db_vars["PG_DB"]
        )

    def all(self):
        cursor = self.connection.cursor()
    
        cursor.execute("SELECT id, label, color FROM tags")

        return [Tag(*row) for row in cursor.fetchall()]
 



if __name__ == "__main__":
    ENV = {
        "PG_USER": "inflow-client",
        "PG_PASS": "QwerTY",
        "PG_DB": "inflow",
        "PG_PORT":"5432",
    }

    tag_service = TagService(ENV)
    tags = tag_service.all()
    print(tags)
