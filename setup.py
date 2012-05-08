#!/usr/bin/env python

"""
distutils/setuptools install script. See inline comments for packaging documentation.
"""

import os
import sys

import gae_skeleton

try:
    from setuptools import setup
    setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

packages = [
    'gae_skeleton',
]

requires = [
    'Fabric>=1.4.2',
    'webassets>=0.6',
    'closure>=20120305',
    'cssmin>=0.1.4',
    'mock>=0.8.0',
]

extras_require = {
}

setup(
    name='gae-skeleton',
    version=gae_skeleton.__version__,
    description='A simple skeleton for App Engine apps',
    long_description=open('README.rst').read() + '\n\n' +
                     open('HISTORY.rst').read(),
    author='Robert Kluin, Beau Lyddon',
    author_email='',
    url='',
    packages=packages,
    package_data={'': ['LICENSE', 'NOTICE']},
    include_package_data=True,
    install_requires=requires,
    extras_require=extras_require,
    license=open("LICENSE").read(),
    classifiers=(
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: Apache License 2.0',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
    ),
)
