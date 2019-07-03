#!/usr/bin/python3

'''
Author: Austin Raney
Email: aaraney@crimson.ua.edu
Date: 7/3/19
'''

class Job:
    '''
    Class to hold information pertaining to nwm Docker
    container used by Scheduler.py.
    '''
    def __init__(self, local_mount_point, changed_domain_file, mpi_host_file):
        self.local_mount_point = local_mount_point
        self.changed_domain_file = changed_domain_file
        self.mpi_host_file = mpi_host_file
