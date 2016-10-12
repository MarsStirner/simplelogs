# -*- coding: utf-8 -*-
import flask
from flask_pymongo import PyMongo
from flask_beaker import BeakerSession
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from hitsl_utils.cas import CasExtension


__author__ = 'viruzzz-kun'


app = flask.Flask(__name__)

mongo = PyMongo()

login_manager = LoginManager()

beaker_session = BeakerSession()

cas = CasExtension()

db = SQLAlchemy()
