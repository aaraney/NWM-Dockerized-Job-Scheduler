import xarray as xr
import numpy as np

# rt_lnk = "C:/Users/Iman/Desktop/RouteLink_NWMv2.0_20190517_cheyenne_pull.nc"
# org_lnk = "C:/Users/Iman/Desktop/sipsey_wilderness/Route_Link.nc"
#
# org_rt = xr.open_dataset(org_lnk)
# rt = xr.open_dataset(rt_lnk)
#
# max_lat = max(org_rt.lat.values)
# min_lat = min(org_rt.lat.values) - 0.0001
# max_lon = max(org_rt.lon.values) + 0.0001
# min_lon = min(org_rt.lon.values)
#
# # print(rt.variables)
# new_rt = rt.where((rt.lat >= min_lat) & (rt.lat <= max_lat) & (rt.lon >= min_lon) & (rt.lon <= max_lon), drop=True)
# # print(new_rt.variables)
#
# new_rt.to_netcdf("C:/Users/Iman/Desktop/RouteLink_NWMv2.0_20190517_cheyenne_pull_subset.nc")
# # -87.59833,-87.26391,34.20192,34.49317


# Function to modify the input files in the netcdf file
def para_editor(File_name, para_name , editing_mode = 'Scl', scale = 1.1):
    '''(netcdf file path and name, parameter name to be modified, editing mode: 'Scl' for Scaler and 'StOr' for BasedoOnStreamOrder , scale)'''

    valid_para_to_edit = {'ChSlp', 'n', 'nCC', 'TopWdth', 'TopWdthCC', 'BtmWdth'}
    editing_mode_list = {'Scl', 'StOr'}

    if para_name not in valid_para_to_edit:
        raise ValueError("results: parameter_name to be edited must be one of %r." % valid_para_to_edit)

    if editing_mode not in editing_mode_list:
        raise ValueError("results: editing_mode must be one of %r." % editing_mode_list)

    ds = xr.open_dataset(File_name) # Open the netcdf file
    print('opened file: ', File_name)

    if editing_mode == 'Scl':
        ds[para_name][:] *= scale  # Modify the parameter

        # !!!Be advised: should better define the cs_area, currently, it is a xarray dataframe and the variable name is
        # not correct...but it works!
        if para_name == 'ChSlp':
            #  Following 2 equations are from Blackburn et al.
            cs_area = 0.75*((ds['TopWdth'][:]/2.44)**(1.0 / 0.34))**0.53  # cs_area is not a varaible in NWM dataframe
                                                                          # but is necessary to be calculated in order
                                                                          # to be able to calculate BtmWdth to

            # Be careful of neg values being root squared: happens when dramatically decrease ChSlp
            ds['BtmWdth'][:] = (ds['TopWdth'][:]**2-(4.0*cs_area)/ds['ChSlp'][:])**0.5


        if para_name == 'BtmWdth':
            #  Following 2 equations are from Blackburn et al.
            cs_area = 0.75 * ((ds['TopWdth'][:] / 2.44) ** (1.0 / 0.34)) ** 0.53
            # cs_area is not a varaible in NWM dataframe
            # but is necessary to be calculated in order
            # to be able to calculate BtmWdth to

            ds['ChSlp'][:] = 4.0 * cs_area / (ds['TopWdth'][:] ** 2 - ds['BtmWdth'][:] ** 2)



    # !!!Be advised: Currently StOr is NOT complete
    if editing_mode == 'StOr':
        for i in range(int(max(new_rt.order.values))):
            ds[para_name] = xr.where(ds.order == i, ds[para_name] * scale * (i / 10 + 1), ds[para_name])

    return ds


def copier(xr_dataframe, outputpath):
    '''(Output from function para_editor which is an edited RouteLink xarray dataset, path to copy the file)'''

    xr_dataframe.to_netcdf(outputpath)


#################################################################################
###                                     Main                                  ###
#################################################################################

Para = 'BtmWdth'  # parameter to be edited

# A simple parameter perturber
scale_list = []
for i in np.arange(0.4, 1.66667, 0.2):  # Do not exceed 1.66667, as by keeping TopWdth constant and multiplying BtmWdth
                                    # by 1.66667, it will get bigger than TopWdth leading to a reverse trapezoidal which
                                    # is not what we want...
    scale_list.append(i)

# Input netcdf file for study area
FileName = "C:/Users/Iman/Desktop/RouteLink_NWMv2.0_20190517_cheyenne_pull_subset.nc"

# Edited netcdf file
outputpath = "C:/Users/Iman/Desktop/RouteLink_NWMv2.0_20190517_cheyenne_pull_subset_edit"

# perturb parameter, edit file, copy the edited file, and repeat...
for counter, scale in enumerate(scale_list):
    print('\nCounter: ', counter+1, '  Scaler: ', scale)

    new2_rt = para_editor(FileName, Para , editing_mode='Scl', scale=scale)

    # Print some of the parameters after perturb
    print('First value for ' + 'ChSlp' + ': ', new2_rt['ChSlp'][0].values)
    print('First value for ' + 'BtmWdth' + ': ', new2_rt['BtmWdth'][0].values)
    print('First value for ' + 'TopWdth' + ': ', new2_rt['TopWdth'][0].values)
    print('First value for ' + 'CrossSectionArea' + ': ', 0.75*((new2_rt['TopWdth'][0].values/2.44)**(1.0 / 0.34))**0.53)
    print('First value for ' + 'n' + ': ', new2_rt['n'][0].values)

    copier(new2_rt, outputpath + '_para_' + Para + '_scale_' + str(scale) + '.nc')



