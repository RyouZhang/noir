import os
import platform
import sys
import warnings

try:
    # Use setuptools if available, for install_requires (among other things).
    import setuptools
    from setuptools import setup
except ImportError:
    setuptools = None
    from distutils.core import setup

from distutils.core import Extension

setup(
    name='nori',
    version='0.0.1',
    packages=['nori'],    
    description='fast web framework',
    author='ryou zhang',
    author_email='ryouzhang@gmail.com',
    install_requires=['uvloop', 'aiohttp', 'toml'],
    url='https://github.com/RyouZhang/nori/',
    licence='Licence :: MTI Lecence'
)