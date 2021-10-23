class ResourceService:
    def __init__(self, db_vars):
        self.connection = psycopg2.connect(
            host=db_vars["PG_HOST"], user=db_vars["PG_USER"],
            password=db_vars["PG_PASS"], port=db_vars["PG_PORT"],
            database=db_vars["PG_DB"]
        )

    def search_from_tags(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM resources WHERE tags_resources.resources_id",()) ???

        return [Tag(*row) for row in cursor.fetchall()]

    def search_from_label(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM resources WHERE label LIKE '%(%s)%'",())

        return [Resource(*row) for row in cursor.fetchall()]

    def delete(self):
        cursor = self.connection.cursor()
        cursor.execute("DELETE * FROM resources WHERE label = %s",())
        cursor.execute("DELETE * FROM tags_resources WHERE resources_id = %s",())

    def add(self, label, link):
        self.label = label
        self.link = link
        cursor = self.connection.cursor()

        cursor.execute("INSERT INTO resources(label, link) VALUES (%s, %s)", (label, link))

    def edit_add_tags(self):
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO tags_resources(tag_id, resources_id) VALUES (%s, %s),())

    def edit_delete_tags(self):
        cursor = self.connection.cursor()
        cursor.execute("DELETE * FROM tags_resources WHERE tag_id = %s",())

    def edit(self):
        cursor = self.connection.cursor()
        cursor.execute("UPDATE resources SET label = %s, link = %s WHERE id = %s",())
