import psycopg2

import sys
sys.path.append('..')

from models.resource import Resource
from utils import Singleton


class ResourceService(metaclass=Singleton):
    def __init__(self, pool):
        self.pool = pool

    def status(self):
        try:
            conn = self.pool.getconn()
            cursor = conn.cursor()

            cursor.execute("SELECT count(id) FROM resources;")
            
            count = int(cursor.fetchone()[0])

            cursor.close()
            self.pool.putconn(conn)

            return {
                "status": count,
            }
        except:
            return "oops"


    def search_by_tag(self, tags):
        try:
            conn = self.pool.getconn()
            cursor = conn.cursor()
            
            cursor.execute("SELECT resources.id, resources.title, resources.link FROM resources JOIN tags_resources WHERE tags_resources.tag_id IN %s;",(tags))
            result = [Resource(*row).__dict__ for row in cursor.fetchall()]
            cursor.close()
            self.pool.putconn(conn)
            return result
        except:
            return "oops"

    def search_by_title(self, title):
        try:
            conn = self.pool.getconn()
            cursor = conn.cursor()

            cursor.execute("SELECT id, title, link FROM resources WHERE title LIKE '%(%s)%';",(title))
            result = [Resource(*row).__dict__ for row in cursor.fetchall()]
            cursor.close()
            self.pool.putconn(conn)
            return result
        except:
            return "oops"

    def delete(self, id):
        try:
            conn = self.pool.getconn()
            cursor = conn.cursor()
            cursor.execute("DELETE id, title, link FROM resources WHERE id = %s;",(id))
            cursor.execute("DELETE tag_id, resource_id FROM tags_resources WHERE resource_id = %s;",(id))
            conn.commit()
            cursor.close()
            self.pool.putconn(conn)
        except:
            return "oops"

    def create(self, title, link):
        try:
            conn = self.pool.getconn()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO resources (title, link) VALUES (%s, %s) RETURNING id;", (title, link))
            id = cursor.fetchone()[0]
            # result = [Resource(*row).__dict__ for row in cursor.fetchall()]
            conn.commit()
            Resource(id, title, link)
            cursor.close()
            self.pool.putconn(conn)
            return id
        except:
            return "oops"

    def update_add_tags(self, tag_id, resource_id):
        try:
            conn = self.pool.getconn()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO tags_resources(tag_id, resource_id) VALUES (%s, %s);",(tag_id, resource_id))
            conn.commit()
            cursor.close()
            self.pool.putconn(conn)
        except:
            return "oops"

    def update_delete_tags(self, tag_id, resource_id):
        try:
            conn = self.pool.getconn()
            cursor = conn.cursor()
            cursor.execute("DELETE resources_id, tag_id FROM tags_resources WHERE tag_id = %s AND resource_id = %s;",(tag_id, resource_id))
            conn.commit()
            cursor.close()
            self.pool.putconn(conn)
        except:
            return "oops"

    # def update(self):
    #     cursor = self.connection.cursor()
    #     cursor.execute("UPDATE resources SET title = %s, link = %s WHERE id = %s",())
