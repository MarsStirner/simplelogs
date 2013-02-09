# -*- coding: utf-8 -*-

from datetime import datetime
from pymongo.errors import AutoReconnect

from connectors import MongoDBConnection

db = MongoDBConnection.connect()
from helpers import config

config = config()
collection = config['mongo']['collection']

class LogEntry:
    """Main class for new log entries.

    Keyword arguments:
    owner - person ot system, who create this entry (required)
    datetimestamp - date and time, when entry was created (required)
    level - attentiveness level (required):
        - critical – for errors that lead to termination
        - error – for errors that occur, but are handled
        - warning – for exceptional circumstances that might not be errors
        - notice – for non-error messages you usually want to see
        - info – for messages you usually don’t want to see
        - debug – for debug messages
    data - main message body (required)
    tags - tags list for extended search

    """
    def __init__(self, level='info', owner='', data='', tags=[]):
        self.level = level
        self.owner = owner
        self.data = data
        self.tags = tags

    def save(self):
        '''Trying to save new log entry to Mongo.

        Returns entry id (from mongo) if everything all right, otherwise returns Connection error message.

        '''
        try:
            entry_id = db[collection].insert({
                'level': self.level,
                'datetimestamp': datetime.now(),
                'owner': self.owner,
                'data': self.data,
                'tags': self.tags
            })
            return entry_id
        except AutoReconnect, e:
            return e.message
