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
    license = ecl_facebook.__license__,
    description = 'Easy Facebook integration for Django.',
    author = ecl_facebook.__license__,
    author_email = ecl_facebook.__email__,
    packages=['ecl_facebook'],
    install_requires=["objectifier", "django>=1.3"],
    package_data={'': ['LICENSE']},
)

