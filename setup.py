#!/usr/bin/env python


from setuptools import setup

setup(
    name='noir',
    version='0.0.10',
    description='A python fast web service base on aiohttp and uvloop, for python 3.5+',
    author='ryou zhang',
    author_email='ryouzhang@gmail.com',
    url='https://github.com/RyouZhang/noir/',
    install_requires=['uvloop', 'aiohttp'],
    packages=[
        'noir', 
        'noir.app', 
        'noir.rule',
        'noir.router',
        'noir.util',
        'noir.util.http',
        'noir.util.json',
        'noir.util.logging'],   
    license='Licence :: MTI Lecence',
)