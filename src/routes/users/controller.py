import sys
from flask import json
from flask.json import jsonify
import psycopg2

from flask import request

sys.path.append('..')

from .service import UserService
from models import User
from utils import Singleton

class UserController(metaclass=Singleton):

    def __init__(self, services: dict):
        # TODO: raise exception if services doesn't contain "resources"
        self.users: UserService = services.get("users")

    def create(self): 
        jsonbody: dict = request.get_json(force=True)

        # TODO: check keys
        if "login" and "password" in jsonbody:
            login: str = jsonbody.get("login")
            password: str = jsonbody.get("password")

            # TODO: handle service's exceptions
            user: User = self.users.create(login, password)
            return jsonify(user)
        else:
            return {"error": "incorrect data entered"}

    def delete(self):
        jsonbody: dict = request.get_json(force=True)
        if "id" in jsonbody:
            id: str = jsonbody.get("id")
            self.users.delete(id)
        else:
            return {"error": "incorrect data entered"}

    def get(self):
        jsonbody: dict = request.get_json(force=True)
        if "id" in jsonbody:
            id: str = jsonbody.get("id")
            self.users.get(id)
        else:
            return {"error": "incorrect data entered"} 