#!/usr/bin/env python3

from os import makedirs
from pathlib import Path

# Local import
from .filehandler import identify_domain_file


def _clean_up(job):
    """
    Remove forcings and restarts
    Aggregate files to better location
    """
    # TODO: Implement this method
    pass


def _link(dest_dir, *src_files):
    """
    src_files accepted as n args or dict with
    key = common file name (e.g. Fulldom_hires.nc)
    value = src path

    Create a symlink. This was added to ensure that
    full pathnames were used when linking files --
    as mpi does not handle relative links well.
    """
    # If there are no src files, return none
    if not len(src_files):
        return None

    elif type(src_files[0]) is dict:
        src_files_dict = src_files[0]
        # for common name (i.e. Fulldom_hires.nc), source path
        for common_name, src in src_files_dict.items():
            # link primary to replica with correct common name
            Path(src).resolve().symlink_to(Path(dest_dir, common_name))

    else:
        # Link full path of src file to dest_dir using
        # the name of src file
        def __link(src):
            Path(src).resolve().symlink_to(Path(dest_dir, Path(src).name))

        try:
            if src_files:
                for item in src_files:
                    __link(item)
        except FileExistsError:
            # handle existing links
            for item in src_files:
                Path(dest_dir, Path(item).name).unlink
            _link(dest_dir, *src_files)


def _populate_domain_files(primary_dir, alt_domain_list):
    """
    :returns dict of domain files to be linked to
    replica directory. Accounts for differences in files names
    and replaces primary domain files with the correct alternative
    ones
    """
    if not type(alt_domain_list) is list:
        alt_domain_list = [alt_domain_list]
    # set of primary domain files
    primary_domain_files = list(Path(primary_dir).glob("DOMAIN/*.nc"))

    # Dictionary of key = Common name convention (i.e. 'Fulldom_hires.nc')
    # and value = source of the file
    # Note: GEOGRID_LDASOUT_Spatial_Metadata.nc
    # is explicitly linked, meaning the input filename
    # does matter, unlike the other files
    # See filehandler.py for a better understanding
    primary_domain_dict = {}
    for src in primary_domain_files:
        common_name = identify_domain_file(src)
        primary_domain_dict[common_name] = src

    # Replace source src location of default domain files
    # with the location of alternative domain files
    for alt_src in alt_domain_list:
        common_name = identify_domain_file(alt_src)
        primary_domain_dict[common_name] = alt_src

    return primary_domain_dict


def _setup_model(job):
    """
    Create symbolic link of primary DOMAIN, TBL,
    wrf_hydro.exe files to slave_dir. Alt_domain
    files from alt_domain_list replace default
    domain files.

    Future dev: Implement containerized database
    for writing meta_data
    """

    primary_dir = job.primary_mnt_point
    replica_dir = job.replica_mnt_point
    alt_domain_list = job.alt_domain_list

    # Check if DOMAIN and FORCING exist in primary directory
    if (
        not Path(primary_dir, "DOMAIN").is_dir()
        and not Path(primary_dir, "FORCING").is_dir()
    ):
        raise Exception("DOMAIN or FORCING directory not present in primary directory")

    # Create dirs
    makedirs(replica_dir, exist_ok=True)
    makedirs(Path(replica_dir, "DOMAIN"), exist_ok=True)
    makedirs(Path(replica_dir, "FORCING"), exist_ok=True)
    makedirs(Path(replica_dir, "RESTART"), exist_ok=True)

    # Link DOMAIN and FORCING files
    domain_file_dict = _populate_domain_files(primary_dir, alt_domain_list)

    _link(Path(replica_dir, "DOMAIN"), domain_file_dict)
    _link(Path(replica_dir, "FORCING"), *Path(primary_dir).glob("FORCING/*"))
    _link(Path(replica_dir, "RESTART"), *Path(primary_dir).glob("RESTART/*"))

    # link namelist files
    _link(Path(replica_dir), Path(primary_dir, "hydro.namelist"))
    _link(Path(replica_dir), Path(primary_dir, "namelist.hrldas"))
