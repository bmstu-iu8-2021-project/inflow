import psycopg2

import sys
sys.path.append('..')

from models import Resource
from utils import Singleton


class ResourceService(metaclass=Singleton):
    def __init__(self, pool):
        self.pool = pool

    # def search_by_tag(self, id, *args):
    #     cursor = self.connection.cursor()
    #     str = 'tags_resources.tag_id = ' + id + ' '
    #     for i in args:
    #         str += 'AND tags_resources.tag_id = ' + i + ' '

    #     cursor.execute("SELECT resources.id, resources.label, resources.link FROM resources JOIN tags_resources WHERE %s",(str))

    #     return [Resource(*row) for row in cursor.fetchall()]

    # def search_by_label(self, label):
    #     cursor = self.connection.cursor()
    #     cursor.execute("SELECT id, label, link FROM resources WHERE label LIKE '%(%s)%'",(label))

    #     return [Resource(*row) for row in cursor.fetchall()]

    # def art_delete(self, id):
    #     cursor = self.connection.cursor()
    #     cursor.execute("DELETE id, label, link FROM resources WHERE id = %s",(id))
    #     cursor.execute("DELETE id, label, link FROM tags_resources WHERE resources_id = %s",(id))

    # def create(self, label, link):

    #     return Resource(0, label, link)
    #     cursor = self.connection.cursor()
    #     cursor.execute("INSERT INTO resources(label, link) VALUES (%s, %s)", (label, link))

    # def update_add_tags(self, tag_id, resources_id):
    #     cursor = self.connection.cursor()
    #     cursor.execute("INSERT INTO tags_resources(tag_id, resources_id) VALUES (%s, %s)",(tag_id, resources_id))

    # def update_delete_tags(self, tag_id):
    #     cursor = self.connection.cursor()
    #     cursor.execute("DELETE resources_id, tag_id FROM tags_resources WHERE tag_id = %s",(tag_id))

    # def update(self):
    #     cursor = self.connection.cursor()
    #     cursor.execute("UPDATE resources SET label = %s, link = %s WHERE id = %s",())

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