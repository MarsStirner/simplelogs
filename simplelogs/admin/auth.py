# -*- coding: utf-8 -*-

import requests
import json

from flask import session, request, abort
from flask_login import UserMixin, login_user, logout_user
from sqlalchemy.orm import contains_eager

from simplelogs.systemwide import db, app, login_manager


class Person(db.Model):
    __tablename__ = 'Person'

    id = db.Column(db.Integer, primary_key=True)
    deleted = db.Column(db.Integer, nullable=False)
    lastName = db.Column(db.Unicode(30), nullable=False)
    firstName = db.Column(db.Unicode(30), nullable=False)
    patrName = db.Column(db.Unicode(30), nullable=False)
    login = db.Column(db.Unicode(32), nullable=False)

    user_profiles = db.relation('rbUserProfile', secondary='Person_Profiles')


class PersonProfiles(db.Model):
    __tablename__ = u'Person_Profiles'

    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.ForeignKey('Person.id'), nullable=False)
    userProfile_id = db.Column(db.ForeignKey('rbUserProfile.id'), nullable=False)


class rbUserProfile(db.Model):
    __tablename__ = u'rbUserProfile'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(16), nullable=False, index=True)
    name = db.Column(db.String(128), nullable=False, index=True)


class User(UserMixin):

    def __init__(self, person):
        self.id = person.id
        self.deleted = person.deleted
        self.lastName = person.lastName
        self.firstName = person.firstName
        self.patrName = person.patrName
        self.login = person.login
        self.roles = tuple({prof.code for prof in person.user_profiles})

    def is_active(self):
        return self.deleted == 0

    def is_admin(self):
        return 'admin' in self.roles

    def format_name(self):
        return u'{0} {1}'.format(self.lastName, self.firstName)


@login_manager.user_loader
def load_user(user_id):
    hippo_user = session.get('user', None)
    return hippo_user


def create_user_session(user_id):
    try:
        user_id = int(user_id)
    except ValueError:
        raise abort(401, '`cas_user_id` must be integer')
    person = db.session.query(Person).join(Person.user_profiles).filter(
        Person.id == user_id
    ).options(
        contains_eager(Person.user_profiles)
    ).all()
    if len(person):
        user = User(person[0])
        if login_user(user):
            session['user'] = user
    else:
        raise abort(401, 'cannot find user by `cas_user_id`')


def destroy_user_session():
    logout_user()
    session.pop('user', None)
    token = request.cookies.get(app.config['CASTIEL_AUTH_TOKEN'])
    if token:
        requests.post(app.config['COLDSTAR_URL'] + 'cas/api/release',
                      data=json.dumps({'token': token}))
