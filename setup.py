#!/usr/bin/env/python

from ecl_facebook import metadata

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = 'ecl_facebook',
    version = metadata.__version__,
    url = 'http://git.elmcitylabs.com/ecl-facebook',
    license = metadata.__license__,
    description = 'Easy Facebook integration for Django.',
    long_description=read('README.rst'),
    author = metadata.__author__,
    author_email = metadata.__email__,
    packages=['ecl_facebook'],
    install_requires=["objectifier"],
    package_data={'': ['LICENSE']},
)

