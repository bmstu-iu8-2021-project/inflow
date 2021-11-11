# from _typeshed import Self
import sys
from flask import json
from flask.json import jsonify
import psycopg2

from flask import request

sys.path.append('..')

from .service import TagService
from models import Tag
from utils import Singleton

class TagController(metaclass=Singleton):

    def __init__(self, services: dict):
        # TODO: raise exception if services doesn't contain "resources"
        self.tags: TagService = services.get("tags")

    def create(self): 
        jsonbody: dict = request.get_json(force=True)

        # TODO: check keys
        label: str = jsonbody.get("label")
        color: str = jsonbody.get("color")

        # TODO: handle service's exceptions
        tag: Tag = self.tags.create(label, color)

        return jsonify(tag)

    def delete(self):
        jsonbody: dict = request.get_json(force=True)
        id: str = jsonbody.get("id")
        self.tags.delete(id)

    def search(self):
        jsonbody: dict = request.get_json(force=True)

        label: str = jsonbody.get("label")
        result = self.tags.search(label)
        return jsonify(result)

    def join(self):
        jsonbody: dict = request.get_json(force=True)
        tags: str = jsonbody.get("tags")
        self.resourses.search_by_tag(tags)

    def all(self):
        result = self.tags.all()
        return jsonify(result)
