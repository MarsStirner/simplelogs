# -*- coding: utf-8 -*-
from simplelogs.systemwide import app, mongo

from tsukino_usagi.client import TsukinoUsagiClient

__author__ = 'viruzzz-kun'


# noinspection PyUnresolvedReferences
class SimplelogsUsagiClient(TsukinoUsagiClient):
    def on_configuration(self, configuration):
        app.config.update(configuration)
        mongo.init_app(app)
        from simplelogs.app import views
