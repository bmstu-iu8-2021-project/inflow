import sys
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
        self.resourses: ResourceService = services.get("resources")
        

    def create(self): 
        jsonbody: dict = request.get_json(force=True)

        # TODO: check keys
        label: str = jsonbody.get("label")
        link: str = jsonbody.get("link")

        # TODO: handle service's exceptions
        resource: Resource = self.resourses.create(label, link)

        return jsonify(resource.__dict__)
