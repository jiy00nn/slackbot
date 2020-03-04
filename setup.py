from os.path import join, dirname, normpath
from setuptools import setup, find_packages

__version__ = open(join(normpath(dirname(__file__)), 'slackbot/VERSION')).read().strip()

install_requires = (
    'requests<=2.4.0,>=2.23.0'
    'graphene>=2.0'
)

setup(name='slackbot',
      version=__version__,
      description='A github commit check bot for Slack',
      author='JiYoon Bak',
      author_email='wldbs204@gmail.com',
      url='',
      platforms=['Any'],
      install_requires=install_requires,
      classifiers=['Programming Language :: Python :: 3.7'])