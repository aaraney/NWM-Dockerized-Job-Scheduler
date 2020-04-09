#!/usr/bin/env python3

from os import link, makedirs, remove
from os.path import join, realpath, basename, dirname, isdir
from glob import glob

# Local import
from .filehandler import identifyDomainFile


def cleanUp(job):
    '''
    Remove forcings and restarts
    Aggregate files to better location
    '''
    # TODO: Implement this method
    pass

def __link(dest_dir, *src_files):
    '''
    src_files accepted as n args or dict with
    key = common file name (e.g. Fulldom_hires.nc)
    value = src path

    Create a symlink. This was added to ensure that
    full pathnames were used when linking files --
    as mpi does not handle relative links well.
    '''
    # If there are no src files, return none
    if not len(src_files):
        return None

    elif type(src_files[0]) is dict:
        src_files_dict = src_files[0]
        # for common name (i.e. Fulldom_hires.nc), source path
        for common_name, src in src_files_dict.items():
           # link primary to replica with correct common name
            link(realpath(src), join(dest_dir, common_name))

    else:
        # Link full path of src file to dest_dir using
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
            __link(dest_dir, *src_files)

def populateDomainFiles(primary_dir, alt_domain_list):
    '''
    :returns dict of domain files to be linked to
    replica directory. Accounts for differences in files names
    and replaces primary domain files with the correct alternative
    ones
    '''
    if not type(alt_domain_list) is list:
        alt_domain_list = [alt_domain_list]
    # set of primary domain files
    primary_domain_files = list(glob(join(primary_dir, 'DOMAIN/*.nc')))

    # Dictionary of key = Common name convention (i.e. 'Fulldom_hires.nc')
    # and value = source of the file
    # Note: GEOGRID_LDASOUT_Spatial_Metadata.nc
    # is explicitly linked, meaning the input filename
    # does matter, unlike the other files
    # See filehandler.py for a better understanding
    primary_domain_dict = {}
    for src in primary_domain_files:
        common_name = identifyDomainFile(src)
        primary_domain_dict[common_name] = src

    # Replace source src location of default domain files
    # with the location of alternative domain files
    for alt_src in alt_domain_list:
        common_name = identifyDomainFile(alt_src)
        primary_domain_dict[common_name] = alt_src

    return primary_domain_dict


def setupModel(job):
    '''
    Create symbolic link of primary DOMAIN, TBL,
    wrf_hydro.exe files to slave_dir. Alt_domain
    files from alt_domain_list replace default
    domain files.

    Future dev: Implement containerized database
    for writing meta_data
    '''

    primary_dir = job.primary_mnt_point
    replica_dir = job.replica_mnt_point
    alt_domain_list = job.alt_domain_list

    # Check if DOMAIN and FORCING exist in primary directory
    if not isdir(join(primary_dir, 'DOMAIN')) and not isdir(join(primary_dir, 'FORCING')):
        raise Exception('DOMAIN or FORCING directory not present in primary directory')

    # Create dirs
    makedirs(replica_dir, exist_ok=True)
    makedirs(join(replica_dir, 'DOMAIN'), exist_ok=True)
    makedirs(join(replica_dir, 'FORCING'), exist_ok=True)
    makedirs(join(replica_dir, 'RESTART'), exist_ok=True)

    # Link DOMAIN and FORCING files
    domain_file_dict = populateDomainFiles(primary_dir, alt_domain_list)

    __link(join(replica_dir, 'DOMAIN'), domain_file_dict)
    __link(join(replica_dir, 'FORCING'), *glob(join(primary_dir, 'FORCING/*')))
    __link(join(replica_dir, 'RESTART'), *glob(join(primary_dir, 'RESTART/*')))

    # link namelist files
    __link(join(replica_dir), join(primary_dir, 'hydro.namelist'))
    __link(join(replica_dir), join(primary_dir, 'namelist.hrldas'))
