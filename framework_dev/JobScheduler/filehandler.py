#!/usr/bin/env python3

import xarray as xr

'''
This module is used to link
the output of the parameter editor
to the job scheduler
'''

# Dict of unique variables in
# domain files mapped to their
# common name convention in NWM/Wrf-Hydro
# TODO: Add other unique keys and files names
file_type_dict = {
    'link': 'Route_link.nc'
}

def identifyDomainFile(domain_file):
    '''
    Return the NWM filename convention
    of the input file.
    e.g.
    identifyDomainFile('Route_link123.nc) -> 'Route_link.nc'
    '''
    domain_file_xr = xr.open_dataset(domain_file)
    for key in file_type_dict:
        if key in domain_file_xr.keys():
            return file_type_dict[key]
    else:
        print('Check the validity of your domain files')
        raise KeyError

if __name__ == '__main__':
    file = "/Users/austinraney/Box Sync/si/nwm/domains/pocono/Route_Link.nc"
    x = xr.open_dataset(file)
    print(identifyDomainFile(file))
