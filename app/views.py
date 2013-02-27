# -*- coding: utf-8 -*-

from bson import ObjectId

from flask import jsonify, request

from helpers import config
from models import LogEntry

VERSION = "0.1.4"

config = config()


def index():
    """Status page

    Generating status (main) page and returns it.

    """
    response = {'name': "simplelogs",
                'type': "API",
                'status': "available",
                'version': VERSION}
    return jsonify(response)


def get_levels_list():
    """Levels list

    Returns level list from config file as a json-list.

    """
    levels_list = config['level']
    return jsonify({'level': levels_list})


def add_logentry():
    """Creating new log entry and saving it to DB.

    Returns False, if validation had problems with validating inputs,
    returns False, if client tries to send not a json,
    otherwise return True and ObjectId.

    """
    if request.headers['Content-Type'] == 'application/json':
        errors = []

        request_data = request.json

        # Lets check selected level
        level = ""
        if not request_data.has_key("level"):
            errors.append({'level': 'Field required.'})
        else:
            level = request_data['level']

        # Is level in level list in config file?
        if level not in config['level']:
            errors.append({'level': 'Unknown level type.'})

        # Checking owner present (required)
        owner = ""
        if not request_data.has_key("owner"):
            errors.append({'owner': 'Field required.'})
        else:
            owner = request_data['owner']

        # Checking data present (required)
        data = ""
        if not request_data.has_key("data"):
            errors.append({'data': 'Field required.'})
        else:
            data = request_data['data']

        tags = []
        # Tags isn't required. If it present lets try to convert it to python-list.
        # If successfully - add it to entry. If not - return full error and don't create entry in DB.
        if request_data.has_key("tags"):
            tags = request.json['tags']
            if not isinstance(tags, list):
                errors.append({'tags': 'Tags must be an array.'})

        if not errors:
            entry = LogEntry(level, owner, data, tags)
            id_or_error = entry.save()
            if not isinstance(id_or_error, ObjectId):
                return jsonify({'OK': False, 'error': id_or_error})
            # ___str___ is a string representation of JS ObjectID from MongoDB.
            return jsonify({'OK': True, 'id': id_or_error.__str__()})
        else:
            return jsonify({"OK": False, 'errors': errors})

    else:
        #TODO Here should be NORMAL exception.
        return jsonify({"errors": ["415 Unsupported Media Type. \"application/json\" required.\n",]})