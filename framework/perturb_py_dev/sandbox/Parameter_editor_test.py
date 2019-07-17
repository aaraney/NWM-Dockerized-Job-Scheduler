import sys
from os.path import realpath
sys.path.append(realpath('../'))
from Validation import readNWMoutput_csv_ensemble

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
    'bounds': [[0.001, 1.5]]
}

# Generate the parameter space based on latin hypercube sampling
scales_list_of_lists = (np.round(latin.sample(problem, 25), len(params_list))).tolist()


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


# # --------------------------Example of Scaler based on Streamorder ----------------------------------
# para_name = 'BtmWdth'
# ds = xr.open_dataset(Filename)
#
# # Create list of streamorders present in the domain file
# Streamorder_list = []
# for i in range(int(min(ds.order)), int(max(ds.order))+1):
#     Streamorder_list.append(i)
#
# # Arbitrarily, create list of scalers corrsoponding to each streamorder
# # scaler_list = []
# # if max(ds.order) == 5:
# #     scaler_list = [0.65, 0.75, 0.90, 1.1, 1.25]
# # elif max(ds.order) == 4:
# #     scaler_list = [0.75, 0.9, 1.1, 1.25]
# #
# # if (max(ds.order) % 2) == 0:
# #     a = 1/(((len(list))+1)/2.0)
# # else:
# #     a =
#
# a = 1/(((len(Streamorder_list))+1)/2.0)
# scaler_list = [round(i * a, 3) for i in Streamorder_list]
#
# ds.attrs['Edits_made'] = ''  # Add Global Attribute to track the changes made on parameters
# ds1 = para_editor_streamorder_based_scaler(ds, para_name, Streamorder_list, scaler_list)
#
# # Create the outputfile name
# for i, Streamorder in enumerate(Streamorder_list):
#     outputpath += '_p_' + para_name + '_Streamorder_' + str(Streamorder) + '_sc_' + str(scaler_list[i])
# outputpath += '.nc'
#
# # Create the edited netcdf file
# ds1.to_netcdf(outputpath)