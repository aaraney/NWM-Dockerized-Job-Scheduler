#!/usr/bin/env python3

import xarray as xr
from os.path import basename
from typing import Union

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

def identifyDomainFile(domain_file: Union[str, xr.core.dataset.Dataset]):
    '''
    Return the NWM filename convention of the input file. Accepts a filename
    as a string or an xarray dataset dataset
    e.g.
    identifyDomainFile('Route_link123.nc) -> 'Route_link.nc'
    '''
    if type(domain_file) is str:
        domain_file = xr.open_dataset(domain_file)

    for key in file_type_dict:
        if key in domain_file.keys():
            return file_type_dict[key]

    else:
        raise KeyError('Check the validity of your domain files.\nNote: GEOGRID_LDASOUT_Spatial_Metadata.nc is not supported file')
