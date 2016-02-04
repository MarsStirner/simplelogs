# -*- coding: utf-8 -*-
import os
import sys
sys.path.insert(0, os.path.dirname(__file__))
from app import app as application, LogEntry
if __name__ == '__main__':
    # LogEntry.ensure_index('owner')
    # LogEntry.ensure_index('owner.name')  #TODO: вкл. после приведения к owner.name
    application.run()
