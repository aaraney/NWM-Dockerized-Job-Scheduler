import xarray as xr
import numpy as np
from SALib.sample import latin


# --------------------------------------------------------------------------------------------------
# ---------------------------------  functions -----------------------------------------------------
# --------------------------------------------------------------------------------------------------
# Function to modify the input files in the netcdf file

def cross_section_area_BlckBrn(TopWdth):
    '''(Top Width of Trapezoidal Channel)'''
    # This function calculates the cross section area from Topwidth using Blackburn et al. equations
    cs_area = 0.75 * ((TopWdth / 2.44) ** (1.0 / 0.34)) ** 0.53

    return cs_area

def metadata_string(parameter, opperator, amount, key='p'):
    '''
    key is either p or d depending on if the parameter is dependent or not
    '''
    return '{3}: {0}-{1}-{2}'.format(parameter,opperator, amount, key)

def para_editor_evenly_scaler(ds, para_name, scale):
    '''(dateset, parameter name to be modified, scale)'''
    # This function scales the chosen parameter and the dependent parameters if any.

    # For now, don't play with 'TopWdth'
    valid_para_to_edit = {'ChSlp', 'n', 'nCC', 'TopWdth', 'TopWdthCC', 'BtmWdth'}
    if para_name not in valid_para_to_edit:
        raise ValueError("results: parameter_name to be edited must be one of %r." % valid_para_to_edit)


    ds[para_name][:] *= scale  # Modify the parameter
    ds.attrs['Edits_made'] += metadata_string(para_name, '*', scale) # Modify the MetaData

    # !!!Be advised: should better define the cs_area, currently, it is a xarray dataframe and the variable name is
    # not correct...but it works!
    if para_name == 'ChSlp':
        #  Following 2 equations are from Blackburn et al.
        cs_area = cross_section_area_BlckBrn(ds['TopWdth'][:])  # cs_area is not a varaible in NWM dataframe
        # but is necessary to be calculated in order to be able to calculate BtmWdth to

        # Be careful of neg values being root squared: happens when dramatically decrease ChSlp
        ds['BtmWdth'][:] = (ds['TopWdth'][:] ** 2 - 4.0 * cs_area * ds['ChSlp'][:]) ** 0.5

        # ds.attrs['Edits_made'] += ' ** Also, para ' + 'BtmWdth' + ' was changed as dependent para '  # Modify the MetaData
        # TODO: Might need to add for dependent parameter case?
        ds.attrs['Edits_made'] += metadata_string('BtmWdth', '', '', key='d')


    if para_name == 'BtmWdth':
        #  Following 2 equations are from Blackburn et al.
        cs_area = cross_section_area_BlckBrn(ds['TopWdth'][:])
        ds['ChSlp'][:] = (ds['TopWdth'][:] ** 2 - ds['BtmWdth'][:] ** 2) / (4.0 * cs_area)

        # ds.attrs['Edits_made'] += ' ** Also, param ' + 'ChSlp' + ' was changed as dependent para '  # Modify the MetaData
        # TODO: Might need to add for dependent parameter case?
        ds.attrs['Edits_made'] += metadata_string('ChSlp', '', '', key='d')

    return ds

def para_editor_evenly_scaler_multi_para(InputFilename, outputpath, para_names, scales_list):
    '''(Input file to be edited, outputpath, list of parameters to be edited, list of scales corresponding to the parameters)'''
    # This function scales multiple parameters and the dependent parameters if any.

    # TODO: For Iman: Raise values error when len(para_names) != len(scales_list)
    ds = xr.open_dataset(InputFilename)  # Open the netcdf file

    ds1 = ds  # Copy the dataset
    ds1.attrs['Edits_made'] = ''  # Add Global Attribute to track the changes made on parameters

    # edit the netcdf files
    for i, para_name in enumerate(para_names):
        ds1 = para_editor_evenly_scaler(ds1, para_name, scales_list[i])

    # TODO: do sth like this: f = open(os.path.join(reportfile_directory, "PerfMetrReport.csv"), "w")
    # Create the outputfile name
    for i, para_name in enumerate(para_names):
        outputpath += '_p' + str(i) + '_' + para_name + '_sc_' + str(scales_list[i])
    outputpath += '.nc'

    # Create the edited netcdf file
    ds1.to_netcdf(outputpath)

    # #  Read the edited netcdf file
    # ds1.close()
    # del ds1
    # ds1 = xr.open_dataset(outputpath)  # Open the netcdf file

    return ds1, outputpath  # Austing said change to outputpath


def para_editor_streamorder_based_scaler(ds, para_name, streamorder_list, scale_list):
    '''(dateset, parameter name to be modified, scaler list for each streamorder)'''
    # This function scales the chosen parameter and the dependent parameters if any.

    # TODO: For Iman: Raise values error when len(para_names) != len(scales_list)
    valid_para_to_edit = {'ChSlp', 'n', 'nCC', 'TopWdth', 'TopWdthCC', 'BtmWdth'}
    if para_name not in valid_para_to_edit:
        raise ValueError("results: parameter_name to be edited must be one of %r." % valid_para_to_edit)

    for i, streamorder in enumerate(streamorder_list):
        ds[para_name] = xr.where(ds.order == streamorder, ds[para_name] * scale_list[i], ds[para_name])

    ds.attrs['Edits_made'] += '|| Para ' + para_name + ' scaled by scales ' + str(scale_list) + ' for streamorders ' + str(streamorder_list)  # Modify the MetaData


    # !!!Be advised: should better define the cs_area, currently, it is a xarray dataframe and the variable name is
    # not correct...but it works!
    if para_name == 'ChSlp':

        #  Following 2 equations are from Blackburn et al.
        cs_area = cross_section_area_BlckBrn(ds['TopWdth'][:])
        # Be careful of neg values being root squared: happens when dramatically decrease ChSlp
        ds['BtmWdth'][:] = (ds['TopWdth'][:] ** 2 - 4.0 * cs_area * ds['ChSlp'][:]) ** 0.5
        ds.attrs['Edits_made'] += ' ** Also, para ' + 'BtmWdth' + ' was changed as dependent para '  # Modify the MetaData

    if para_name == 'BtmWdth':
        #  Following 2 equations are from Blackburn et al.
        cs_area = cross_section_area_BlckBrn(ds['TopWdth'][:])
        ds['ChSlp'][:] = (ds['TopWdth'][:] ** 2 - ds['BtmWdth'][:] ** 2) / (4.0 * cs_area)
        ds.attrs['Edits_made'] += ' ** Also, param ' + 'ChSlp' + ' was changed as dependent para '  # Modify the MetaData

    return ds

# --------------------------------------------------------------------------------------------------
# -------------------------------------------- Main ------------------------------------------------
# --------------------------------------------------------------------------------------------------

Filename = r'C:\Users\Iman\Desktop\example_case\NWM\DOMAIN_DEFAULT\Route_Link.nc'
outputpath = r'C:\Users\Iman\Desktop\Route_Link'


# --------------------------------- Example of Evenly Scaler ---------------------------------------
# params_list = ['BtmWdth', 'n', 'nCC']  # parameters to be edited
params_list = ['BtmWdth']  # parameters to be edited

# # Define the model inputs for SALib.sample.latin
# problem = {
#     'num_vars': len(params_list),
#     'names': params_list,
#     'bounds': [[0.001, 1.5],
#                [0.5, 1.5],
#                [0.5, 1.5]]
# }

# Define the model inputs for SALib.sample.latin
problem = {
    'num_vars': len(params_list),
    'names': params_list,
    'bounds': [[0.001, 1.5],
]
}

# Generate the parameter space based on latin hypercube sampling
scales_list_of_lists = (np.round(latin.sample(problem, 25), 3)).tolist()
# scales_list_of_lists = [[1.1, 1.2, 1.5], [1.1, 1.2, 4], [1.1, 1.2, 5],
#                         [1.1, 1.2, 6], [1.1, 1.2, 10], [1.1, 1.2, 20]] # Arbitrarily chosen

for scales_list in scales_list_of_lists:
    ds1, outputpath_final = para_editor_evenly_scaler_multi_para(Filename, outputpath, params_list, scales_list)

    print('\n**********************')
    # print('First value for ' + 'ChSlp' + ': ', ds1['ChSlp'][0].values)
    print('First value for ' + 'BtmWdth' + ': ', ds1['BtmWdth'][0].values)
    # print('First value for ' + 'TopWdth' + ': ', ds1['TopWdth'][0].values)
    # print('First value for ' + 'CrossSectionArea' + ': ', 0.75 * ((ds1['TopWdth'][0].values / 2.44) ** (1.0 / 0.34)) ** 0.53)
    # print('First value for ' + 'n' + ': ', ds1['n'][0].values)
    # print('First value for ' + 'nCC' + ': ', ds1['nCC'][0].values)
    print(ds1.Edits_made.split('||'))


# --------------------------Example of Scaler based on Streamorder ----------------------------------
para_name = 'BtmWdth'
ds = xr.open_dataset(Filename)

# Create list of streamorders present in the domain file
Streamorder_list = []
for i in range(int(min(ds.order)), int(max(ds.order))+1):
    Streamorder_list.append(i)

# Arbitrarily, create list of scalers corrsoponding to each streamorder
# scaler_list = []
# if max(ds.order) == 5:
#     scaler_list = [0.65, 0.75, 0.90, 1.1, 1.25]
# elif max(ds.order) == 4:
#     scaler_list = [0.75, 0.9, 1.1, 1.25]
#
# if (max(ds.order) % 2) == 0:
#     a = 1/(((len(list))+1)/2.0)
# else:
#     a =

a = 1/(((len(Streamorder_list))+1)/2.0)
scaler_list = [round(i * a, 3) for i in Streamorder_list]

ds.attrs['Edits_made'] = ''  # Add Global Attribute to track the changes made on parameters
ds1 = para_editor_streamorder_based_scaler(ds, para_name, Streamorder_list, scaler_list)

# Create the outputfile name
for i, Streamorder in enumerate(Streamorder_list):
    outputpath += '_p_' + para_name + '_Streamorder_' + str(Streamorder) + '_sc_' + str(scaler_list[i])
outputpath += '.nc'

# Create the edited netcdf file
ds1.to_netcdf(outputpath)
