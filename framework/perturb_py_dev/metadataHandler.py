from os.path import dirname, join, realpath
import re
import xarray as xr

def metadataDict(filePathList, metadataFileType):
    '''
    This function returns a dictionary where values
    are the metadata created by Parameter_editor.py

    :returns a dictionary where the keys are the given
    file paths from the filePathList parameter and the
    values are the adjusted parameter metadata from the
    Route_link.nc file.

    Example usage:
    metaDict = metadataDict(['/file1/frxst_out.txt', 'file2/frxst_out.txt'], 'Route_link.nc')
    '''

    if not type(filePathList) is list:
        raise TypeError

    # Get full path to DOMAIN file of interest
    metadataPathList = list(map(lambda x: realpath(join(dirname(x), 'DOMAIN/{}'.format(metadataFileType))), filePathList))

    # Get full path to, for e.g. frxst_out.txt file
    filePathList = list(map(realpath, filePathList))


    metaDict = {}

    for i, path in enumerate(metadataPathList):
        metadata = xr.open_dataset(path).attrs['Edits_made']
        # regex to match (<param-name>, <value>)
        match = re.findall('Para.(\S*\sscaled).*(\d+\.\d*)', metadata)[0]
        # iterate over metdata files e.g Route_link.nc and get pair
        # associated metadata with input e.g frxst_out.txt file in dict
        metaDict[filePathList[i]] = ': '.join(match)

    return metaDict
