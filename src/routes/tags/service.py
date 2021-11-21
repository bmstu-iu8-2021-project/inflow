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
        try:
            conn = self.pool.getconn()
            cursor = conn.cursor()
            cursor.execute("SELECT id, label, color FROM tags;")
            # cursor.execute("CREATE FUNCTION all(code text) RETURNS table (id integer, label varchar, color varchar) as $$ BEGIN return query SELECT id, label, color FROM tags; EXCEPTION WHEN others THEN RAISE NOTICE 'SQLSTATE: %', SQLSTATE; RAISE; END; $$;")
            # cursor.execute("CREATE FUNCTION all(out id int, out label text, out color text) RETURNS TABLE (id integer, label varchar, color varchar) as $$ DECLARE r record; BEGIN return query SELECT id, label, color INTO r FROM tags; RETURN QUERY SELECT id, label, color FROM tags; EXCEPTION WHEN others THEN RAISE NOTICE 'SQLSTATE: %', SQLSTATE; RAISE; END; $$;")
            # cursor.execute("DO $$ DECLARE rec record; BEGIN SELECT id, label, color INTO rec FROM tags; raise notice '% % %', rec.id, rec.label, rec.color; END; $$ language plpgsql;")
            result = [Tag(*row).__dict__ for row in cursor.fetchall()]
            cursor.close()
            self.pool.putconn(conn)
            return result
        except:
            return "oops"

    def create(self, label, color):
        try:
            conn = self.pool.getconn()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO tags (label, color) VALUES (%s, %s) RETURNING id;", (label, color))
            id = cursor.fetchone()[0]
            
            conn.commit()
            
            tag = Tag(id, label, color)
            cursor.close()
            self.pool.putconn(conn)
            return [Tag(*row).__dict__ for row in cursor.fetchall()]
            # return tag.__dict__
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
            cursor.execute("DELETE id, label, color FROM tags WHERE id = %s;",(id))
            cursor.execute("DELETE resources_id, tag_id FROM tags_resources WHERE tag_id = %s;",(id))
            conn.commit()
            cursor.close()
            self.pool.putconn(conn)
        except:
            return "oops"

    def search(self, label):
        try:
            conn = self.pool.getconn()
            cursor = conn.cursor()
            cursor.execute("SELECT id, label, color FROM tags WHERE label LIKE '%(%s)%';",(label))
            result = [Tag(*row).__dict__ for row in cursor.fetchall()]
            conn.commit()
            cursor.close()
            self.pool.putconn(conn)
            return result
        except:
            return "oops"

    def join(self, id_src, id_dst):
        try:
            conn = self.pool.getconn()
            cursor = conn.cursor()
            cursor.execute("UPDATE tags_resources SET tag_id = %s WHERE tag_id = %s;",(id_dst, id_src))
            cursor.execute("DELETE id, label, color FROM tags WHERE id = %s;",(id_src)) #другой тег удаляем
            conn.commit()
            cursor.close()
            self.pool.putconn(conn)
        except:
            return "oops"
