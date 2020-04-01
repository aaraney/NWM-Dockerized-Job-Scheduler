def evenly_scale(xr_obj, parameter_name, scale):
    '''
    Input: xarray netcdf object, parameter name,
    '''
    # This function scales the chosen parameter and the dependent parameters if any.

    # For now, don't play with 'TopWdth'
    valid_para_to_edit = {'ChSlp', 'n', 'nCC', 'TopWdth', 'TopWdthCC', 'BtmWdth'}
    if parameter_name not in valid_para_to_edit:
        raise ValueError("results: parameter_name to be edited must be one of %r." % valid_para_to_edit)


    xr_obj[parameter_name][:] *= scale  # Modify the parameter
    xr_obj.attrs['Edits_made'] = metadata_string(parameter_name, '*', scale) # Modify the MetaData

    # !!!Be advised: should better define the cs_area, currently, it is a xarray dataframe and the variable name is
    # not correct...but it works!
    if parameter_name == 'ChSlp':
        #  Following 2 equations are from Blackburn et al.
        cs_area = cross_section_area_BlckBrn(xr_obj['TopWdth'][:])  # cs_area is not a varaible in NWM dataframe
        # but is necessary to be calculated in order to be able to calculate BtmWdth to

        # Be careful of neg values being root squared: happens when dramatically decrease ChSlp
        xr_obj['BtmWdth'][:] = (xr_obj['TopWdth'][:] ** 2 - 4.0 * cs_area * xr_obj['ChSlp'][:]) ** 0.5

        # ds.attrs['Edits_made'] += ' ** Also, para ' + 'BtmWdth' + ' was changed as dependent para '  # Modify the MetaData
        # TODO: Might need to add for dependent parameter case?
        xr_obj.attrs['Edits_made'] += metadata_string('BtmWdth', '', '', key='d')


    if parameter_name == 'BtmWdth':
        # Following 2 equations are from Blackburn et al.
        # The calculation of updated Channel slope IS NOT consistent
        # with current manuscripts, however it is correct despite not being
        # documented correctly in Wrf-Hydro documentation.
        cs_area = cross_section_area_BlckBrn(xr_obj['TopWdth'][:])
        xr_obj['ChSlp'][:] = 1/((xr_obj['TopWdth'][:] ** 2 - xr_obj['BtmWdth'][:] ** 2) / (4.0 * cs_area))

        # TODO: Might need to add for dependent parameter case?
        xr_obj.attrs['Edits_made'] += metadata_string('ChSlp', '', '', key='d')

    return xr_obj