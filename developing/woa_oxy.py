#!/usr/bin/env python
# coding: utf-8

import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import cmocean

def woa_oxy(filepath, month_idx, lat=41.625, lon_range=(-126.625, -124.375), depth_range=(0, 1000)):
    # Load dataset
    ds = xr.open_dataset(filepath, decode_times=False)

    # Select the geographical extent
    ds = ds.sel(lat=lat, lon=slice(*lon_range), depth=slice(*depth_range))

    # Extract temperature variable
    o_an = ds['o_an'][0, :, :]
    lon = ds['lon']
    depth = ds['depth'] 

    # Define new grid
    z_new = np.arange(0, 1000, 5)
    lon_new = np.arange(lon_range[0], lon_range[1], 0.0625)

    # Interpolate dataset
    ds_z_new = ds.interp(depth=z_new, lon=lon_new)

    # Meshgrid for plotting
    Xgrid, Ygrid = np.meshgrid(ds_z_new['lon'], ds_z_new['depth'])

    # Extract interpolated temperature
    ds_z_o_an = ds_z_new['o_an'][0, :, :]

    # # Plot
    # fig, ax = plt.subplots(1,1, figsize=(12,7), dpi=300)
    # plot = ax.contourf(Xgrid, Ygrid, ds_z_t_an, cmap=cmocean.cm.thermal, vmin=2, vmax=18)
    # ax.set_ylim(max(Ygrid.flatten()), min(Ygrid.flatten()))  # Explicitly set the y-axis limits
    # ax.set_title(f'WOA Temperature at 41.625N - Month {month_idx}')
    # ax.set_xlabel(r'Longitude ($\degree$E)')
    # ax.set_ylabel('Depth (m)')
    # cbar = plt.colorbar(plot)
    # cbar.set_label(r'Temperature ($\degree$C)')
    # save_results_to = './WOA/'
    # fig.savefig(save_results_to + f'woa_{month_idx}.png')

    # Return variables you want to save
    return {
        'lon': lon,
        'depth': depth,
        'o_an': o_an,
        'ds_z_o_an': ds_z_o_an,
        'Xgrid': Xgrid,
        'Ygrid': Ygrid
    }

# Example usage for multiple months
filepaths_oxy = [
    r'C:/Users/marqjace/TH_line/woa_climatology_data/oxygen/woa18_decav_o01_04.nc',
    r'C:/Users/marqjace/TH_line/woa_climatology_data/oxygen/woa18_decav_o02_04.nc',
    r'C:/Users/marqjace/TH_line/woa_climatology_data/oxygen/woa18_decav_o03_04.nc',
    r'C:/Users/marqjace/TH_line/woa_climatology_data/oxygen/woa18_decav_o04_04.nc',
    r'C:/Users/marqjace/TH_line/woa_climatology_data/oxygen/woa18_decav_o05_04.nc',
    r'C:/Users/marqjace/TH_line/woa_climatology_data/oxygen/woa18_decav_o06_04.nc',
    r'C:/Users/marqjace/TH_line/woa_climatology_data/oxygen/woa18_decav_o07_04.nc',
    r'C:/Users/marqjace/TH_line/woa_climatology_data/oxygen/woa18_decav_o08_04.nc',
    r'C:/Users/marqjace/TH_line/woa_climatology_data/oxygen/woa18_decav_o09_04.nc',
    r'C:/Users/marqjace/TH_line/woa_climatology_data/oxygen/woa18_decav_o10_04.nc',
    r'C:/Users/marqjace/TH_line/woa_climatology_data/oxygen/woa18_decav_o11_04.nc',
    r'C:/Users/marqjace/TH_line/woa_climatology_data/oxygen/woa18_decav_o12_04.nc',
]

# Dictionary to store the results
results = {}

for i, filepath in enumerate(filepaths_oxy, start=1):
    result = woa_oxy(filepath, month_idx=i)
    results[i] = result  # Store the result by month index

# Now the 'results' dictionary contains all the variables for each month.
woa_oxy_jan = results[1]['ds_z_o_an']
woa_oxy_feb = results[2]['ds_z_o_an']
woa_oxy_mar = results[3]['ds_z_o_an']
woa_oxy_apr = results[4]['ds_z_o_an']
woa_oxy_may = results[5]['ds_z_o_an']
woa_oxy_jun = results[6]['ds_z_o_an']
woa_oxy_jul = results[7]['ds_z_o_an']
woa_oxy_aug = results[8]['ds_z_o_an']
woa_oxy_sep = results[9]['ds_z_o_an']
woa_oxy_oct = results[10]['ds_z_o_an']
woa_oxy_nov = results[11]['ds_z_o_an']
woa_oxy_dec = results[12]['ds_z_o_an']