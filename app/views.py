# -*- coding: utf-8 -*-

import json
from bson import ObjectId

from flask import jsonify

from helpers import config
from forms import EntryForm
from models import LogEntry

config = config()

def index():
    return jsonify({'SimpleLogs API status': 'Available'})

def new_entry():
    form = EntryForm(csrf_enabled=False)
    errors = []

    #TODO customize request/response headers and messages
    if form.validate_on_submit():
        entry = LogEntry()

        level = form.level.data
        if level not in config['level']:
            errors.append({'level': 'Unknown level type.'})
        else:
            entry.level = level

        entry.datetimestamp = form.datetimestamp.data

        try:
            owner =json.loads(form.owner.data)
        except ValueError:
            owner = form.owner.data
        entry.owner = owner

        try:
            data =json.loads(form.data.data)
        except ValueError:
            data = form.data.data
        entry.data = data

        if form.tags.data:
            tags = form.tags.data
            try:
                tags = list(json.loads(tags))
                entry.tags = tags
            except:
                errors.append({'tags': 'Tags must be array.'})

        if not errors:
            id_or_error = entry.save()
            if isinstance(id_or_error, ObjectId):
                return jsonify({'OK': True, 'id': id_or_error.__str__()})
            else:
                return jsonify({'OK': False, 'error': id_or_error})
        else:
            return jsonify({"OK": False, 'errors': errors})

    else:
        if form.level.errors: errors.append({'level': form.level.errors[0]})
        if form.owner.errors: errors.append({'owner': form.owner.errors[0]})
        if form.data.errors: errors.append({'data': form.data.errors[0]})
        return jsonify({'OK': False, 'errors': errors})