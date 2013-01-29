# -*- coding: utf-8 -*-

import datetime

from flask.ext.wtf import Form, TextField, StringField, DateTimeField
from flask.ext.wtf import Required

class EntryForm(Form):
    level =  StringField('level', validators = [Required()])
    datetimestamp = DateTimeField(default=datetime.datetime.now())
    owner = TextField('owner', validators = [Required()])
    data = TextField('data', validators = [Required()])
    tags = TextField('tags')