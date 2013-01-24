# -*- coding: utf-8 -*-
from connectors import MongoDBConnection
from helpers import config

db = MongoDBConnection.connect()
config = config()

def index(username):
    db.test.insert({username: "Hello, world!"})
    return "Hello, World!"
