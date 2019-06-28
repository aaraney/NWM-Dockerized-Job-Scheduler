import xarray as xr
import os

InputDir = 'C:/Users/Iman/Desktop/sipsey_wilderness/'
filename = 'Route_Link.nc'

ds = xr.open_dataset(os.path.join(InputDir, filename), autoclose=True)
print('opened file')

ds['ChSlp'][:] *= 4  # Modify the parameter

# Create a copy of the netcdf file with modified  parameter
ds.to_netcdf(os.path.join(InputDir, filename.split('.')[0] + '_2' + '.' + filename.split('.')[1]))
