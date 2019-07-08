#!/usr/local/bin/python3

from os import mkdir, symlink
from os.path import join, realpath, basename, exists
from glob import glob


class NwmDomainSetup:

    def __init__(self, master_dir, slave_dir, alt_domain_list=[], nwm_src='/nwm/Run/'):
        self.master_dir = realpath(master_dir)
        self.slave_dir = slave_dir
        self.nwm_src = realpath(nwm_src)
        self.alt_domain_list = list(map(lambda x: realpath(x), alt_domain_list) if len(alt_domain_list) else [])

        self.setupModel()

    def __symlink(self, src_path, dest_path):
        '''
        Create a symlink. This was added to ensure that
        full pathnames were used when linking files --
        as mpi does not handle relative links well.
        '''
        # May need to add handler for existing links
        if type(src_path) == list:
            # Create symlinks for list of src_paths to dest_path
            for src_item in src_path:
                src_item_path = realpath(src_item)
                des_item_path = join(dest_path, basename(src_item_path))
                symlink(src_item_path, des_item_path)
        else:
            symlink(realpath(src_path), join(dest_path, basename(src_path)))

    def replaceDomainFiles(self, alt_domain_list):
        # This could be recoded in the future to be more
        # readable/better coded.
        if not len(alt_domain_list):
            return []

        master_domain_files = set(glob(join(self.master_dir, 'DOMAIN/*.nc')))
        join_master_dir = lambda x: join(self.master_dir, 'DOMAIN/{}'.format(basename(x)))

        for item in alt_domain_list:
            if join_master_dir(item) in master_domain_files:
                master_domain_files.remove(join_master_dir(item))
                master_domain_files.add(item)
        return list(master_domain_files)

    def setupModel(self):
        '''
        Create symbolic link of master DOMAIN, TBL,
        wrf_hydro.exe files to slave_dir. Alt_domain
        files from alt_domain_list replace default
        domain files.

        Future dev: Implement containerized database
        for writing meta_data
        '''

        # if slave path does not exist, create it
        if not exists(self.slave_dir):
            mkdir(self.slave_dir)

        # Symlink TBL and wrf_hydro.exe to slave
        # THIS NEEDS TO BE CHANGED TO INTERACT WITH CONTAINER
        self.__symlink(glob(join(self.nwm_src, '*.TBL')), self.slave_dir)
        self.__symlink(glob(join(self.nwm_src, 'wrf_hydro.exe')), self.slave_dir)

        # mkdir and symlink DOMAIN and FORCING files
        domain_file_list = self.replaceDomainFiles(self.alt_domain_list)

        mkdir(join(self.slave_dir, 'DOMAIN'))
        mkdir(join(self.slave_dir, 'FORCING'))

        self.__symlink(domain_file_list, join(self.slave_dir, 'DOMAIN'))
        self.__symlink(join(self.master_dir, 'FORCING'), join(self.slave_dir, 'FORCING'))


if __name__=='__main__':
    master_path = '/Users/austinraney/Box Sync/si/local/framework_dev/SIPSEY_WILDERNESS_DOMAIN'
    slave_path = '/Users/austinraney/Box Sync/si/local/framework_dev/test1'
    nwm_path = '/Users/austinraney/Box Sync/si/local/ms_domain1'
    domain_files = ['/Users/austinraney/Box Sync/si/nwm/domains/cahaba_nwm_subset/f495f0293071225d21af98fa455e148662c442b8/geo_em.d01.nc', '/Users/austinraney/Box Sync/si/nwm/domains/cahaba_nwm_subset/f495f0293071225d21af98fa455e148662c442b8/Route_Link.nc']

    nwm = NwmDomainSetup(master_path,slave_path,nwm_src=nwm_path,alt_domain_list=domain_files)
