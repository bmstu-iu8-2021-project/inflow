from _typeshed import Self
import sys
from flask.json import jsonify
import psycopg2

from flask import request

sys.path.append('..')

from .service import ResourceService
from models import Resource, resource
from utils import Singleton


class ResourceController(metaclass=Singleton):

    def __init__(self, services: dict):
        # TODO: raise exception if services doesn't contain "resources"
        self.resourses: ResourceService = services.get("resources")
        

    def create(self): 
        jsonbody: dict = request.get_json(force=True)

        # TODO: check keys
        label: str = jsonbody.get("label")
        link: str = jsonbody.get("link")

        # TODO: handle service's exceptions
        resource: Resource = self.resourses.create(label, link)

        return jsonify(resource)

    def status(self): 
        status = self.resourses.status()
        return jsonify(status)

    def search_by_tag(self):
        jsonbody: dict = request.get_json(force=True)
        str=""
        for key, tags in jsonbody.items():
            if key == "id":
                str += tags + ","
        str -= ","
        result = self.resourses.search_by_tag(str)
        return jsonify(result)

    def search_by_label(self):
        jsonbody: dict = request.get_json(force=True)

        label: str = jsonbody.get("label")
        result = self.resourses.search_by_label(label)
        return jsonify(result)

    def delete(self):
        jsonbody: dict = request.get_json(force=True)
        id: str = jsonbody.get("id")
        self.resourses.delete(id)

    def update_add_tags(self):
        jsonbody: dict = request.get_json(force=True)
        resource_id = ""
        tag_id = ""
        for value in jsonbody:
            if value == Resource:
                resource_id = value.get("id")
            if value == Resource:
                tag_id = value.get("id")
        self.resourses.update_add_tags(tag_id, resource_id)

    def update_delete_tags(self):
        jsonbody: dict = request.get_json(force=True)
        resource_id = ""
        tag_id = ""
        for value in jsonbody:
            if value == Resource:
                resource_id = value.get("id")
            if value == Resource:
                tag_id = value.get("id")
        self.resourses.update_delete_tags(tag_id, resource_id)    

