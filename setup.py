#!/usr/bin/env/python

import ecl_facebook

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name = 'ecl_facebook',
    version = ecl_facebook.__version__,
    url = 'http://git.elmcitylabs.com/ecl_facebook',
    license = 'Apache 2.0',
    description = 'Easy Facebook integration for Django.',
    author = 'Dan Loewenherz',
    author_email = 'dan@elmcitylabs.com',
    packages=['ecl_facebook'],
    install_requires=["objectifier", "django>=1.3"],
    package_data={'': ['LICENSE']},
)

