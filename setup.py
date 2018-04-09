#!/usr/bin/env python
# coding: utf-8

"""setuptools based setup module for quaternions"""

from setuptools import setup
# To use a consistent encoding
import codecs
from os import path

import quaternions

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with codecs.open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name=quaternions.__name__,
    version=quaternions.__version__,
    description=quaternions.__description__,
    long_description=long_description,
    url=quaternions.__url__,
    download_url=quaternions.__download_url__,
    author=quaternions.__author__,
    author_email=quaternions.__author_email__,
    license=quaternions.__license__,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6'],
    keywords='OpenCASCADE pythonocc CAD',
    packages=['quaternions'],
    install_requires=[],
    extras_require={
        'dev': [],
        'test': ['pytest', 'coverage'],
    },
    package_data={},
    data_files=[],
    entry_points={})
