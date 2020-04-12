#!/usr/bin/env python3

import xarray as xr
import numpy as np
import operator
from typing import Dict, List, Union
from os.path import basename

from djs.job_scheduler.filehandler import identifyDomainFile

def _check_parameter_validity(parameter_file: Union[str, xr.core.dataset.Dataset]):
    '''

    Load a netcdf or check that an existing dataset is a valid file for usage
    by the perturbation engine. Return dataframe of representation of the
    file if it is a valid file and the parameters capible of being varried.

    _check_parameter_validity -> (df, {parameter names})
    '''

    # Dictionary of valid filenames using Wrf-Hydro/NWM name conventions
    # with valid paramters to vary as their values
    valid_files_to_edit = {
    'Route_link.nc': {'ChSlp', 'n', 'nCC', 'TopWdth', 'TopWdthCC', 'BtmWdth'},
    'GWBUCKPARM.nc' : {'Expon', 'Zinit', 'Zmax'},
    'LAKEPARM.nc' : {'OrificeA', 'OrificeC', 'OrificeE', 'WeirC', 'WeirE', 'WeirL'},
    'soil_properties.nc': {'mfsno'},
    'Fulldom_hires.nc' : {'LKSATFAC', 'OVROUGHRTFAC', 'RETDEPRTFAC'}
    }

    if type(parameter_file) is str:
        parameter_file = xr.open_dataset(parameter_file)

    try:
        fn_w_nwm_naming_convention = identifyDomainFile(parameter_file)
        valid_params = valid_files_to_edit[fn_w_nwm_naming_convention]

        return( (parameter_file, valid_params) )

    # KeyError thrown by filehandler if not a valid NWM file
    except KeyError:
        raise IOError('The provided parameter file, {}, is not valid, please provide a valid WRF-Hydro/NWM parameter file'.format(basename(parameter_file._file_obj._filename)))

def _metadata_string(parameter, op, value, key=''):
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
    # equals is special case. Setting `=` is handled explicitly within functions checking for setitem function name
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

    return( [op, value] )

def _create_parameter_operator_dict(parameters, operators, values):
    '''

    Take a list of: parameters, operators, and values and return a dictionary
    with keys=parameters and values a list of operator value tuples

    '''

    if not len(parameters) == len(operators) == len(values):
        raise IndexError('Check that number of provided parameters, operators, and values equal the same length')

    parameter_dict = {}

    for index, parameter in enumerate(parameters):

        # If parameter already key in dictionary, then append to the list of
        # operator, value tuples
        if parameter in parameter_dict.keys():
            parameter_dict[parameter].append( (operators[index], values[index]) )
        
        else:
            parameter_dict[parameter] = [ (operators[index], values[index]) ] 

    # Check to make sure dictionary isnt empty
    if len(parameter_dict.keys()):
        return parameter_dict
    
    else:
        raise KeyError('There were no parameter, operator, value pairs provided')

def _apply_functions(df, parameter_operator_dict): 
    ''' 

    Map string representations of mathmatical operations to in-place (+=, -=, *=, etc. )
    operations and apply these operations on dataframe parameters

    Take a dataframe and dictionary, with keys=parameters and values = [ (operator, value), ... ]
    
    Return augmented COPY of df

    Example:
        parameter_operator_dict = 
            {
                'TopWdth' : [ ('*', 1.2) ] 
            }

            # '*' gets mapped to its in-place operator representation. Then 1.2
            # is applied using the function mapping to the df @ the parameter
            # specified as the key in the dictionary
            # This is an tautologic representation:
            # df['TopWdth'] *= 1.2
            
            operator.imul( df['TopWdth'], 1.2 )
    '''

    local_df = df.copy()

    for parameter, operator_value_list in parameter_operator_dict.items():

        # Loop through operator value pairs and apply to dataframe
        for func_value_pair in operator_value_list:

            # str representation of function
            str_func = func_value_pair[0]
            value = func_value_pair[1]

            func = _map_to_operator(str_func) 
            operator_name = func.__name__

            # Check  for special case when operator is '=', see _create_operator_value_pairs()
            if operator_name ==  'setitem':
                local_df[parameter][:] = value

            else:
                local_df[parameter] = func( local_df[parameter][:], value )

            # Tag the dataframe with metadata concerning the change
            if 'perterbation_engine_edits:' in local_df.attrs:
                local_df.attrs['perterbation_engine_edits:'] += _metadata_string( parameter, str_func, value )

            else:
                local_df.attrs['perterbation_engine_edits:'] = _metadata_string( parameter, str_func, value )

    return local_df

def _apply_dists(df: xr.core.dataset.Dataset, parameter_operator_dict: Dict[str, List[Union[str, bool]]]) -> xr.core.dataset.Dataset:
    '''
    TODO: Docstring should still be expanded
    Apply random values sampled from statistical distribution to parameter
    values. Random samples are either applied using a single sample or a
    contemporaneous random sampling. Distributions fitting parameters are
    estimated using an MLE and the values from the input df. 

    Supported distribution:
        normal, gamma, uniform

    parameter_operator_dict:
        {
        <parameter-name> :
            [<dist-name>, <contemporaneous-apply-bool>]
        }

    Example:
        parameter_operator_dict = 
                {
                    'TopWdth' : ['gamma', False]
                }
    '''

    # import dist functions
    from scipy.stats import norm, gamma, uniform

    # Copy of input df that will be returned
    local_df = df.copy()

    parameter = list(parameter_operator_dict)[0]
    dist_type = parameter_operator_dict[parameter][0]
    apply_bool = bool(parameter_operator_dict[parameter][1])

    parameter_datatype = eval(f'np.{str(df[parameter].dtype)}')
    parameter_shape = df[parameter].shape
    parameter_size = df[parameter].size

    # Fit distribution
    mle_fit = eval(f'{dist_type}.fit(df[parameter][:])')

    if apply_bool:
        rvs = eval(f'{dist_type}.rvs(*mle_fit, size = parameter_size).reshape(*parameter_shape)')
    else:
        rvs = eval(f'{dist_type}.rvs(*mle_fit, size = 1)')

    # rvs = eval('func(rvs)')

    apply_dict = {parameter: [('=', rvs)]}

    df = _apply_functions(local_df, apply_dict)
    return df

def edit_parameters(df, parameters, operators, values):
    '''
    Return augmented parameter dataframe

    df:
        NWM/Wrf-Hydro parameter file as a filename string or xarray dataset
    
    parameters:
        List of parameters to edit

    operators:
        List of operators to be evaluated with values resulting in parameter changes

    values:
        List of values applied using operators

    '''

    # Check that provided file contains valid parameters to edit for that file type
    df, valid_parameters = _check_parameter_validity(df)

    parameter_operator_dict = _create_parameter_operator_dict(parameters, operators, values)

    # Intersection between provided parameter names and parameters that can be varried is not zero 
    parameter_intersection = set(parameter_operator_dict.keys()) & valid_parameters

    # Check that intersection 
    if not len( parameter_intersection ):
        raise IOError('Input parameters {} are not valid'.format( ( set(parameter_operator_dict.keys()) - valid_parameters ) ))

    return _apply_functions(df, parameter_operator_dict) 

# Code below has been kept mainly to preserve the thoughts held within the
# code. This will be refactored into either functions or implemented within
# existing functions 

# # TODO: Handle the streamorder problem metadata and also changing mulitiple parameters at the same time
# def para_editor_streamorder_based_scaler(ds, para_name, streamorder_list, scale_list):
#     '''(dateset, parameter name to be modified, scaler list for each streamorder)'''
#     # This function scales the chosen parameter and the dependent parameters if any.

#     # TODO: For Iman: Raise values error when len(para_names) != len(scales_list)
#     valid_para_to_edit = {'ChSlp', 'n', 'nCC', 'TopWdth', 'TopWdthCC', 'BtmWdth'}
#     if para_name not in valid_para_to_edit:
#         raise ValueError("results: parameter_name to be edited must be one of %r." % valid_para_to_edit)

#     for i, streamorder in enumerate(streamorder_list):
#         ds[para_name] = xr.where(ds.order == streamorder, ds[para_name] * scale_list[i], ds[para_name])

#     ds.attrs['Edits_made'] += '|| Para ' + para_name + ' scaled by scales ' + str(scale_list) + ' for streamorders ' + str(streamorder_list)  # Modify the MetaData


#     # !!!Be advised: should better define the cs_area, currently, it is a xarray dataframe and the variable name is
#     # not correct...but it works!
#     if para_name == 'ChSlp':

#         #  Following 2 equations are from Blackburn et al.
#         cs_area = cross_section_area_BlckBrn(ds['TopWdth'][:])
#         # Be careful of neg values being root squared: happens when dramatically decrease ChSlp
#         ds['BtmWdth'][:] = (ds['TopWdth'][:] ** 2 - 4.0 * cs_area * ds['ChSlp'][:]) ** 0.5
#         ds.attrs['Edits_made'] += ' ** Also, para ' + 'BtmWdth' + ' was changed as dependent para '  # Modify the MetaData

#     if para_name == 'BtmWdth':
#         #  Following 2 equations are from Blackburn et al.
#         cs_area = cross_section_area_BlckBrn(ds['TopWdth'][:])
#         ds['ChSlp'][:] = (ds['TopWdth'][:] ** 2 - ds['BtmWdth'][:] ** 2) / (4.0 * cs_area)
#         ds.attrs['Edits_made'] += ' ** Also, param ' + 'ChSlp' + ' was changed as dependent para '  # Modify the MetaData

#     return ds
