from os.path import join, dirname, normpath
from setuptools import setup, find_packages

__version__ = open(join(normpath(dirname(__file__)), 'slackbot/VERSION')).read().strip()
print(__version__)
