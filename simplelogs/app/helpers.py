# -*- coding: utf-8 -*-

import os
import datetime
from bson.objectid import ObjectId
from flask import Response

from werkzeug.utils import import_string, cached_property
import yaml

from simplelogs.systemwide import app

try:
    import simplejson as json
except ImportError:
    try:
        import json
    except ImportError:
        raise ImportError


class MongoJsonEncoder(json.JSONEncoder):
    """JSONEncoder for MongoDB ObjectId and datetime object conversion

    It's impossible to serialize ObjectId and datetime object to json without such MongoJsonEncoder.
    """
    def default(self, obj):
        if isinstance(obj, (datetime.datetime, datetime.date)):
            return obj.isoformat()
        elif isinstance(obj, ObjectId):
            return obj.__str__()
        return json.JSONEncoder.default(self, obj)


def jsonify(*args, **kwargs):
    """ jsonify with support for MongoDB ObjectId and datetime-to-string conversion
    """
    return Response(json.dumps(dict(*args, **kwargs), cls=MongoJsonEncoder), mimetype='application/json')