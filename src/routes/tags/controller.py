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
        if "label" and "color" in jsonbody:
            label: str = jsonbody.get("label")
            color: str = jsonbody.get("color")

            # TODO: handle service's exceptions
            tag: Tag = self.tags.create(label, color)
            return jsonify(tag)
        else:
            return {"error": "incorrect data entered"}

    def delete(self):
        jsonbody: dict = request.get_json(force=True)
        if "id" in jsonbody:
            id: str = jsonbody.get("id")
            self.tags.delete(id)
        else:
            return {"error": "incorrect data entered"}

    def search(self):
        jsonbody: dict = request.get_json(force=True)
        if "label" in jsonbody:
            label: str = jsonbody.get("label")
            result = self.tags.search(label)
            return jsonify(result)
        else:
            return {"error": "incorrect data entered"}

    def join(self):
        jsonbody: dict = request.get_json(force=True)
        if "tags" in jsonbody:
            tags: str = jsonbody.get("tags")
            self.resourses.search_by_tag(tags)
        else:
            return {"error": "incorrect data entered"}

    def all(self):
        result = self.tags.all()
        return jsonify(result)
