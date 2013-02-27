#!/usr/bin/env python
__author__ = "Dmitry Timofeev"
__version__ = "0.1.4"
__email__ = "dimkat@gmail.com"

"""
Simplelogs is a logging system as a service (RESTful API).
It was made using MongoDB and Flask Framework.
Now I'm working on extending methods-list and client libraries.
Now it available for Python and Java. In future I think I will add lib for Objective-C.
Simplelogs is a very tiny layer between MongoDB and HTTP requests.

Fell free to contact with me by e-mail or IM.

"""

from app import app
app.run(debug = False) # If you are working on improvements I recommending you change debugging mo to True.