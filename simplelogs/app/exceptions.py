# -*- coding: utf-8 -*-
from flask import make_response, request
from simplelogs.app.helpers import app, jsonify


class InvalidAPIUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


@app.errorhandler(InvalidAPIUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.errorhandler(404)
def not_found(error):
    if request.method == 'POST' and request.headers['Content-Type'] == 'application/json':
        return make_response(jsonify({'error': 'Not found'}), 404)
    else:
        return make_response('<html><body><h1>Not found</h2></body></html>', 404)