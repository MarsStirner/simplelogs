# -*- coding: utf-8 -*-
from app import db

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
    def __init__(self, level, datetimestamp, owner, data, tags=[]):
        self.level = level
        self.datetimestamp = datetimestamp
        self.owner = owner
        self.data = data
        self.tags = tags

    def save(self):
        pass