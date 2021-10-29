#!/usr/bin/python3

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
        
        self.app.add_url_rule('/', view_func=self.get_home)
        self.app.add_url_rule('/home', view_func=self.get_home)
        self.app.add_url_rule('/tags/all', view_func=self.tags_all, methods=['GET'])
        # self.app.add_url_rule('/tags/add',)
        # self.app.add_url_rule('/tags/edit',)
        # self.app.add_url_rule('/tags/delete',)
        # self.app.add_url_rule('/tags/search',)
        # self.app.add_url_rule('/tags/join',)
        # self.app.add_url_rule('/article/add',)
        # self.app.add_url_rule('/article/edit',)
        # self.app.add_url_rule('/article/delete',)
        # self.app.add_url_rule('/article/search',)

    def run(self):
        self.server = threading.Thread(target=self.app.run, kwargs={'host': self.host, 'port': self.port})
        self.server.start()
        return self.server

    def get_home(self):
        return 'Welcome to the inflow!'

    
    def tags_all(self):
        return str(self.tag_service.all())
            

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

    server = Server(address, "3000", SERVER_CONFIG)
    server.run()