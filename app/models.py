# -*- coding: utf-8 -*-

from datetime import datetime
from pymongo.errors import AutoReconnect
from pymongo import DESCENDING

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
        """Trying to save new log entry to Mongo.

        Returns entry id (from mongo) if everything all right, otherwise returns Connection error message.

        """
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

    def get_entries(self, find=None, sort=None, limit=None):
        """Getting logentry data

        Args:
            find: dict, pymongo-find clause for filtering documents
            sort: single key or a list of (key, direction) pairs specifying the keys to sort on
            limit: int, the number of results to be returned

        Returns:
            pymongo cursor
        """
        if sort is None:
            sort = [('datetimestamp', DESCENDING)]
        if limit is None:
            limit = 100
        if find is not None and isinstance(find, dict):
            try:
                cursor = db[collection].find(find).sort(sort).limit(limit)
            except TypeError, e:
                error = u'Неверный тип параметров ({0})'.format(e)
                raise TypeError(error)
            except AutoReconnect, e:
                error = u'Потеряно подключение к БД ({0})'.format(e)
                raise AutoReconnect(error)
        else:
            cursor = db[collection].find().sort(sort).limit(limit)
        return cursor

    def count(self, find=None):
        """Count logentry

        Args:
            find: dict, pymongo-find clause for filtering documents

        Returns:
            the number of documents in the results set for this clause
        """
        if find is not None and isinstance(find, dict):
            try:
                cursor = db[collection].find(find).count()
            except TypeError, e:
                error = u'Неверный тип параметров ({0})'.format(e)
                raise TypeError(error)
            except AutoReconnect, e:
                error = u'Потеряно подключение к БД ({0})'.format(e)
                raise AutoReconnect(error)
        else:
            cursor = db[collection].find().count()
        return cursor

    def get_owners(self):
        """Getting list of unique owners

        Returns:
            pymongo cursor
        """
        try:
            cursor = db[collection].distinct('owner')
        except AutoReconnect, e:
            error = u'Потеряно подключение к БД ({0})'.format(e)
            raise AutoReconnect(error)
        else:
            return cursor