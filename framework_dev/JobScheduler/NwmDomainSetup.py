#!/usr/local/bin/python3

from os import link, makedirs, remove
from os.path import join, realpath, basename, dirname
from glob import glob


class NwmDomainSetup(object):

    def __init__(self, master_dir, slave_dir, alt_domain_list=[], nwm_src='/nwm/Run/', setup_model=True):
        self.master_dir = realpath(master_dir)
        self._master_parent_dir = dirname(self.master_dir)
        self.slave_dir = slave_dir
        self.nwm_src = realpath(nwm_src)
        self.alt_domain_list = list(map(lambda x: realpath(x), alt_domain_list) if len(alt_domain_list) else [])

        self.setupModel() if setup_model else None

    def __str__(self):
        return 'slave mnt: {}\nmaster mnt: {}\nalt domain list: {}\nnwm src: {}' \
            .format(
            self.slave_dir, self.master_dir,
            self.alt_domain_list, self.nwm_src
        )

    @classmethod
    def fromJob(cls, job, setup_model=True):
        master_dir = job.parent_mnt_point
        slave_dir = job.mnt_point
        alt_domain_list = job.alt_domain_list
        return cls(master_dir, slave_dir, alt_domain_list, setup_model=setup_model)

    @property
    def master_parent_dir(self):
        return self._master_parent_dir

    def cleanUp(self):
        '''
        Remove forcings and restarts
        Aggregate files to better location
        '''
        pass

    def createSlave(self):
        '''
        Creates slave dir in parent dir of the master
        i.e.
        if master is /master, slave will be created
        at /slave
        '''
        # undecided if I want to make this function or not
        pass

    def __link(self, dest_dir, *src_files):
        '''
        Create a symlink. This was added to ensure that
        full pathnames were used when linking files --
        as mpi does not handle relative links well.
        '''
        # link full path of src file to dest_dir using
        # the name of src file
        def _link(src):
            link(realpath(src), join(dest_dir, basename(src)))
        try:
            if src_files:
                for item in src_files:
                    _link(item)
        except FileExistsError:
            # handle existing links
            for item in src_files:
                remove(join(dest_dir, basename(item)))
            self.__link(dest_dir, *src_files)

    def populateDomainFiles(self, alt_domain_list):
        # This could be recoded in the future to be more
        # readable/better coded.

        # set of master domain files
        master_domain_files = set(glob(join(self.master_dir, 'DOMAIN/*.nc')))

        # helper function for finding matching domain files
        # this should be coded differently
        join_master_dir = lambda x: join(self.master_dir, 'DOMAIN/{}'.format(basename(x)))

        try:
            for item in alt_domain_list:
                if join_master_dir(item) in master_domain_files:
                    master_domain_files.remove(join_master_dir(item))
                    master_domain_files.add(item)
            return list(master_domain_files)

        except:
            # if no alt domain files, then just return master
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

        # Create dirs
        makedirs(self.slave_dir, exist_ok=True)
        makedirs(join(self.slave_dir, 'DOMAIN'), exist_ok=True)
        makedirs(join(self.slave_dir, 'FORCING'), exist_ok=True)


        # Symlink TBL and wrf_hydro.exe to slave
        # THIS NEEDS TO BE CHANGED TO INTERACT WITH CONTAINER
        # self.__link(self.slave_dir, *glob(join(self.nwm_src, '*.TBL')))
        # self.__link(self.slave_dir, 'wrf_hydro.exe')

        # mkdir and symlink DOMAIN and FORCING files
        domain_file_list = self.populateDomainFiles(self.alt_domain_list)

        self.__link(join(self.slave_dir, 'DOMAIN'), *domain_file_list)
        self.__link(join(self.slave_dir, 'FORCING'), *glob(join(self.master_dir, 'FORCING/*')))

        # link namelist files
        self.__link(self.slave_dir, *glob(join(self.master_dir, '*namelist*')))
        # self.__link(domain_file_list, join(self.slave_dir, 'DOMAIN'))
        # self.__link(join(self.master_dir, 'FORCING'), join(self.slave_dir, 'FORCING'))


if __name__=='__main__':
    from JobScheduler.Job import Job
    master_path = '/Users/austinraney/Box Sync/si/sandbox/framework_test/master_domain'
    slave_path = '/Users/austinraney/Box Sync/si/sandbox/framework_test/slave_domain'
    nwm_path = '/Users/austinraney/Box Sync/si/local/ms_domain1'
    domain_files = ['/Users/austinraney/Box Sync/si/sandbox/docker_testing/framework_test/master_domain/DOMAIN/geo_em.d01.nc']

    j = Job(slave_path, master_path, domain_files)
    # nwm = NwmDomainSetup(slave_path, master_path, domain_files)
    nwm_job = NwmDomainSetup.fromJob(j, setup_model=False)
    print(nwm_job)


