#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths


extra_files = package_files('simplelogs/admin/static')
extra_files.extend(package_files('simplelogs/admin/templates'))

setup(
    name='Simplelogs',
    version='1.5.4',
    url='https://stash.bars-open.ru/scm/medvtr/simplelogs.git',
    author='hitsl',
    description='MIS logging system',
    long_description=read('readme.md'),
    include_package_data=True,
    packages=find_packages(),
    package_data={
        '': extra_files
    },
    platforms='any',
    install_requires=[
        'Flask',
        'PyMongo',
        'pyyaml',
        'simplejson',

        'requests',
        'Flask-SQLAlchemy',
        'pymysql',
        'Flask-Beaker',
        'Flask-Login',
        'Flask-Cache',
        'tsukino_usagi',
        'hitsl_utils',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
