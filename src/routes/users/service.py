import psycopg2
from flask import jsonify

import sys

from models.user import User
sys.path.append('..')

from models import User
from utils import Singleton


class UserService(metaclass=Singleton):

    def __init__(self, pool):
        self.pool = pool

    def create(self, login, password):
        try:
            conn = self.pool.getconn()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (login, password) VALUES (%s, %s) RETURNING id;", (login, password))
            id = cursor.fetchone()[0]
            
            conn.commit()
            
            user = User(id, login, password)
            cursor.close()
            self.pool.putconn(conn)
            return [User(*row).__dict__ for row in cursor.fetchall()]
            # return user.__dict__
        except:
            return "oops"
        
    # def update(self, id, edit_params):
    #     conn = self.pool.getconn()
        # cursor = conn.cursor()
    #     cursor.execute("UPDATE tags SET label = %s, color = %s WHERE id = %s",())

    def delete(self, id):
        try:
            conn = self.pool.getconn()
            cursor = conn.cursor()
            cursor.execute("DELETE id, login, password FROM users WHERE id = %s;",(id))
            # cursor.execute("DELETE resources_id, tag_id FROM tags_resources WHERE tag_id = %s;",(id))
            conn.commit()
            cursor.close()
            self.pool.putconn(conn)
        except:
            return "oops"

    def get(self, id):
        try:
            conn = self.pool.getconn()
            cursor = conn.cursor()
            cursor.execute("SELECT id, login, password FROM users WHERE id = %s;",(id))
            # cursor.execute("DELETE resources_id, tag_id FROM tags_resources WHERE tag_id = %s;",(id))
            conn.commit()
            cursor.close()
            self.pool.putconn(conn)
        except:
            return "oops"