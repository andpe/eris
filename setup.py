#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(
    name='Eris',
    version='0.1',
    # uncomment when there are tests.
    # test_suite='tests'
    packages=find_packages(),
    install_requires=[
        'discord.py>=1.3.4',
        'jsonschema>=3.2.0'
    ]
)
