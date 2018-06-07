#!/usr/bin/env python3

from setuptools import setup

setup(
    name='Eris',
    version='0.1',
    # uncomment when there are tests.
    #test_suite='tests'
    packages=['eris'],
    install_requires=[
        'discord.py==0.16.12',
        'jsonschema==2.6.0'
    ]
)