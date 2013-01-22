# -*- coding: utf-8 -*-

from werkzeug import import_string, cached_property

from app import app
import yaml

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

#TODO Write this class!
class Config:
    #TODO Add try-except block.
    @staticmethod
    def mongo():
        return yaml.load(open('app/config.yaml', 'r'))['mongo']

def url(url_rule, import_name, **options):
    """
    We further optimize this in terms of amount of keystrokes needed to write Lazy views loading by having a function
    that calls into add_url_rule() by prefixing a string with the project name and a dot, and by wrapping view_func in
    a LazyView as needed.

    One thing to keep in mind is that before and after request handlers have to be in a file that is imported upfront
     to work properly on the first request. The same goes for any kind of remaining decorator.
    """
    view = LazyView('app.' + import_name)
    app.add_url_rule(url_rule, view_func=view, **options)