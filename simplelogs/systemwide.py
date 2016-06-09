# -*- coding: utf-8 -*-
import flask
from flask_pymongo import PyMongo

__author__ = 'viruzzz-kun'

app = flask.Flask(__name__)

mongo = PyMongo()
