# -*- coding: utf-8 -*-
from simplelogs.systemwide import app, mongo, beaker_session, login_manager, cas, db

from tsukino_usagi.client import TsukinoUsagiClient
from simplelogs.admin.app import module as admin_module

__author__ = 'viruzzz-kun'


# noinspection PyUnresolvedReferences
class SimplelogsUsagiClient(TsukinoUsagiClient):
    def on_configuration(self, configuration):
        app.config.update(configuration)
        mongo.init_app(app)
        beaker_session.init_app(app)
        login_manager.init_app(app)
        cas.init_app(app)
        db.init_app(app)

        app.register_blueprint(admin_module, url_prefix='/admin')
        from simplelogs.app import views
