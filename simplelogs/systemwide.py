# -*- coding: utf-8 -*-
import flask
from flask.ext.pymongo import PyMongo

__author__ = 'viruzzz-kun'

app = flask.Flask(__name__)

mongo = PyMongo()
