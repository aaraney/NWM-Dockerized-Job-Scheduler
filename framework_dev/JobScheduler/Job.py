#!/usr/bin/python3

# Author: Austin Raney
# Email: aaraney@crimson.ua.edu
# Date: 7/3/19


class Job:
    '''
    Class to hold information pertaining to nwm Docker
    container used by Scheduler.py.
    '''
    def __init__(self, local_mount_point, alt_domain_list, container_id, mpi_host_file):
        self.local_mount_point = local_mount_point
        self.alt_domain_list = alt_domain_list
        self.container_id = container_id
        self.mpi_host_file = mpi_host_file

    def __str__(self):
        return 'mnt: {}\ndomain list: {}\n' \
               'container id: {}\nmpi host file: {}'.format(
            self.local_mount_point, self.alt_domain_list,
            self.container_id, self.mpi_host_file
        )

