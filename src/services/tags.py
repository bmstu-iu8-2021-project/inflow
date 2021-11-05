import psycopg2
from flask import jsonify

import sys
sys.path.append('..')

from models import Tag

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

        return jsonify([Tag(*row).__dict__ for row in cursor.fetchall()])

    def create(self, label, color):
        cursor = self.connection.cursor()

        cursor.execute("INSERT INTO tags(label, color) VALUES (%s, %s) RETURNING id;", (label, color))
        id = cursor.fetchone()[0]
        return Tag(id, label, color)
        
        
    # def update(self, id, edit_params):
    #     cursor = self.connection.cursor()
    #     cursor.execute("UPDATE tags SET label = %s, color = %s WHERE id = %s",())

    def delete(self, id):
        cursor = self.connection.cursor()
        cursor.execute("DELETE id, label, color FROM tags WHERE id = %s",(id))
        cursor.execute("DELETE resources_id, tag_id FROM tags_resources WHERE tag_id = %s",(id))

    def search(self, label):
        cursor = self.connection.cursor()
        cursor.execute("SELECT id, label, color FROM tags WHERE label LIKE '%(%s)%'",(label))

        return [Tag(*row) for row in cursor.fetchall()]

    def join(self, id_src, id_dst):
        cursor = self.connection.cursor()
        cursor.execute("UPDATE tags_resources SET tag_id = %s WHERE tag_id = %s",(id_dst, id_src))
        cursor.execute("DELETE id, label, color FROM tags WHERE id = %s",(id_src)) #другой тег удаляем

    


    

class CreateTable:
        def __init__(self, db_vars):
            
            self.connection = psycopg2.connect(
                host=db_vars["PG_HOST"], user=db_vars["PG_USER"],
                password=db_vars["PG_PASS"], port=db_vars["PG_PORT"],
                database=db_vars["PG_DB"]
            )

        def table_for_tags(self):
            cursor = self.connection.cursor()

            cursor.execute("CREATE TABLE IF NOT EXISTS tags (id SERIAL PRIMARY KEY, label CHARACTER VARYING(30), color CHARACTER VARYING(30) );")


        def table_for_resources(self):
            cursor = self.connection.cursor()

            cursor.execute("CREATE TABLE IF NOT EXISTS resources (id SERIAL PRIMARY KEY, label CHARACTER VARYING(70), link TEXT);")

        def table_for_tags_resources(self):
            cursor = self.connection.cursor()

            cursor.execute("CREATE TABLE IF NOT EXISTS tags_recources (tag_id INTEGER, resources_id INTEGER, FOREIGN KEY (tag_id) REFERENCES tags(Id), FOREIGN KEY (resources_id) REFERENCES resources(Id));")    

    


 

