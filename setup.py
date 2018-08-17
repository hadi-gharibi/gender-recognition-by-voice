#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""
from os import read

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('requirements.text') as requirements_file:
    requirements = requirements_file.read()

setup_requirements =[]

setup(
    author="hadi gharibi",
    author_email='hady.gharibi@gmail.com',
    description='Gender Recognition by Voice',
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n',
    include_package_data=True,
    keywords='irholiday',
    name='irholiday',
    packages=find_packages(include=['irholiday']),
    setup_requires=setup_requirements,
    url='https://github.com/hadi-gharibi/Gender-Recognition-by-Voice'
)