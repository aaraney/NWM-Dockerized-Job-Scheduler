#!/usr/local/bin/python3

import os
from glob import glob
import re

#temp
from pprint import pprint


class NwmDomainSetup:

    def __init__(self, master_dir, slave_dir, alt_domain_list=[], nwm_src='/nwm/Run/'):
        self.master_dir = os.path.realpath(master_dir)
        self.slave_dir = slave_dir
        self.nwm_src = os.path.realpath(nwm_src)
        self.alt_domain_list = map(lambda x: os.path.realpath(x), alt_domain_list) if len(alt_domain_list) else []

        # self.setupModel()

    def __symlink(self, src_path, dest_path):
        '''
        Create a symlink. This was added to ensure that
        full pathnames were used when linking files --
        as mpi does not handle relative links well.
        '''
        if type(src_path) == list:
            # Create symlinks for list of src_paths to dest_path
            for src_item in src_path:
                src_item_path = os.path.realpath(src_item)
                des_item_path = os.path.join(dest_path, os.path.basename(src_item_path))
                os.symlink(src_item_path, des_item_path)
        else:
            os.symlink(os.path.realpath(src_path), os.path.join(dest_path, os.path.basename(src_path)))

    def replaceDomainFiles(self, alt_domain_list):
        if not len(alt_domain_list):
            return None

        # General regex pattern is .*(?!(str1|str2|str n))$
        #
        inner_pattern = '|'.join(map(lambda x: os.path.basename(x), alt_domain_list))
        pattern = r'.*(?!({}))$'.format(inner_pattern)
        print(pattern)
        regex = re.compile(pattern)

        # This could be more general in the future
        master_domain_files = glob(os.path.join(self.master_dir, 'DOMAIN/*.nc'))
        L = list(filter(regex.match, master_domain_files))

        print(list(L))

    def setupModel(self):
        '''
        Create symbolic link of master DOMAIN, TBL,
        wrf_hydro.exe files to slave_dir. Alt_domain
        files from alt_domain_list replace default
        domain files.

        Future dev: Implement containerized database
        for writing meta_data
        '''

        CWD = os.getcwd()

        # if slave path does not exist, create it
        if not os.path.exists(self.slave_dir):
            os.mkdir(self.slave_dir)

        os.chdir(self.slave_dir)

        # Symlink TBL and wrf_hydro.exe to slave
        self.__symlink(glob(os.path.join(self.nwm_src,'*.TBL')), self.slave_dir)
        # self.__symlink(glob(os.path.join(self.nwm_src, 'wrf_hydro.exe')), self.slave_dir)

        # Symlink DOMAIN and FORCING files
        self.replaceDomainFiles(self.alt_domain_list)
        self.__symlink(self.master_dir, self.slave_dir)

if __name__=='__main__':
    master_path = '/Users/SDML/Box Sync/si/local/framework_dev/SIPSEY_WILDERNESS_DOMAIN'
    slave_path = '/Users/SDML/Box Sync/si/local/framework_dev/test1'
    nwm_path = '/Users/SDML/Box Sync/si/local/ms_domain1'

    nwm = NwmDomainSetup(master_path,slave_path,nwm_src=nwm_path)
    nwm.replaceDomainFiles(['/Users/SDML/Box Sync/si/local/framework_dev/SIPSEY_WILDERNESS_DOMAIN/DOMAIN/geo_em.d01.nc', '/Users/SDML/Box Sync/si/local/framework_dev/SIPSEY_WILDERNESS_DOMAIN/DOMAIN/Fulldom_hires.nc'])
