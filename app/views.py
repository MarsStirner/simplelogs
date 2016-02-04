# -*- coding: utf-8 -*-

from bson import ObjectId

from flask import request

from helpers import config, jsonify
from models import LogEntry
from exceptions import InvalidAPIUsage
from pymongo.errors import AutoReconnect

VERSION = "0.2.1"

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
        if "level" not in request_data:
            errors.append({'level': 'Field required.'})
        else:
            level = request_data['level']

        # Is level in level list in config file?
        if level not in config['level']:
            errors.append({'level': 'Unknown level type.'})

        # Checking owner present (required)
        owner = ""
        if "owner" not in request_data:
            errors.append({'owner': 'Field required.'})
        else:
            owner = request_data['owner']

        # Checking data present (required)
        data = ""
        if "data" not in request_data:
            errors.append({'data': 'Field required.'})
        else:
            data = request_data['data']

        tags = []
        # Tags isn't required. If it present lets try to convert it to python-list.
        # If successfully - add it to entry. If not - return full error and don't create entry in DB.
        if "tags" in request_data:
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


def get_logentry_list():
    """Logentries list

    Returns Logentries list

    """
    if request.method == 'POST' and request.headers['Content-Type'] == 'application/json':
        request_data = request.json
        request_find = request_data.get('find', dict())
        sort = request_data.get('sort')
        limit = request_data.get('limit')
        skip = request_data.get('skip')
        find = dict()
        for key, value in request_find.iteritems():
            if key in ('level', 'owner', 'datetimestamp', 'tags', 'start', 'end'):
                find[key] = value
    elif request.method == 'GET':
        find, sort, limit, skip = None, None, None, None
    else:
        raise InvalidAPIUsage('Unsupported Media Type. \"application/json\" required.\n', 415)
    entry = LogEntry()
    try:
        result = entry.get_entries(find=find, sort=sort, skip=skip, limit=limit)
    except ValueError, e:
        raise InvalidAPIUsage(e.message, status_code=404)
    except AttributeError, e:
        raise InvalidAPIUsage(e.message, status_code=400)
    except TypeError, e:
        raise InvalidAPIUsage(e.message, status_code=400)
    except AutoReconnect, e:
        raise InvalidAPIUsage(e.message, status_code=500)
    return jsonify(dict(OK=True, result=list(result)))


def get_owners():
    """Get owners list

    Returns owners list

    """
    entry = LogEntry()
    try:
        result = entry.get_owners()
    except ValueError, e:
        raise InvalidAPIUsage(e.message, status_code=404)
    except AutoReconnect, e:
        raise InvalidAPIUsage(e.message, status_code=500)
    return jsonify(dict(OK=True, result=result))


def count_logentries():
    """Count logentries

    Returns number of logentries

    """
    if request.method == 'POST' and request.headers['Content-Type'] == 'application/json':
        find = dict()
        request_data = request.json
        request_find = request_data.get('find', dict())
        for key, value in request_find.iteritems():
            if key in ('level', 'owner', 'datetimestamp', 'tags', 'start', 'end'):
                find[key] = value
    elif request.method == 'GET':
        find, sort, limit = None, None, None
    else:
        raise InvalidAPIUsage('Unsupported Media Type. \"application/json\" required.\n', 415)
    entry = LogEntry()
    try:
        result = entry.count(find)
    except ValueError, e:
        raise InvalidAPIUsage(e.message, status_code=404)
    except AttributeError, e:
        raise InvalidAPIUsage(e.message, status_code=400)
    except TypeError, e:
        raise InvalidAPIUsage(e.message, status_code=400)
    except AutoReconnect, e:
        raise InvalidAPIUsage(e.message, status_code=500)
    return jsonify(dict(OK=True, result=result))
