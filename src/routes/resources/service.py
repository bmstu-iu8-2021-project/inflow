import psycopg2

import sys
sys.path.append('..')

from models.resource import Resource
from utils import Singleton


class ResourceService(metaclass=Singleton):
    def __init__(self, pool):
        self.pool = pool

    def status(self):
        conn = self.pool.getconn()
        cursor = conn.cursor()

        cursor.execute("SELECT count(id) FROM resources;")
        
        count = int(cursor.fetchone()[0])

        cursor.close()
        self.pool.putconn(conn)

        return {
            "status": count,
        }


    def search_by_tag(self, tags):
        conn = self.pool.getconn()
        cursor = conn.cursor()
        
        cursor.execute("SELECT resources.id, resources.title, resources.link FROM resources JOIN tags_resources WHERE tags_resources.tag_id IN %s;",(tags))
        result = [Resource(*row).__dict__ for row in cursor.fetchall()]
        cursor.close()
        self.pool.putconn(conn)
        return result

    def search_by_title(self, title):
        conn = self.pool.getconn()
        cursor = conn.cursor()

        cursor.execute("SELECT id, title, link FROM resources WHERE title LIKE '%(%s)%';",(title))
        result = [Resource(*row).__dict__ for row in cursor.fetchall()]
        cursor.close()
        self.pool.putconn(conn)
        return result

    def delete(self, id):
        conn = self.pool.getconn()
        cursor = conn.cursor()
        cursor.execute("DELETE id, title, link FROM resources WHERE id = %s;",(id))
        cursor.execute("DELETE tag_id, resource_id FROM tags_resources WHERE resource_id = %s;",(id))
        conn.commit()
        cursor.close()
        self.pool.putconn(conn)

    def create(self, title, link):
        conn = self.pool.getconn()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO resources(title, link) VALUES (%s, %s);", (title, link))
        result = [Resource(*row).__dict__ for row in cursor.fetchall()]
        conn.commit()
        cursor.close()
        self.pool.putconn(conn)
        return result

    def update_add_tags(self, tag_id, resource_id):
        conn = self.pool.getconn()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tags_resources(tag_id, resource_id) VALUES (%s, %s);",(tag_id, resource_id))
        conn.commit()
        cursor.close()
        self.pool.putconn(conn)

    def update_delete_tags(self, tag_id, resource_id):
        conn = self.pool.getconn()
        cursor = conn.cursor()
        cursor.execute("DELETE resources_id, tag_id FROM tags_resources WHERE tag_id = %s AND resource_id = %s;",(tag_id, resource_id))
        conn.commit()
        cursor.close()
        self.pool.putconn(conn)

    # def update(self):
    #     cursor = self.connection.cursor()
    #     cursor.execute("UPDATE resources SET title = %s, link = %s WHERE id = %s",())
