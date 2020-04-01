#!/usr/bin/env python3
'''djs setup file'''

from setuptools import setup, find_packages
from os.path import abspath, dirname, join
from io import open

root_dir = abspath(dirname(__file__))

short_description = '''A framework for varying model parameters and automating concurrent usage
of the Wrf-hydro/National Water Model using Docker'''

# Use README.md as long description
with open(join(root_dir, 'README.md'), mode='r') as f:
    long_description = f.read()

setup(
    # Package version and information
    name='djs',
    version='0.1',
    package_dir={'' : 'djs'},
    packages=find_packages(where='djs', exclude=['*test*']),
    url='https://github.com/aaraney/NWM-Docker-Ensemble-Framework',

    # Package description information
    description='A framework for varying model parameters and automating concurrent usage of the Wrf-hydro/National Water Model using Docker',
    long_description=long_description,
    long_description_content_type='text/markdown',

    # Author information
    author='Austin Raney',
    author_email='aaraney@crimson.ua.edu',


    license='MIT License',

    # Search keywords
    keywords='docker nwm hydrology cuahsi noaa owp nwc',
)