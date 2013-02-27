# -*- coding: utf-8 -*-

import os

from werkzeug import import_string, cached_property
import yaml

from app import app


class LazyView(object):
    """Lazily Loading Views

    Source: http://flask.pocoo.org/docs/patterns/lazyloading/
    The trick to actually load the view function as needed.

    What’s important here is is that __module__ and __name__ are properly set. This is used by Flask internally to
    figure out how to name the URL rules in case you don’t provide a name for the rule yourself.

    """
    def __init__(self, import_name):
        self.__module__, self.__name__ = import_name.rsplit('.', 1)
        self.import_name = import_name

    @cached_property
    def view(self):
        return import_string(self.import_name)

    def __call__(self, *args, **kwargs):
        return self.view(*args, **kwargs)


def url(url_rule, import_name, **options):
    """Generating new urls for url_rule by func_name

    We further optimize this in terms of amount of keystrokes needed to write Lazy views loading by having a function
    that calls into add_url_rule() by prefixing a string with the project name and a dot, and by wrapping view_func in
    a LazyView as needed.

    One thing to keep in mind is that before and after request handlers have to be in a file that is imported upfront
     to work properly on the first request. The same goes for any kind of remaining decorator.

    """
    view = LazyView('app.' + import_name)
    app.add_url_rule(url_rule, view_func=view, **options)


def config():
    """Loading configurations from config file

    This method read the config.yaml file and then returns all configurations as a dict.
    If you don't familiar with yaml format visit: http://en.wikipedia.org/wiki/YAML
    Before reading file this method changing working directory. It don't any sense when you use
    werkzeug. But it really need when you will install this app with nginx+uwsgi.
    How to do that, read manual: https://github.com/SkyFox/simplelogs/wiki/Deploying-simplelogs-with-nginx-and-uWSGI

    """
    f = open(os.path.join(app.root_path, 'config.yaml'), 'r')
    config = yaml.load(f)
    return config