#!/usr/local/bin/python3

import xarray as xr

rt_lnk = "/Users/austinraney/Box Sync/si/nwm/nwm_v2_conus/RouteLink_NWMv2.0_20190517_cheyenne_pull.nc"
org_lnk = "/Users/austinraney/Box Sync/si/nwm/domains/sipsey_wilderness/Route_Link.nc"

org_rt = xr.open_dataset(org_lnk)
rt = xr.open_dataset(rt_lnk)

max_lat = max(org_rt.lat.values)
min_lat = min(org_rt.lat.values) - 0.0001
max_lon = max(org_rt.lon.values) + 0.0001
min_lon = min(org_rt.lon.values)

# print(rt.variables)
new_rt = rt.where(
    (rt.lat >= min_lat)
    & (rt.lat <= max_lat)
    & (rt.lon >= min_lon)
    & (rt.lon <= max_lon),
    drop=True,
)
# print(new_rt.variables)

new_rt.to_netcdf(
    "/Users/austinraney/Box Sync/si/nwm/nwm_v2_conus/RouteLink_NWMv2.0_20190517_cheyenne_pull_subset.nc"
)
# -87.59833,-87.26391,34.20192,34.49317
