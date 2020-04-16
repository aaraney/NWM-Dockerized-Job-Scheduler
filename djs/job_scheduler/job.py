#!/usr/bin/env python3

from os.path import realpath


class Job(object):
    '''
    Class to hold information pertaining to nwm Docker
    container used by Scheduler.py.

    NOTE:
        The parameter alt_domain_list is inaptly named as of now.
        Currently only one file is supported by the Scheduler
    '''
    def __init__(self, replica_mnt_point, primary_mnt_point, alt_domain_list):
        self.replica_mnt_point = replica_mnt_point
        self.primary_mnt_point = primary_mnt_point
        self.alt_domain_list = alt_domain_list
        self._container_id = None

    def __str__(self):
        # Only print the first 12 characters of the id
        return f'''mount point: {self.replica_mnt_point}
        alternate files: {self.alt_domain_list}
        container_id: {self._container_id.id[:12]}'''

    @property
    def container_id(self):
        return self._container_id

    @container_id.setter
    def container_id(self, id):
        self._container_id = id
