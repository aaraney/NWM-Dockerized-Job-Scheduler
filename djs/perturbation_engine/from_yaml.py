#!/usr/bin/env python

import yaml
import xarray as xr
from os import access, W_OK
from os.path import basename, dirname, splitext
from typing import Dict, List, Set, Tuple, Union

# Local imports
from djs.perturbation_engine.parameter_editor import _check_parameter_validity, perturb_parameters

def perturb_from_yaml(setup_file):
    '''
    Apply scalar or randomly sampled values to WRF-Hydro/NWM model parameters
    using in-place operator (i.e. +=, *=) operand pairs or fitted statistical
    distribution random sampling using yaml file inputs.

    YAML setup file structure:

        path-to-paramterfile.nc:
            - parameter_name:
                output (optional): output-filename
                perturbation-method: operator operand pairs OR boolean

            - group_of_parameters:
                output (optional): group-output-filename
                parameter_name_0:
                    perturbation-method: operator operand pairs OR boolean
                parameter_name_1:
                    perturbation-method: operator operand pairs OR boolean

    Supported WRF-Hydro/NWM parameters:
        Route_link.nc: BtmWdth, ChSlp, n, nCC, TopWdth, TopWdthCC, BtmWdth
        GWBUCKPARM.nc : Expon, Zinit, Zmax
        LAKEPARM.nc : OrificeA, OrificeC, OrificeE, WeirC, WeirE, WeirL
        soil_properties.nc: mfsno
        Fulldom_hires.nc : LKSATFAC, OVROUGHRTFAC, RETDEPRTFAC

    Supported operators:
        +, -, *, /, ^ OR **, =, %, //, <<, >>

    Supported distribution:
        normal, gamma, uniform

    Random samples are applied using a single sample (e.g. df[parameter][:] =
    1) or a ubiquitous random sampling. Distributions fitting parameters are
    estimated using an MLE using the values from the input df. The ubiquitous
    apply bool controls sampling, True results in ubiquitous random sampling,
    False results in a single random sample applied equally to the parameter.
    
    Example setup file:

        /home/example/NWM-Docker-Ensemble-Framework/pocono_test_case/Route_Link.nc:
            - group1:
                output: 'ChSlp_nCC_scalar.nc'
                ChSlp:
                    scalar: '- 2'
                nCC:
                    scalar: '* 3'
            - n:
                output: 'n_normal.nc'
                norm: True
            - TopWdthCC:
                gamma: False
                scalar: '* 1'
        /home/example/NWM-Docker-Ensemble-Framework/pocono_test_case/primary/DOMAIN/Fulldom_hires.nc:
            - LKSATFAC:
                output: ubiquitous_uniform_Fulldom_hires.nc
                uniform: True
    '''

    # Read in setup yaml file 
    with open(setup_file, 'r') as setup:
        setup_file = yaml.safe_load(setup)

    # Outter most loop that steps through filename keys
    for filenames, parameter_list in setup_file.items():

        _parameter_df, valid_parameters = _check_parameter_validity(filenames)

        # Inner loop that steps through parameter name keys OR groups
        for parameter_dict in parameter_list:

            # Create copy of dataframe
            parameter_df = _parameter_df.copy()

            # Get the key name as a string. Should be valid parameter or group,
            # which is just a nested set of valid parameters
            current_parameter = list(parameter_dict)[0]

            # This could be either operations to preform on a parameter or the
            # outer part of a group
            op_dict = parameter_dict[current_parameter]

            # If the key is a valid parameter
            if current_parameter in valid_parameters:

                # Try to get output file 
                try:
                    output_fn = op_dict.pop('output')

                # output_fn not provided
                except KeyError:
                    # Original input file without the file extention
                    output_fn = splitext(filenames)[0]
                    output_fn = '{}_djs_{}.nc'.format(output_fn, current_parameter)

                # Check for scalar, if not scalar should be dist
                operator_operand_pair_list = _value_parser(op_dict)
                parameter_df = perturb_parameters(parameter_df, {current_parameter: operator_operand_pair_list})

                # Save perturbed parameter file 
                _save_output(parameter_df, output_fn)

            # Group case
            else:
                # Alias to existing variables for readability
                group_name = current_parameter
                group_dict = op_dict

                # Try to get output file 
                try:
                    output_fn = group_dict.pop('output')
                # output_fn not provided
                except KeyError:
                    # Original input file without the file extention
                    output_fn = splitext(filenames)[0]
                    output_fn = '{}_djs_{}.nc'.format(output_fn, group_name)

                # Check for scalar, if not scalar should be dist
                group_operator_operand_pair_list = {parameter: _value_parser(method) for (parameter, method) in group_dict.items()}
                # operator_operand_pair_list = _value_parser(group_dict)
                parameter_df = perturb_parameters(parameter_df, group_operator_operand_pair_list)

                # Save perturbed parameter file 
                _save_output(parameter_df, output_fn)

def _save_output(parameter_df, output_fn, index=0):
    '''
    Save netcdf file, avoid collitions by incrimenting 1 to the filename.
    '''
    try:
    # Save output perturbed parameter file
        parameter_df.to_netcdf(output_fn)

    except PermissionError:
        output_fn_dirname = dirname(output_fn)

        # Check for write access to dir
        if access(output_fn_dirname, W_OK):

            output_fn = splitext(output_fn)[0]
            _save_output(parameter_df, '{}{}.nc'.format(output_fn, index+1), index = index+1)
        else:
            raise PermissionError('Check the directory permissions for the location you are trying to save')

def _value_parser(op_dict: Dict[str, Union[bool, str]]) -> List[Tuple[Union[bool, str, int, float]]]:
    '''
    Map a dictionary of scalar/dist methods to a list of tuples

    Ex:
            _value_parser({'scalar': '+ 3'}) -> [('+', 3.0)]
            _value_parser({'scalar': '+ 3 % 5'}) -> [('+', 3.0), ('%', 5.0)]
            _value_parser({'norm': False, 'scalar': '% 5'}) -> [('norm', False), ('%', 5.0)]
    '''
    operator_operand_pair_list = []
    for (k, v) in op_dict.items():
        if k == 'scalar':
            operator_operand_pair_list += _scalar_value_parser(v)
        else:
            operator_operand_pair_list += [(k, v)]
    
    return operator_operand_pair_list

def _scalar_value_parser(op_operand: str) -> Tuple[Union[str, int, float]]:
    '''
    Map string of operator operand pairs to a list of tuples.

    Ex:
        _scalar_value_parser('+ 3') -> [('+', 3.0)]
        _scalar_value_parser('+ 3 % 5') -> [('+', 3.0), ('%', 5.0)]
    '''
    # Transform to list and replace multiple spaces with a single space
    op_operand = op_operand.split()

    op_operand_length = len(op_operand)

    if ( op_operand_length % 2 ) == 1:
        raise ValueError(f'Scalar operations {op_operand} passed were not the correct format. i.e. "* 0.3" or "+ 3 - 3 + 6')

    ops = op_operand[::2]
    args = list(map(float, op_operand[1::2]))

    return list(zip(ops, args))