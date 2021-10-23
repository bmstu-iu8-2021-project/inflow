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

    def add(self, label, color):
        self.label = label
        self.color = color
        cursor = self.connection.cursor()

        cursor.execute("INSERT INTO tags(label, color) VALUES (%s, %s)", (label, color))
        
    def edit(self):
        cursor = self.connection.cursor()
        cursor.execute("UPDATE tags SET label = %s, colour = %s WHERE label = %s",())

    def delete(self):
        cursor = self.connection.cursor()
        cursor.execute("DELETE * FROM tags WHERE label = %s",())
        cursor.execute("DELETE * FROM tags_resources WHERE tag_id = %s",())

    def search(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM tags WHERE label LIKE '%(%s)%'",())

        return [Tag(*row) for row in cursor.fetchall()]

    def join(self):
        cursor = self.connection.cursor()
        cursor.execute("UPDATE tags_resources SET tag_id = %s WHERE tag_id = %s and tag_id = %s",())
        cursor.execute("UPDATE tags SET label = %s WHERE label = %s",()) #меняем один из тегов новый
        cursor.execute("DELETE * FROM tags WHERE label = %s",()) #другой тег удаляем


    

class CreateTable:
        def __init__(self, db_vars):
            
        self.connection = psycopg2.connect(
            host=db_vars["PG_HOST"], user=db_vars["PG_USER"],
            password=db_vars["PG_PASS"], port=db_vars["PG_PORT"],
            database=db_vars["PG_DB"]
        )

        def table_for_tags(self):
            cursor = self.connection.cursor()

            cursor.execute("CREATE TABLE IF NOT EXISTS tags (Id SERIAL PRIMARY KEY, Label CHARACTER VARYING(30), colour CHARACTER VARYING(30) );")


        def table_for_resources(self):
            cursor = self.connection.cursor()

            cursor.execute("CREATE TABLE IF NOT EXISTS resources (Id SERIAL PRIMARY KEY, Label CHARACTER VARYING(70), Link CHARACTER VARYING(70));")

        def table_for_tags_resources(self):
            cursor = self.connection.cursor()

            cursor.execute("CREATE TABLE IF NOT EXISTS tags_recources (tag_id INTEGER, resources_id INTEGER, FOREIGN KEY (tag_id) REFERENCES tags(Id), FOREIGN KEY (resources_id) REFERENCES resources(Id));")    

    


 

