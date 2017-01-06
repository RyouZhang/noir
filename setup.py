#!/usr/bin/env python


from setuptools import setup

setup(
    name='nori',
    version='0.0.1',
    packages=['nori'],    
    description='fast web framework',
    author='ryou zhang',
    author_email='ryouzhang@gmail.com',
    install_requires=['uvloop', 'aiohttp', 'toml'],
    url='https://github.com/RyouZhang/nori/',
    licence='Licence :: MTI Lecence',
)