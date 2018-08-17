#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""
from os import read

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('requirements.txt') as requirements_file:
    requirements = requirements_file.read()

setup_requirements =[]

setup(
    author="hadi gharibi",
    author_email='hady.gharibi@gmail.com',
    description='Gender Recognition by Voice',
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n',
    #include_package_data=True,
    name='gender-recognition',
    packages=find_packages(),
    setup_requires=setup_requirements,
    url='https://github.com/hadi-gharibi/gender-recognition-by-voice'
)