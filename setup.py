#!/usr/bin/env python

import botie

try:
    from setuptools import find_packages, setup
except ImportError:
    from distutils.core import find_packages, setup

setup(
    author='Ross McFarland',
    author_email='rwmcfa1@gmail.com',
    description=botie.__doc__,
    install_requires=[
        'certifi>=2017.7.27.1',
        'chardet>=3.0.4',
        'idna>=2.6',
        'requests>=2.18.4',
        'tornado>=4.5.2',
        'urllib3>=1.22',
    ],
    license='MIT',
    long_description=open('README.md').read(),
    name='botie',
    packages=find_packages(),
    url='https://github.com/ross/botie',
    version=botie.__VERSION__,
)
