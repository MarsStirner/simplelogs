#!/usr/bin/env python
import os
from setuptools import setup, find_packages


def list_files(pre_path, *dirnames):
    l = len(pre_path)
    for dirname in dirnames:
        for path, subdirs, files in os.walk(os.path.join(pre_path, dirname)):
            post_path = path[l + 1:]
            for filename in files:
                full_path = os.path.join(post_path, filename)
                yield full_path


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='Simplelogs',
    version='1.4',
    packages=find_packages(),
    url='',
    license='',
    author='HITSL',
    author_email='',
    description=''
)
