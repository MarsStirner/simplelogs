Version: __0.1.2__

About
=====
Simplelogs is [RESTful] [rest] API logging system written in Python. It based on [MongoDB] [mongo] and [Flask Framework] [flask].

For start Simplelogs use:

    python app.py

For test sending log message you can use, for example, [curl]:

    curl -X POST -d 'data={"Entry info": "Some message"}&owner={"ip": "127.0.0.1", "user": "root"}&level=info&tags=["me", "java"]' http://127.0.0.1:5000/api/entry/

Requirements
============
  * [MongoDB] [mongo]
  * [Flask Framework] [flask]
  * [PyMongo] [pymongo]
  * [PyYAML] [pyyaml]
  * [Flask-WTF] [Flask-WTF]
  * [Any web-server with WSGI support] [deploying]

Config-file description
=======================
__app/config.yaml__ - configuration file. Config file is in YAML-format.

It has 2 section: _mongo_ and _levels_.

Mongo section describes base information about connection:

  * _host_ - hostname
  * _port_ - connection port
  * _user_ - not yet supported
  * _password_ not yet supported
  * _database_ - which database will be used
  * _collection_ - which collection in _database_ will be used

_Level_ section describes logenty levels. By default it includes:

  * Critical – for errors that lead to termination
  * Error – for errors that occur, but are handled
  * Warning – for exceptional circumstances that might not be errors
  * Notice – for non-error messages you usually want to see
  * Info – for messages you usually don’t want to see
  * Debug – for debug messages
  
You can add, remove or modify any of level you want. You don't need to restart server after it. 

Log entry description
=====================
Log-entry is a collection of 3 required and 2 non-required entries:

  * level (Required) - only text. Shoud be specified in app/config.yaml
  * datetimestamp - current datetime stamp. You don't need to send it. Server will do it automaticly.
  * owner (Required) - text or dict (hash-table, key-value storage). Dict can include arrays. (MAX 7 MB)
  * data (Required) - text or dict (hash-table, key-value storage). Dict can include arrays. (MAX 7 MB)
  * tags - list (array) only.

API description
===============
<table>
    <tr>
        <td>Method</td>
        <td>URI</td>
        <td>Description</td>
    </tr>
    <tr>
        <td>GET</td>
        <td>http://host/</td>
        <td>Get server status.</td>
    </tr>
    <tr>
            <td>GET</td>
            <td>http://host/api/level/</td>
            <td>Get avaliable log entry levels.</td>
    </tr>
    <tr>
        <td>POST</td>
        <td>http://host/api/entry/</td>
        <td>Create new log entry.</td>
    </tr>
</table>

Last changes:
============

__0.1.2__:

  * New call get avaliable log entry levels (GET http://host/api/level/).


Using config file and connector to Mongo
========================================
  * __helpers.config__ - wrapper for config file. It returns dict with full configurations.
  * __connectors.connect__ - static method. It returns  MongoDB db-object.

[mongo]: http://www.mongodb.org/
[flask]: http://flask.pocoo.org/
[rest]: http://en.wikipedia.org/wiki/Representational_state_transfer
[pymongo]: http://api.mongodb.org/python/current/
[pyyaml]: http://pyyaml.org/
[Flask-WTF]: http://packages.python.org/Flask-WTF/
[deploying]: http://flask.pocoo.org/docs/deploying/
[curl]: http://en.wikipedia.org/wiki/CURL
