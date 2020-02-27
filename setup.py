# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

setup(
    name='ettusdf',
    version='0.1.0',
    description='Direction of arrival estimation with the Ettus N310',
    long_description=readme,
    author='Bailey Campbell',
    author_email='baileycampbell@psu.edu',
    url='https://github.com/hrg-lab/ettus-df',
    packages=find_packages(exclude=('tests', 'docs'))
)

