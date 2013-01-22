from flask import Flask

app = Flask(__name__)
from app import views
from app import urls
from app.helpers import Config
from app.connectors import connect

db = connect()
