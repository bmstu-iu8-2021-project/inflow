import psycopg2
from flask import jsonify

import sys
sys.path.append('..')

from models import Tag
from utils import Singleton


class TagService(metaclass=Singleton):

    def __init__(self, pool):
        self.pool = pool
        

    def all(self):
        conn = self.pool.getconn()
        cursor = conn.cursor()
        cursor.execute("SELECT id, label, color FROM tags;")
        result = [Tag(*row).__dict__ for row in cursor.fetchall()]
        cursor.close()
        self.pool.putconn(conn)
        return result

    def create(self, label, color):
        conn = self.pool.getconn()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tags(label, color) VALUES (%s, %s) RETURNING id;", (label, color))
        id = cursor.fetchone()[0]
        tag = Tag(id, label, color)
        cursor.close()
        self.pool.putconn(conn)
        # return [Tag(*row).__dict__ for row in cursor.fetchall()]
        return tag.__dict__
        
    # def update(self, id, edit_params):
    #     conn = self.pool.getconn()
        # cursor = conn.cursor()
    #     cursor.execute("UPDATE tags SET label = %s, color = %s WHERE id = %s",())

    def delete(self, id):
        conn = self.pool.getconn()
        cursor = conn.cursor()
        cursor.execute("DELETE id, label, color FROM tags WHERE id = %s;",(id))
        cursor.execute("DELETE resources_id, tag_id FROM tags_resources WHERE tag_id = %s;",(id))
        cursor.close()
        self.pool.putconn(conn)

    def search(self, label):
        conn = self.pool.getconn()
        cursor = conn.cursor()
        cursor.execute("SELECT id, label, color FROM tags WHERE label LIKE '%(%s)%';",(label))
        result = [Tag(*row).__dict__ for row in cursor.fetchall()]
        cursor.close()
        self.pool.putconn(conn)
        return result

    def join(self, id_src, id_dst):
        conn = self.pool.getconn()
        cursor = conn.cursor()
        cursor.execute("UPDATE tags_resources SET tag_id = %s WHERE tag_id = %s;",(id_dst, id_src))
        cursor.execute("DELETE id, label, color FROM tags WHERE id = %s;",(id_src)) #другой тег удаляем
        cursor.close()
        self.pool.putconn(conn)
