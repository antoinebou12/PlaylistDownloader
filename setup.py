#!/usr/bin/env python

import runpy
from setuptools import setup, find_packages

ns_version = runpy.run_path('version.py')

# Package meta-data.
NAME = 'PlaylistToMP3S'
DESCRIPTION = 'Download a playlist (spotify, youtube) by finding  download the mp3 of the music video youtube'
URL = 'https://gitlab.com/antoinebou13/playlisttomp3s'
EMAIL = 'antoine.bou13@gmail.com'
AUTHOR = 'Antoine Boucher'
REQUIRES_PYTHON = '>=3.6.0'

VERSION = None

LONG_DESCRIPTION = open('README.md').read()

console_scripts = ['']

extras_require = {}

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

SETUP = dict(
    name=NAME,
    version=ns_version['__version__'],
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    url=URL,
    license='MIT',
    author=AUTHOR,
    author_email=EMAIL,
    packages=find_packages(),
    install_requires=requirements,
    entry_points={'console_scripts': console_scripts},
    extras_require=extras_require
)

if __name__ == '__main__':
    setup(**SETUP)