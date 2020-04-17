#!/usr/bin/env python3

def from_yaml(yaml_setup_file):
    '''
    Fills job queue from a provided yaml file

    Note: Absolute and relative paths are accepted
    Required keys and values for yaml file(these are case sensitive)

    Alternative-files key accepts nested lists, this will link the files
    in the nested list to the same simulation, thus allowing for numerous
    alternate files to be used.

    Job Scheduler yaml format:
        primary: '/path/to/your/primary/'
        alternative-files:
            - '/path/to/alt/file'
            -
              - '/path/to/alt/file1'
              - '/path/to/alt/file2'
            ..
            - '/path/to/alt/file'

    Optional key value pairs:
        image: 'docker/image' default aaraney/nwm-djs:2.0
        max-jobs: <int> (e.g., 3) default 2
        cpus: <str> (e.g., '0-4') default '0-1'
        mpi-np: <int> (e.g., 3) default 
        '''
    from .scheduler import Scheduler
    return Scheduler.from_yaml(yaml_setup_file)


def from_list(primary_dir, alt_domain_list):
    '''
    Fill jobs queue from list of file names.

    The alt domain list files will attempt to have their full path mapped
    to the list, however it is *best practice* to provide a list of
    absolute paths.

    alt_domain_list is accepted as nested lists, this will link the files
    in the nested list to the same simulation, thus allowing for numerous
    alternate files to be used.
    '''
    from .scheduler import Scheduler
    return Scheduler.from_list(primary_dir, alt_domain_list)