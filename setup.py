#!/usr/bin/env/python

from setuptools import setup

setup(
    name = 'ecl_facebook',
    version = '0.3.8',
    url = 'http://elmcitylabs.com',
    license = 'BSD',
    description = 'Easy Facebook integration for Django.',
    author = 'Dan Loewenherz',
    author_email = 'dan@elmcitylabs.com',
    packages=['ecl_facebook'],
    dependency_links=["http://packages.elmcitylabs.com.s3.amazonaws.com/ecl_tools-0.2.0.tar.gz#egg=ecl_tools-0.2.0"],
    install_requires=["ecl_tools>=0.2.0", "django==1.3"],
)

