#!/usr/bin/env python3

# Author: Austin Raney
# Email: aaraney@crimson.ua.edu
# Date: 7/3/19

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
        # self.mpi_host_file = mpi_host_file

    def __str__(self):
        return 'mnt: {}\nparent mnt: {}\ndomain list: {}\ncontainer_id: {}' \
               .format(
            self.replica_mnt_point, self.primary_mnt_point,
            self.alt_domain_list,self.container_id
        )

    @property
    def container_id(self):
        return self._container_id

    @container_id.setter
    def container_id(self, id):
        self._container_id = id
