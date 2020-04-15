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
    version='0.0.1',
    packages=find_packages(exclude=['*test*']),
    url='https://github.com/aaraney/NWM-Dockerized-Job-Scheduler',

    # Set entry point for CLI
    entry_points= {
        'console_scripts' : ['djs=djs.cli.djs:main'],
        },

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
    python_requires='>=3.5',
    install_requires=[
        'click',
        'docker',
        'netcdf4',
        'numpy',
        'pandas',
        'pyyaml',
        'scipy',
        'xarray',
    ],
)
