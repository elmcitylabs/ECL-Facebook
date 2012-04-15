#!/usr/bin/env/python

import os
from ecl_facebook import metadata

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open("README.rst") as f:
    long_description = f.read()

setup(
    name = 'ecl_facebook',
    version = metadata.__version__,
    url = 'http://git.elmcitylabs.com/ecl-facebook',
    license = metadata.__license__,
    description = 'Easy Facebook integration for Django.',
    long_description=long_description,
    author = metadata.__author__,
    author_email = metadata.__email__,
    packages=['ecl_facebook'],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content :: CGI Tools/Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
        ],
    install_requires=['objectifier>=1.1.2'],
    package_data={'': ['LICENSE']},
)

