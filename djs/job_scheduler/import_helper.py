#!/usr/bin/env python3

def from_yaml(yaml_setup_file):
    '''
    Fills job queue from a provided yaml file

    Note: Absolute and relative paths are accepted
    Required keys and values for yaml file(these are case sensitive)

    primary: '/path/to/your/primary/'
    alternative-files:
        - '/path/to/alt/file'
        - '/path/to/alt/file'

    Optional key value pairs
    image: 'docker/image' default aaraney/nwm-djs:2.0
    max-jobs: <int> (e.g., 3) default 2
    cpus: <str> (e.g., '0-4') default '0-1'
    mpi-np: <int> (e.g., 3) default 2

    NOTE:
        Currently model runs are only supported that
        have a single changed domain files per run.
        '''
    from .scheduler import Scheduler
    return Scheduler.fromYaml(yaml_setup_file)


def from_list(primary_dir, alt_domain_list):
    '''
    Fill jobs queue from list of file names

    The alt domain list files will attempt to have
    their full path mapped to the list, however it
    is *best practice* to provide a list of absolute
    paths. Code for this in Job.py

    NOTE:
        Currently model runs are only supported that
        have a single changed domain files per run.
    '''
    from .scheduler import Scheduler
    return Scheduler.fromList(primary_dir, alt_domain_list)