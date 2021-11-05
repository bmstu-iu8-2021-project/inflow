#!/usr/bin/python3

from re import A
import threading
import os

from flask import Flask

app = Flask(__name__)

import services



class Server:
    def __init__(self, host, port, config):
        self.host = host
        self.port = port
        # переменная app в которой лежит объект класса Flask, инициализируем объект через __name__
        self.app = Flask(__name__)
        # andpoint для выключения приложения
        # в view_func= передаем параметр, который будет выполнять функцию shutdown

        self.tag_service = services.TagService(SERVER_CONFIG["PG_VARS"])
        self.resource_service = services.ResourceService(SERVER_CONFIG["PG_VARS"])
        
        self.app.add_url_rule('/', view_func=self.get_home)
        self.app.add_url_rule('/home', view_func=self.get_home)
        self.app.add_url_rule('/tags/all', view_func=self.tag_service.all, methods=['GET'])
        self.app.add_url_rule('/tags/create', view_func=self.tag_service.create, methods=['POST'])
        self.app.add_url_rule('/tags/delete', view_func=self.tag_service.delete, methods=['DELETE'])
        self.app.add_url_rule('/tags/search', view_func=self.tag_service.search, methods=['GET'])
        self.app.add_url_rule('/tags/join', view_func=self.tag_service.join, methods=['PUT'])
        self.app.add_url_rule('/article/search_by_tag', view_func=self.resource_service.search_by_tag, methods=['GET'])
        self.app.add_url_rule('/article/search_by_label', view_func=self.resource_service.search_by_label, methods=['GET'])
        self.app.add_url_rule('/article/delete', view_func=self.resource_service.art_delete, methods=['DELETE'])
        self.app.add_url_rule('/article/create', view_func=self.resource_service.art_create, methods=['POST'])
        self.app.add_url_rule('/article/update_add_tags', view_func=self.resource_service.update_add_tags, methods=['PUT'])
        self.app.add_url_rule('/article/update_delete_tags', view_func=self.resource_service.update_delete_tags, methods=['PUT'])

    def run(self):
        self.server = threading.Thread(target=self.app.run, kwargs={'host': self.host, 'port': self.port})
        self.server.start()
        return self.server

    def get_home(self):
        return 'Welcome to the inflow!'

    
    # def tags_all(self):
    #     return str(self.tag_service.all())
            

SERVER_CONFIG = {
    "PG_VARS": {
        "PG_USER": os.environ.get("PG_USER"),
        "PG_PASS": os.environ.get("PG_PASS"),
        "PG_DB":   os.environ.get("PG_DB"),
        "PG_PORT": os.environ.get("PG_PORT"),
        "PG_HOST": os.environ.get("PG_HOST"),
    }
}

if __name__ == "__main__":
    address = os.environ.get("PROD_ADDR")
    if not address:
        address = "127.0.0.1"
    address = "0.0.0.0"

    server = Server(address, "3000", SERVER_CONFIG)
    server.run()