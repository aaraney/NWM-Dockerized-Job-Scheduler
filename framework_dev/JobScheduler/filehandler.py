#!/usr/bin/env python3

import xarray as xr
from os.path import basename

'''
This module is used to link
the output of the parameter editor
to the job scheduler
'''

# Dict of unique variables in
# domain files mapped to their
# common name convention in NWM/Wrf-Hydro
# Note: GEOGRID_LDASOUT_Spatial_Metadata.nc
# is explicitly looked for based on its basename
# because it does not have a unique variable
file_type_dict = {
    'link': 'Route_link.nc',
    'basn_msk': 'Fulldom_hires.nc',
    'ALBEDO12M': 'geo_em.d01.nc',
    'Area_sqkm': 'GWBUCKPARM.nc',
    'OV_ROUGH2D': 'hydro2dtbl.nc',
    'ifd': 'LAKEPARM.nc',
    'qThresh': 'nudgingParams.nc',
    'bexp': 'soil_properties.nc',
    'weight': 'spatialweights.nc',
    'CANWAT': 'wrfinput_d01.nc'

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
        # Explicitly return GEOGRID_LDASOUT_Spatial_Metadata.nc
        elif basename(domain_file) == 'GEOGRID_LDASOUT_Spatial_Metadata.nc':
            return basename(domain_file)
    else:
        print('Check the validity of your domain files')
        raise KeyError

if __name__ == '__main__':
    file = '/Users/austinraney/Box Sync/si/nwm/domains/pocono/NWM/DOMAIN/GEOGRID_LDASOUT_Spatial_Metadata.nc'
    test_files = ['/Users/austinraney/Box Sync/si/nwm/domains/pocono/NWM/DOMAIN/Fulldom_hires.nc',
    '/Users/austinraney/Box Sync/si/nwm/domains/pocono/NWM/DOMAIN/GEOGRID_LDASOUT_Spatial_Metadata.nc',
    '/Users/austinraney/Box Sync/si/nwm/domains/pocono/NWM/DOMAIN/GWBUCKPARM.nc',
    '/Users/austinraney/Box Sync/si/nwm/domains/pocono/NWM/DOMAIN/LAKEPARM.nc',
    '/Users/austinraney/Box Sync/si/nwm/domains/pocono/NWM/DOMAIN/Route_Link.nc',
    '/Users/austinraney/Box Sync/si/nwm/domains/pocono/NWM/DOMAIN/geo_em.d01.nc',
    '/Users/austinraney/Box Sync/si/nwm/domains/pocono/NWM/DOMAIN/hydro2dtbl.nc',
    '/Users/austinraney/Box Sync/si/nwm/domains/pocono/NWM/DOMAIN/nudgingParams.nc',
    '/Users/austinraney/Box Sync/si/nwm/domains/pocono/NWM/DOMAIN/soil_properties.nc',
    '/Users/austinraney/Box Sync/si/nwm/domains/pocono/NWM/DOMAIN/spatialweights.nc',
    '/Users/austinraney/Box Sync/si/nwm/domains/pocono/NWM/DOMAIN/wrfinput_d01.nc']
    for item in test_files:
        print('{}\n{}\n\n'.format(identifyDomainFile(item),item))
