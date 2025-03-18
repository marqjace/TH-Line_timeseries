#!/usr/bin/env python
# coding: utf-8

# Imports
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
from matplotlib import colors
from datetime import datetime
import pandas as pd
import woa_temp
import woa_salt
import transects_func

# Function to load WOA climatology data
def load_woa_data():
    temp_data = [woa_temp.woa_temp_jan, woa_temp.woa_temp_feb, woa_temp.woa_temp_mar, woa_temp.woa_temp_apr, woa_temp.woa_temp_may, woa_temp.woa_temp_jun, woa_temp.woa_temp_jul, woa_temp.woa_temp_aug, woa_temp.woa_temp_sep, woa_temp.woa_temp_oct, woa_temp.woa_temp_nov, woa_temp.woa_temp_dec]
    salt_data = [woa_salt.woa_salt_jan, woa_salt.woa_salt_feb, woa_salt.woa_salt_mar, woa_salt.woa_salt_apr, woa_salt.woa_salt_may, woa_salt.woa_salt_jun, woa_salt.woa_salt_jul, woa_salt.woa_salt_aug, woa_salt.woa_salt_sep, woa_salt.woa_salt_oct, woa_salt.woa_salt_nov, woa_salt.woa_salt_dec]
    return temp_data, salt_data

# Function to calculate anomalies
def calculate_anomalies(transect_data, climatology_data):
    anomalies = {}
    for i, (transect, clim) in enumerate(zip(transect_data, climatology_data)):
        anomalies[f'transect_{i+1}'] = np.subtract(transect, clim)
    return anomalies

# Function to process SCTI/ONI data
def process_scti_oni_data(filepath):
    dat = xr.open_dataset(filepath, decode_times=False)
    scti = dat['scti']
    oni = dat['oni']
    scti_time = dat['time']
    time2 = [datetime.fromtimestamp(int(value)).toordinal() for value in scti_time]
    scti_time = xr.DataArray(time2)
    return scti, oni, scti_time

# Function to process California MOCI data
def process_moci_data(filepath):
    dat2 = pd.read_csv(filepath)
    dat2 = dat2.drop(['FID', 'Year', 'Season', 'months', 'geometry'], axis=1)
    dat2 = dat2.set_index(['time'])
    norcal = dat2.where(dat2['location'] == 'North California (38-42N)')
    norcal_time = norcal.index
    norcal_moci = norcal['moci']
    norcal_time2 = [pd.to_datetime(value).toordinal() for value in norcal_time]
    norcal_moci = xr.DataArray(norcal_moci)
    norcal_time = xr.DataArray(norcal_time2)
    return norcal_time, norcal_moci

# Function to process transect data
def process_transect_data(transect_func):
    temp_data = [getattr(transect_func, f'temp_{i}_{j}') for i in range(12, 25) for j in ['a', 'b'] if hasattr(transect_func, f'temp_{i}_{j}')]
    salt_data = [getattr(transect_func, f'salt_{i}_{j}') for i in range(12, 25) for j in ['a', 'b'] if hasattr(transect_func, f'salt_{i}_{j}')]
    return temp_data, salt_data

# Function to create a regular grid
def create_grid(xmin, xmax, xn, ymin, ymax, yn):
    xgrid = np.linspace(xmin, xmax, xn)
    ygrid = np.linspace(ymin, ymax, yn)
    Xgrid, Ygrid = np.meshgrid(xgrid, ygrid)
    return Xgrid, Ygrid

# Function to interpolate and grid data
def interpolate_grid(data, Xgrid, Ygrid):
    combined_data = xr.concat(data, dim='time')
    combined_data = combined_data.interp(time=np.arange(combined_data['time'].min(), combined_data['time'].max(), 30), depth=np.arange(-10, 1000, 5), method='linear')
    return combined_data

# Function to plot data
def plot_data(Xgrid, Ygrid, data, title, ylabel, cbar_label, cmap, norm, levels, filename):
    fig, ax = plt.subplots(figsize=(14, 8), dpi=300)
    plot = ax.contourf(Xgrid, Ygrid, data, cmap=cmap, norm=norm, levels=levels)
    lines = ax.contour(Xgrid, Ygrid, data, colors='black', norm=norm, levels=levels, alpha=0.75)
    ax.clabel(lines, lines.levels, inline=True, fontsize=10)
    ax.invert_yaxis()
    ax.set_ylabel(ylabel)
    ax.set_title(title, pad=10)
    cbar = plt.colorbar(plot, shrink=0.5, location='right', pad=0.015)
    cbar.outline.set_linewidth(2)
    cbar.set_label(label=cbar_label, rotation=0, labelpad=10)
    plt.tight_layout()
    plt.savefig(filename)

# Main script
if __name__ == "__main__":
    # Load WOA climatology data
    # Data Access Here: https://www.ncei.noaa.gov/access/world-ocean-atlas-2018/bin/woa18.pl
    temp_clim, salt_clim = load_woa_data()

    # Process SCTI/ONI data
    # Data Access Here: https://spraydata.ucsd.edu/products/socal-index/
    scti, oni, scti_time = process_scti_oni_data('C:/Users/marqjace/TH_line/scti_oni/socal_index_monthly_v1_8571_f367_229e_U1723054143245.nc')

    # Process California MOCI data
    norcal_time, norcal_moci = process_moci_data('C:/Users/marqjace/TH_line/california_moci/california_moci.csv')

    # Process transect data
    temp_data, salt_data = process_transect_data(transects_func)

    # Debugging: Print shapes and types of temp_data
    print("Shapes and types of temp_data:")
    for i, data in enumerate(temp_data):
        print(f"temp_data[{i}]: shape={data.shape}, type={type(data)}")

    # Debugging: Print shapes and types of salt_data
    print("Shapes and types of salt_data:")
    for i, data in enumerate(salt_data):
        print(f"salt_data[{i}]: shape={data.shape}, type={type(data)}")

    # Calculate anomalies
    temp_anomalies = calculate_anomalies(temp_data, temp_clim)
    salt_anomalies = calculate_anomalies(salt_data, salt_clim)

    # Debugging: Print shapes and types of anomalies
    print("Shapes and types of temp_anomalies:")
    for key, value in temp_anomalies.items():
        print(f"{key}: shape={value.shape}, type={type(value)}")

    print("Shapes and types of salt_anomalies:")
    for key, value in salt_anomalies.items():
        print(f"{key}: shape={value.shape}, type={type(value)}")

    # Create grids
    temp_Xgrid, temp_Ygrid = create_grid(-126.625, -124.375, 36, 0, 1000, 200)
    salt_Xgrid, salt_Ygrid = create_grid(-126.5, -124.5, 48, 0, 1000, 200)

    # Debugging: Print shapes of grids
    print(f"temp_Xgrid shape: {temp_Xgrid.shape}, temp_Ygrid shape: {temp_Ygrid.shape}")
    print(f"salt_Xgrid shape: {salt_Xgrid.shape}, salt_Ygrid shape: {salt_Ygrid.shape}")

    # Interpolate and grid data
    combined_temp = interpolate_grid(list(temp_anomalies.values()), temp_Xgrid, temp_Ygrid)
    combined_salt = interpolate_grid(list(salt_anomalies.values()), salt_Xgrid, salt_Ygrid)

    # Debugging: Print shapes of combined data
    print(f"combined_temp shape: {combined_temp.shape}")
    print(f"combined_salt shape: {combined_salt.shape}")

    # Plot data
    plot_data(temp_Xgrid, temp_Ygrid, combined_temp, 'Temperature Anomaly', 'Depth (m)', r'($\degree$C)', 'RdYlBu_r', colors.TwoSlopeNorm(vcenter=0., vmin=-4, vmax=4), [-4, -3.5, -3, -2.5, -2, -1.5, -1, -0.5, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4], "C:/Users/marqjace/seaglider_python/Figures/current_t_anom_timeseries_new.png")
    plot_data(salt_Xgrid, salt_Ygrid, combined_salt, 'Salinity Anomaly', 'Depth (m)', '(PSU)', 'BrBG_r', colors.TwoSlopeNorm(vcenter=0., vmin=-.75, vmax=.75), [-.6, -.4, -.2, .2, .4, .6], "C:/Users/marqjace/seaglider_python/Figures/current_t_anom_timeseries_new.png")
