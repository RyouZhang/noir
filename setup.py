#!/usr/bin/env python


from setuptools import setup

setup(
    name='nori',
    version='0.0.1',
    description='fast web framework',
    author='ryou zhang',
    author_email='ryouzhang@gmail.com',
    url='https://github.com/RyouZhang/nori/',
    install_requires=['uvloop', 'aiohttp', 'toml'],
    packages=['nori'],   
    licence='Licence :: MTI Lecence',
)