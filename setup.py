#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from version import __version__

setup(
    name='ripcord',
    version=__version__,
    description='A package for quickly creating RESTful API clients.',
    author='Wilhelm Murdoch',
    author_email='wilhelm.murdoch@gmail.com',
    url='http://www.thedrunkenepic.com/',
    packages=find_packages(exclude=['tests', 'tests.*']),
    install_requires=[
        'requests==1.1.0',
        'bunch==1.0.1'
    ],
    setup_requires=[
        'nose==1.1.2',
        'yanc==0.2.3',
        'mock==1.0.1'
    ]
)