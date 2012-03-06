#!/usr/bin/env/python

from setuptools import setup

setup(
    name = 'ecl_facebook',
    version = '0.3.16',
    url = 'http://git.elmcitylabs.com/ecl_facebook',
    license = 'BSD',
    description = 'Easy Facebook integration for Django.',
    author = 'Dan Loewenherz',
    author_email = 'dan@elmcitylabs.com',
    packages=['ecl_facebook'],
    install_requires=["objectifier", "django>=1.3"],
)

