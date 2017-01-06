from setuptools import setup

setup(
    name='nori',
    version='0.0.1',
    description='fast web framework',
    author='ryou zhang',
    author_email='ryouzhang@gmail.com',
    packages=['nori'],
    install_requires=['uvloop', 'aiohttp', 'toml']
)