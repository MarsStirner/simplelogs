# -*- coding: utf-8 -*-

from bson import ObjectId

from flask import jsonify, request

from helpers import config
from models import LogEntry

config = config()

def index():
    return jsonify({'SimpleLogs API status': 'Available'})

def get_levels_list():
    levels_list = config['level']
    return jsonify({'level': levels_list})

def add_logentry():
    if request.headers['Content-Type'] == 'application/json':
        errors = []

        request_data = request.json

        level = ""
        if not request_data.has_key("level"):
            errors.append({'level': 'Field required.'})
        else:
            level = request_data['level']

        if level not in config['level']:
            errors.append({'level': 'Unknown level type.'})

        owner = ""
        if not request_data.has_key("owner"):
            errors.append({'owner': 'Field required.'})
        else:
            owner = request_data['owner']

        data = ""
        if not request_data.has_key("data"):
            errors.append({'data': 'Field required.'})
        else:
            data = request_data['data']

        tags = []
        if request_data.has_key("tags"):
            tags = request.json['tags']
            if not isinstance(tags, list):
                errors.append({'tags': 'Tags must be an array.'})

        if not errors:
            entry = LogEntry(level, owner, data, tags)
            id_or_error = entry.save()
            if not isinstance(id_or_error, ObjectId):
                return jsonify({'OK': False, 'error': id_or_error})
            return jsonify({'OK': True, 'id': id_or_error.__str__()})
        else:
            return jsonify({"OK": False, 'errors': errors})

    else:
        #TODO Here should be NORMAL exception.
        return "415 Unsupported Media Type. \"application/json\" required.\n"