import psycopg2

class Resources:

    def __init__(self, id, label, link):
        self.id = id
        self.label = label
        self.link = link


    def __str__(self):
        return "resource[{}]({}, {})".format(self.id, self.label, self.link)

    def __repr__(self):
        return str(self)

class ResourceService:
    def __init__(self, db_vars):
        self.connection = psycopg2.connect(
            host=db_vars["PG_HOST"], user=db_vars["PG_USER"],
            password=db_vars["PG_PASS"], port=db_vars["PG_PORT"],
            database=db_vars["PG_DB"]
        )

    def search_by_tag(self, id, *args):
        cursor = self.connection.cursor()
        str = 'tags_resources.tag_id = ' + id + ' '
        for i in args:
            str += 'AND tags_resources.tag_id = ' + i + ' '

        cursor.execute("SELECT resources.id, resources.label, resources.link FROM resources JOIN tags_resources WHERE %s",(str))

        return [Resources(*row) for row in cursor.fetchall()]

    def search_by_label(self, label):
        cursor = self.connection.cursor()
        cursor.execute("SELECT id, label, link FROM resources WHERE label LIKE '%(%s)%'",(label))

        return [Resource(*row) for row in cursor.fetchall()]

    def art_delete(self, id):
        cursor = self.connection.cursor()
        cursor.execute("DELETE id, label, link FROM resources WHERE id = %s",(id))
        cursor.execute("DELETE id, label, link FROM tags_resources WHERE resources_id = %s",(id))

    def art_create(self, label, link):
        cursor = self.connection.cursor()

        cursor.execute("INSERT INTO resources(label, link) VALUES (%s, %s)", (label, link))

    def update_add_tags(self, tag_id, resources_id):
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO tags_resources(tag_id, resources_id) VALUES (%s, %s)",(tag_id, resources_id))

    def update_delete_tags(self, tag_id):
        cursor = self.connection.cursor()
        cursor.execute("DELETE resources_id, tag_id FROM tags_resources WHERE tag_id = %s",(tag_id))

    # def update(self):
    #     cursor = self.connection.cursor()
    #     cursor.execute("UPDATE resources SET label = %s, link = %s WHERE id = %s",())
