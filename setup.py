#!/usr/bin/env python

from setuptools import find_packages
from setuptools import setup

setup(
    name='splitit',
    version='0.1.0',
    description='A program to divide items fairly',
    author='Tom Dooner, Joseph Lynch',
    author_email='jolynch@mit.edu',
    url='https://github.com/jolynch/splitit.git',
    packages=find_packages(exclude=['tests', 'bin']),
    include_package_data=True,
    setup_requires=['setuptools'],
    install_requires=[
        'Flask',
        'Flask-SQLAlchemy',
        'pytest'
    ],
    scripts=['bin/splitit-web', 'bin/splitit-repl'],
    license='MIT License'
)
