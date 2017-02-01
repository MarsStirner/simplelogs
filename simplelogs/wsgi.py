# -*- coding: utf-8 -*-
import os

from simplelogs.systemwide import app
from simplelogs.usagicompat import SimplelogsUsagiClient

usagi = SimplelogsUsagiClient(app.wsgi_app, os.getenv('TSUKINO_USAGI_URL', 'http://127.0.0.1:5900'), 'simplelogs')
app.wsgi_app = usagi.app
usagi()

if __name__ == '__main__':
    app.run(port=app.config.get('SERVER_PORT', 6604))
