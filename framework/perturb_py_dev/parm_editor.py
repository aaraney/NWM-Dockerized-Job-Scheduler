import xarray as xr
import numpy as np
import operator
from SALib.sample import latin

# TODO: impliment a function to create the methods_dict used by the
# edit_parameters function

# Local package imports 
# TODO: Change relative imports
import sys
sys.path.append('..')
from JobScheduler import filehandler

def metadata_string(parameter, op, value, key=''):
    '''
    Key is d, if parameter is dependent on another parameter, requiring it to also be edited
    '''
    return '{3} {0}-{1}-{2}'.format(parameter, op, value, key)

def _map_to_operator(op):
    '''
    Map operators (+, -, /, *, etc.) taken as strings to in-place operators

    ^ and ** are analogous for in-place raise to a power. ^ does NOT represent an xor

    ex: 
        _map_to_operator('+') -> operator.iadd

    See: https://docs.python.org/3.7/library/operator.html#in-place-operators
    for list of operators. Only in-place ops supported
    '''

    op_dict = {
    '+' : operator.iadd,
    '//' : operator.ifloordiv,
    '<<' : operator.ilshift,
    '%' : operator.imod,
    '*' : operator.imul,
    '**' : operator.ipow,
    '^': operator.ipow,
    '>>' : operator.irshift,
    '-' : operator.isub,
    '/' : operator.itruediv,
    # equals is special case. Need to provide slice( len(df['param']) )
    '=' : operator.setitem
    }

    try:
        return(op_dict[op])

    except KeyError:
        raise(KeyError('Operator "{}" not supported. Please use standard python numeric operators'))

def _create_operator_value_pair(op, value):
    '''
    Return a list, where the first index is an inplace operator function and
    the second index a value to be applied using the function.

    ex:
        _create_operator_value_pair('+', 5) -> [operator.iadd, 5]
    '''

    return( [_map_to_operator(op), value] )

def _apply_functions(df, key, value_list): 
    ''' 
    Takes in list of functions and instance variable values then preform
    operation to df[key] value_list 

    Return augmented df

    ex:
        [operator.iadd, 3, operator.imul, 5]
    '''

    if len(value_list) < 2:
        return

    func = value_list[0]
    arg = value_list[1]

    # Check  for special case when operator is '=', see _create_operator_value_pairs()
    if func.__name__ ==  'setitem':
        func( df[key], slice(0, len(df[key])), arg )

    else:
        func( df[key][:], arg )

    _apply_functions(df, key, value_list[2:])

def load_parameter_file(fn):
    '''
    Load a netcdf and check if it is a valid file for usage by the
    perturbation engine. Return a dataframe of representation of the file if
    it is a valid file and the parameters capible of being varried.

    load_parameter_file -> (df, {parameter names})
    '''

    # Dictionary of valid filenames using Wrf-Hydro/NWM name conventions
    # with valid paramters to vary as their values
    valid_files_to_edit = {
    'Route_Link.nc': {'ChSlp', 'n', 'nCC', 'TopWdth', 'TopWdthCC', 'BtmWdth'},
    'GWBUCKPARM.nc' : {'Expon', 'Zinit', 'Zmax'},
    'LAKEPARM.nc' : {'OrificeA', 'OrificeC', 'OrificeE', 'WeirC', 'WeirE', 'WeirL'},
    'Soil_properties.nc': {'mfsno'},
    'Fulldom_hires.nc' : {'LKSATFAC', 'OVROUGHRTFAC', 'RETDEPRTFAC'}
    }

    try:
        fn_w_nwm_naming_convention = filehandler.identifyDomainFile(fn)
        valid_params = valid_files_to_edit[fn_w_nwm_naming_convention]

        df = xr.open_dataset(fn)

        return( (df, valid_params) )

    # KeyError thrown by filehandler if not a valid NWM file
    except KeyError:
        raise IOError('The provided parameter file, {}, is not valid, please provide a valid WRF-Hydro/NWM parameter file'.format(fn))

def edit_parameters(fn, methods_dict):
    '''
    Augment one or more parameters from the passed dataframe.

    df:
        NWM/Wrf-Hydro parameter file having been passed as dataframe

    methods_dict:
        A dictionary with parameter names stored as keys and values stored as stack using POSTFIX notation

    See: https://docs.python.org/3.7/library/operator.html#in-place-operators for list of operators. Only in-place ops supported

    '''

    # Load provided files and the valid parameters to edit for that file type
    df, valid_parameters = load_parameter_file(fn)

    # Check that provided parameter names can be varried
    if len(set(methods_dict.keys()) - valid_parameters) > 0:
        raise IOError('Input parameters {} are not valid'.format((set(methods_dict.keys()) - valid_parameters)))

    for key, value in methods_dict.items():
        _apply_functions(df, key, value)

def 

def edit_parameter(fn, ds, para_name, scale):
    '''
    This function scales the chosen parameter and the dependent parameters if
    any.
    '''

    valid_files_to_edit = {
    'Route_Link.nc': {'ChSlp', 'n', 'nCC', 'TopWdth', 'TopWdthCC', 'BtmWdth'},
    'GWBUCKPARM.nc' : {'Expon', 'Zinit', 'Zmax'},
    'LAKEPARM.nc' : {'OrificeA', 'OrificeC', 'OrificeE', 'WeirC', 'WeirE', 'WeirL'},
    'Soil_properties.nc': {'mfsno'},
    'Fulldom_hires.nc' : {'LKSATFAC', 'OVROUGHRTFAC', 'RETDEPRTFAC'}
    }

    try:
        fn_w_nwm_naming_convention = filehandler.identifyDomainFile(fn)
        ds = xr.open_dataset(InputFilepath + '\\' + InputFilename)  # Open the netcdf file

        valid_params = valid_files_to_edit[fn]

        param_to_edit = valid_params[para_name]

    except ValueError:
        raise IOError('The provided parameter, {}, is not valid, please provide' \
                      ' a valid WRF-Hydro/NWM parameter for the input file {}'.format(para_name, valid_files_to_edit))

    # KeyError thrown by filehandler if not a valid NWM file
    except KeyError:
        raise IOError('The provided parameter file, {}, is not valid, please provide a valid WRF-Hydro/NWM parameter file'.format(fn))


    # Something like:

    # Need to make call to verify what kind of file it is, should be able to use function from Job Scheduler
    try:
        valid_params = valid_files_to_edit[fn] 

        param_to_edit = valid_params[para_name]

    except ValueError:
        raise IOError('The provided parameter, {}, is not valid, please provide' \
                      ' a valid WRF-Hydro/NWM parameter for the input file {}'.format(para_name, valid_files_to_edit)
                      )

    except KeyError:
        raise IOError('The provided parameter file, {}, is not valid, please provide a valid WRF-Hydro/NWM parameter file'.format(valid_files_to_edit))




    valid_files_to_edit = {'Route_Link.nc', 'GWBUCKPARM.nc', 'LAKEPARM.nc', 'Soil_properties.nc', 'Fulldom_hires.nc'}

    if fn not in valid_files_to_edit:
        raise ValueError("results: file_name to be edited must be one of %r." % valid_files_to_edit)

    if fn == 'Route_link.nc':
        # For now, don't play with 'TopWdth'
        valid_para_to_edit = {'ChSlp', 'n', 'nCC', 'TopWdth', 'TopWdthCC', 'BtmWdth'}
        if para_name not in valid_para_to_edit:
            raise ValueError("results: parameter_name to be edited must be one of %r." % valid_para_to_edit)


    elif fn == 'GWBUCKPARM.nc':
        # For now, don't play with 'TopWdth'
        valid_para_to_edit = {'Expon', 'Zinit', 'Zmax'}
        if para_name not in valid_para_to_edit:
            raise ValueError("results: parameter_name to be edited must be one of %r." % valid_para_to_edit)


    elif fn == 'LAKEPARM.nc':
        # For now, don't play with 'TopWdth'
        valid_para_to_edit = {'OrificeA', 'OrificeC', 'OrificeE', 'WeirC', 'WeirE', 'WeirL'}
        if para_name not in valid_para_to_edit:
            raise ValueError("results: parameter_name to be edited must be one of %r." % valid_para_to_edit)


    elif fn == 'Soil_properties.nc':
        # For now, don't play with 'TopWdth'
        valid_para_to_edit = {'mfsno'}
        if para_name not in valid_para_to_edit:
            raise ValueError("results: parameter_name to be edited must be one of %r." % valid_para_to_edit)


    elif fn == 'Fulldomain_hires.nc':
        # For now, don't play with 'TopWdth'
        valid_para_to_edit = {'LKSATFAC', 'OVROUGHRTFAC', 'RETDEPRTFAC'}
        if para_name not in valid_para_to_edit:
            raise ValueError("results: parameter_name to be edited must be one of %r." % valid_para_to_edit)


    ds[para_name][:] *= scale  # Modify the parameter
    ds.attrs['Edits_made'] = metadata_string(para_name, '*', scale) # Modify the MetaData

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
        # Following 2 equations are from Blackburn et al.
        # The calculation of updated Channel slope IS NOT consistent
        # with current manuscripts, however it is correct despite not being
        # documented correctly in Wrf-Hydro documentation.
        cs_area = cross_section_area_BlckBrn(ds['TopWdth'][:])
        ds['ChSlp'][:] = 1/((ds['TopWdth'][:] ** 2 - ds['BtmWdth'][:] ** 2) / (4.0 * cs_area))

        # TODO: Might need to add for dependent parameter case?
        ds.attrs['Edits_made'] = metadata_string('ChSlp', '', '', key='d')

    return ds

def para_editor_evenly_scaler_multi_para(InputFilepath, InputFilename, outputpath, para_names, scales_list):
    '''(Input file to be edited, outputpath, list of parameters to be edited, list of scales corresponding to the parameters)'''
    # This function scales multiple parameters and the dependent parameters if any.

    # TODO: For Iman: Raise values error when len(para_names) != len(scales_list)
    ds = xr.open_dataset(InputFilepath + '\\' + InputFilename)  # Open the netcdf file

    ds1 = ds  # Copy the dataset

    attr = ''
    # edit the netcdf files
    for i, para_name in enumerate(para_names):
        ds1 = para_editor_evenly_scaler(InputFilename, ds1, para_name, scales_list[i])
        attr = attr + ds1.attrs['Edits_made']

    ds1.attrs['Edits_made'] = attr  # Add Global Attribute to track the changes made on parameters

    # TODO: do sth like this: f = open(os.path.join(reportfile_directory, "PerfMetrReport.csv"), "w")
    # Create the outputfile name
    for i, para_name in enumerate(para_names):
        outputpath += '_p' + str(i) + '_' + para_name + '_sc_' + str(scales_list[i])
    outputpath += '.nc'

    # Create the edited netcdf file
    ds1.to_netcdf(outputpath)

    return ds1, outputpath  # Austing said change to outputpath


# TODO: Handle the streamorder problem metadata and also changing mulitiple parameters at the same time
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

if __name__ == "__main__":
    import sys
    sys.path.append('..')
    from JobScheduler import filehandler