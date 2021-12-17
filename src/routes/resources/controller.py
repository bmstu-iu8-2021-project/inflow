# from _typeshed import Self
import sys
from flask import json
from flask.json import jsonify
import psycopg2

from flask import request

sys.path.append('..')

from .service import ResourceService
from models import Resource
from utils import Singleton


class ResourceController(metaclass=Singleton):

    def __init__(self, services: dict):
        # TODO: raise exception if services doesn't contain "resources"
        if "resources" in services:
            self.resourses: ResourceService = services.get("resources")
        

    def create(self): 
        jsonbody: dict = request.get_json(force=True)

        # TODO: check keys
        if "title" and "link" in jsonbody:
            title: str = jsonbody.get("title")
            link: str = jsonbody.get("link")

            # TODO: handle service's exceptions
            resource: Resource = self.resourses.create(title, link)

            return jsonify(resource)
        else:
            return {"error": "incorrect data entered"}

    def status(self): 
        status = self.resourses.status()
        return jsonify(status)

    def search_by_tags(self):
        jsonbody: dict = request.get_json(force=True)
        if "tags" in jsonbody:
            tags: str = jsonbody.get("tags")
            result = self.resourses.search_by_tag(tags)
            return jsonify(result)
        else:
            return {"error": "incorrect data entered"}

    def search_by_title(self):
        jsonbody: dict = request.get_json(force=True)
        if "title" in jsonbody:
            title: str = jsonbody.get("title")
            result: Resource = self.resourses.search_by_title(title)
            # last_result = json.dumps(result)
            last_result = format(jsonify(result).get_json(force=True))
            last_result = jsonify(result)
            # return format(result.get_json(force=True))
            # return format(jsonify(result).get_json(force=True))
            
            return last_result
        else:
            return {"error": "incorrect data entered"}

    def delete(self):
        jsonbody: dict = request.get_json(force=True)
        if "id" in jsonbody:
            id: str = jsonbody.get("id")
            self.resourses.delete(id)
        else:
            return {"error": "incorrect data entered"}

    def update_add_tags(self):
        jsonbody: dict = request.get_json(force=True)
        # resource_id = ""
        # tag_id = ""
        if "tags" in jsonbody:
            for value in jsonbody:
                if value == Resource:
                    resource_id = value.get("id")
                if value == Resource:
                    tag_id = value.get("id")
            self.resourses.update_add_tags(tag_id, resource_id)
        else:
            return {"error": "incorrect data entered"}

    def update_delete_tags(self):
        jsonbody: dict = request.get_json(force=True)
        # resource_id = ""
        # tag_id = ""
        if "tags" in jsonbody:
            for value in jsonbody:
                if value == Resource:
                    resource_id = value.get("id")
                if value == Resource:
                    tag_id = value.get("id")
            self.resourses.update_delete_tags(tag_id, resource_id)  
        else:
            return {"error": "incorrect data entered"}  

