#!/usr/bin/env python


from setuptools import setup

setup(
    name='nori',
    version='0.0.1',
    description='fast web framework',
    author='ryou zhang',
    author_email='ryouzhang@gmail.com',
    url='https://github.com/RyouZhang/nori/',
    install_requires=['uvloop', 'aiohttp'],
    packages=[
        'nori', 
        'nori.app', 
        'nori.entry', 
        'nori.rule',
        'nori.router',
        'nori.util',
        'nori.util.http',
        'nori.util.json'],   
    license='Licence :: MTI Lecence',
)