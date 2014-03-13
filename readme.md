Version: __0.2.2__

About
=====
Simplelogs is [RESTful] [rest] API logging system written in Python. It based on [MongoDB] [mongo] and [Flask Framework] [flask].

For start Simplelogs use:

    python app.py

For testing sending log message you can use [curl].

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

  * _Critical_ – for errors that lead to termination
  * _Error_ – for errors that occur, but are handled
  * _Warning_ – for exceptional circumstances that might not be errors
  * _Notice_ – for non-error messages you usually want to see
  * _Info_ – for messages you usually don’t want to see
  * _Debug_ – for debug messages
  
You can add, remove or modify any of level you want. You don't need to restart server after it. 

Log entry description
=====================
Log-entry is a collection of 3 required and 2 non-required entries:

  * _level_ (Required) - only text. Shoud be specified in app/config.yaml
  * _datetimestamp_ - current datetime stamp. You don't need to send it. Server will do it automaticly.
  * _owner_ (Required) - text or dict (hash-table, key-value storage). Dict can include arrays. (MAX 7 MB)
  * _data_ (Required) - text or dict (hash-table, key-value storage). Dict can include arrays. (MAX 7 MB)
  * _tags_ - list (array) only.

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
        <td>http://host/api/</td>
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

__0.2.2__:

  * Supporting datetime search parameter instead of date type,
  * Added 'skip' parameter for possibility of pagination realization.

__0.2.1__:

  * Modernizations getting data methods;
  * Supporting more various search parameters.

__0.2.0__:

  * New methods for getting data;
  * Some refactoring.

__0.1.4__:

  * Full test coverage;
  * Supporting username and password for remote connection to MongoDB-server. [Setting up authentication for MongoDB on Ubuntu with pymongo example.] [mongodb-remote-access]

__0.1.3__:

  * New method for creating entries. Now it understand only application/json content-type headers.

__0.1.2__:

  * New call get avaliable log entry levels (GET http://host/api/level/).


Using config file and connector to Mongo
========================================
  * __helpers.config__ - wrapper for config file. It returns dict with full configurations.
  * __connectors.connect__ - static method. It returns  MongoDB db-object.

Other
=====
For run unittests use:

    python -m unittest tests

in project-root directory.

[mongodb-remote-access]: https://github.com/SkyFox/simplelogs/wiki/Setting-up-authentication-for-MongoDB-on-Ubuntu-with-pymongo-example
[mongo]: http://www.mongodb.org/
[flask]: http://flask.pocoo.org/
[rest]: http://en.wikipedia.org/wiki/Representational_state_transfer
[pymongo]: http://api.mongodb.org/python/current/
[pyyaml]: http://pyyaml.org/
[Flask-WTF]: http://packages.python.org/Flask-WTF/
[deploying]: http://flask.pocoo.org/docs/deploying/
[curl]: http://en.wikipedia.org/wiki/CURL
