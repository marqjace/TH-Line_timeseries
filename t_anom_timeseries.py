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


# Open WOA Climatology Data
# Data Access Here: https://www.ncei.noaa.gov/access/world-ocean-atlas-2018/bin/woa18.pl

print('\nImporting WOA climatology data...')

# Temperature
ds_z_t_an1 = woa_temp.woa_temp_jan
ds_z_t_an2 = woa_temp.woa_temp_feb
ds_z_t_an3 = woa_temp.woa_temp_mar
ds_z_t_an4 = woa_temp.woa_temp_apr
ds_z_t_an5 = woa_temp.woa_temp_may
ds_z_t_an6 = woa_temp.woa_temp_jun
ds_z_t_an7 = woa_temp.woa_temp_jul
ds_z_t_an8 = woa_temp.woa_temp_aug
ds_z_t_an9 = woa_temp.woa_temp_sep
ds_z_t_an10 = woa_temp.woa_temp_oct
ds_z_t_an11 = woa_temp.woa_temp_nov
ds_z_t_an12 = woa_temp.woa_temp_dec

# Salinity
ds_z_s_an1 = woa_salt.woa_salt_jan
ds_z_s_an2 = woa_salt.woa_salt_feb
ds_z_s_an3 = woa_salt.woa_salt_mar
ds_z_s_an4 = woa_salt.woa_salt_apr
ds_z_s_an5 = woa_salt.woa_salt_may
ds_z_s_an6 = woa_salt.woa_salt_jun
ds_z_s_an7 = woa_salt.woa_salt_jul
ds_z_s_an8 = woa_salt.woa_salt_aug
ds_z_s_an9 = woa_salt.woa_salt_sep
ds_z_s_an10 = woa_salt.woa_salt_oct
ds_z_s_an11 = woa_salt.woa_salt_nov
ds_z_s_an12 = woa_salt.woa_salt_dec


# SCTI / ONI Data
# Data Access Here: https://spraydata.ucsd.edu/products/socal-index/

print('\nImporting SCTI, ONI, and MOCI data...')

dat = xr.open_dataset(r'C:/Users/marqjace/TH_line/scti_oni/socal_index_monthly_v1_8571_f367_229e_U1743622012494.nc', decode_times=False)

# Assign Variables
scti = dat['scti']
oni = dat['oni']
scti_time = dat['time']

# Convert time to ordinal time
time2 = []

for value in scti_time:
    new = datetime.fromtimestamp(int(value)).toordinal()
    time2.append(new)

time2 = xr.DataArray(time2)
scti_time = time2


# California MOCI
# García-Reyes, M. and Sydeman, W.J. (2017). California Multivariate Ocean Climate Indicator (MOCI) [Data set, V2]. Farallon Institute website, http://www.faralloninstitute.org/moci. Accessed [2 April 2025].
dat2 = pd.read_csv(r'C:/Users/marqjace/TH_line/california_moci/CaliforniaMOCI.csv')
dat2 = dat2.drop(['Year', 'Season', 'Central California (34.5-38N)', 'Southern California (32-34.5N)'], axis=1)
dat2 = dat2.set_index(['time'])

# Norcal Only
norcal_moci = dat2['North California (38-42N)']
norcal_time = norcal_moci.index

norcal_time2 = []

for value in norcal_time:
    value = pd.to_datetime(value)
    new = value.toordinal()
    norcal_time2.append(new)

norcal_moci = xr.DataArray(norcal_moci)
norcal_time = xr.DataArray(norcal_time2)


# Glider Transect Data

# Temp & Salt Grid
# Set up new grid (36 points is 2.25 deg longitude for every 5 km, 200 points depth to 1000m is every 5 meters)

# number of grid points:
xn, yn = 36, 200

# grid window
xmin, xmax = -126.625, -124.375
ymin, ymax = 0, 1000

# Generate a regular grid to interpolate the data
xgrid = np.linspace(xmin, xmax, xn)
ygrid = np.linspace(ymin, ymax, yn)
Xgrid, Ygrid = np.meshgrid(xgrid, ygrid)

# Oxygen Grid

# Set up new grid (36 points is 2.25 deg longitude for every 5 km, 200 points depth to 1000m is every 5 meters)
# number of grid points:
xn2, yn2 = 48, 200

# grid window
xmin2, xmax2 = -126.5, -124.5
ymin2, ymax2 = 0, 1000

# Generate a regular grid to interpolate the data
xgrid2 = np.linspace(xmin2, xmax2, xn2)
ygrid2 = np.linspace(ymin2, ymax2, yn2)
Xgrid2, Ygrid2 = np.meshgrid(xgrid2, ygrid2)

# Interpolated & Gridded Temperature
print('\nImporting TH line transect data...')
temp_12_14_a = transects_func.temp_12_14_a
temp_12_14_b = transects_func.temp_12_14_b
temp_1_15 = transects_func.temp_1_15
temp_2_15_a = transects_func.temp_2_15_a
temp_2_15_b = transects_func.temp_2_15_b
temp_3_15 = transects_func.temp_3_15
temp_4_15 = transects_func.temp_4_15
temp_5_15 = transects_func.temp_5_15
temp_6_15 = transects_func.temp_6_15
temp_7_15 = transects_func.temp_7_15
temp_8_15 = transects_func.temp_8_15
temp_9_15 = transects_func.temp_9_15
temp_10_15 = transects_func.temp_10_15
temp_11_15 = transects_func.temp_11_15
temp_12_15 = transects_func.temp_12_15
temp_1_16 = transects_func.temp_1_16
temp_3_16 = transects_func.temp_3_16
temp_4_16 = transects_func.temp_4_16
temp_5_16 = transects_func.temp_5_16
temp_6_16 = transects_func.temp_6_16
temp_7_16 = transects_func.temp_7_16
temp_8_16 = transects_func.temp_8_16
temp_9_16_a = transects_func.temp_9_16_a
temp_9_16_b = transects_func.temp_9_16_b
temp_10_16_a = transects_func.temp_10_16_a
temp_10_16_b = transects_func.temp_10_16_b
temp_11_16 = transects_func.temp_11_16
temp_12_16 = transects_func.temp_12_16
temp_1_17 = transects_func.temp_1_17
temp_2_17 = transects_func.temp_2_17
temp_3_17 = transects_func.temp_3_17
temp_4_17_a = transects_func.temp_4_17_a
temp_4_17_b = transects_func.temp_4_17_b
temp_5_17 = transects_func.temp_5_17
temp_6_17 = transects_func.temp_6_17
temp_7_17 = transects_func.temp_7_17
temp_8_17 = transects_func.temp_8_17
temp_9_17 = transects_func.temp_9_17
temp_10_17_a = transects_func.temp_10_17_a
temp_10_17_b = transects_func.temp_10_17_b
temp_11_17 = transects_func.temp_11_17
temp_4_18 = transects_func.temp_4_18
temp_5_18 = transects_func.temp_5_18
temp_6_18 = transects_func.temp_6_18
temp_8_18 = transects_func.temp_8_18
temp_9_18_a = transects_func.temp_9_18_a
temp_9_18_b = transects_func.temp_9_18_b
temp_11_18 = transects_func.temp_11_18
temp_12_18 = transects_func.temp_12_18
temp_1_19 = transects_func.temp_1_19
temp_2_19 = transects_func.temp_2_19
temp_3_19_a = transects_func.temp_3_19_a
temp_3_19_b = transects_func.temp_3_19_b
temp_4_19_a = transects_func.temp_4_19_a
temp_4_19_b = transects_func.temp_4_19_b
temp_6_19 = transects_func.temp_6_19
temp_7_19 = transects_func.temp_7_19
temp_8_19 = transects_func.temp_8_19
temp_9_19 = transects_func.temp_9_19
temp_10_19 = transects_func.temp_10_19
temp_11_19 = transects_func.temp_11_19
temp_12_19 = transects_func.temp_12_19
temp_1_20 = transects_func.temp_1_20
temp_2_20 = transects_func.temp_2_20
temp_3_20_a = transects_func.temp_3_20_a
temp_3_20_b = transects_func.temp_3_20_b
temp_9_20 = transects_func.temp_9_20
temp_10_20 = transects_func.temp_10_20
temp_11_20 = transects_func.temp_11_20
temp_12_20 = transects_func.temp_12_20
temp_1_21 = transects_func.temp_1_21
temp_2_21 = transects_func.temp_2_21
temp_11_21 = transects_func.temp_11_21
temp_12_21 = transects_func.temp_12_21
temp_1_22 = transects_func.temp_1_22
temp_2_22 = transects_func.temp_2_22
temp_3_22 = transects_func.temp_3_22
temp_4_22 = transects_func.temp_4_22
temp_5_22 = transects_func.temp_5_22
temp_6_22 = transects_func.temp_6_22
temp_8_22 = transects_func.temp_8_22
temp_9_22 = transects_func.temp_9_22
temp_10_22 = transects_func.temp_10_22
temp_11_22 = transects_func.temp_11_22
temp_12_22 = transects_func.temp_12_22
temp_1_23 = transects_func.temp_1_23
temp_2_23 = transects_func.temp_2_23
temp_3_23_a = transects_func.temp_3_23_a
temp_3_23_b = transects_func.temp_3_23_b
temp_4_23 = transects_func.temp_4_23
temp_5_23 = transects_func.temp_5_23
temp_6_23 = transects_func.temp_6_23
temp_7_23 = transects_func.temp_7_23
temp_8_23 = transects_func.temp_8_23
temp_10_23 = transects_func.temp_10_23
temp_11_23 = transects_func.temp_11_23
temp_12_23 = transects_func.temp_12_23
temp_1_24= transects_func.temp_1_24
temp_2_24_a= transects_func.temp_2_24_a
temp_2_24_b= transects_func.temp_2_24_b
temp_3_24= transects_func.temp_3_24
temp_4_24= transects_func.temp_4_24
temp_5_24= transects_func.temp_5_24
temp_6_24= transects_func.temp_6_24
temp_7_24= transects_func.temp_7_24
temp_8_24_a= transects_func.temp_8_24_a
temp_8_24_b= transects_func.temp_8_24_b
temp_10_24= transects_func.temp_10_24
temp_11_24= transects_func.temp_11_24
temp_3_25= transects_func.temp_3_25

# Interpolated & Gridded Salinity
salt_12_14_a = transects_func.salt_12_14_a
salt_12_14_b = transects_func.salt_12_14_b
salt_1_15 = transects_func.salt_1_15
salt_2_15_a = transects_func.salt_2_15_a
salt_2_15_b = transects_func.salt_2_15_b
salt_3_15 = transects_func.salt_3_15
salt_4_15 = transects_func.salt_4_15
salt_5_15 = transects_func.salt_5_15
salt_6_15 = transects_func.salt_6_15
salt_7_15 = transects_func.salt_7_15
salt_8_15 = transects_func.salt_8_15
salt_9_15 = transects_func.salt_9_15
salt_10_15 = transects_func.salt_10_15
salt_11_15 = transects_func.salt_11_15
salt_12_15 = transects_func.salt_12_15
salt_1_16 = transects_func.salt_1_16
salt_3_16 = transects_func.salt_3_16
salt_4_16 = transects_func.salt_4_16
salt_5_16 = transects_func.salt_5_16
salt_6_16 = transects_func.salt_6_16
salt_7_16 = transects_func.salt_7_16
salt_8_16 = transects_func.salt_8_16
salt_9_16_a = transects_func.salt_9_16_a
salt_9_16_b = transects_func.salt_9_16_b
salt_10_16_a = transects_func.salt_10_16_a
salt_10_16_b = transects_func.salt_10_16_b
salt_11_16 = transects_func.salt_11_16
salt_12_16 = transects_func.salt_12_16
salt_1_17 = transects_func.salt_1_17
salt_2_17 = transects_func.salt_2_17
salt_3_17 = transects_func.salt_3_17
salt_4_17_a = transects_func.salt_4_17_a
salt_4_17_b = transects_func.salt_4_17_b
salt_5_17 = transects_func.salt_5_17
salt_6_17 = transects_func.salt_6_17
salt_7_17 = transects_func.salt_7_17
salt_8_17 = transects_func.salt_8_17
salt_9_17 = transects_func.salt_9_17
salt_10_17_a = transects_func.salt_10_17_a
salt_10_17_b = transects_func.salt_10_17_b
salt_11_17 = transects_func.salt_11_17
salt_4_18 = transects_func.salt_4_18
salt_5_18 = transects_func.salt_5_18
salt_6_18 = transects_func.salt_6_18
salt_8_18 = transects_func.salt_8_18
salt_9_18_a = transects_func.salt_9_18_a
salt_9_18_b = transects_func.salt_9_18_b
salt_11_18 = transects_func.salt_11_18
salt_12_18 = transects_func.salt_12_18
salt_1_19 = transects_func.salt_1_19
salt_2_19 = transects_func.salt_2_19
salt_3_19_a = transects_func.salt_3_19_a
salt_3_19_b = transects_func.salt_3_19_b
salt_4_19_a = transects_func.salt_4_19_a
salt_4_19_b = transects_func.salt_4_19_b
salt_6_19 = transects_func.salt_6_19
salt_7_19 = transects_func.salt_7_19
salt_8_19 = transects_func.salt_8_19
salt_9_19 = transects_func.salt_9_19
salt_10_19 = transects_func.salt_10_19
salt_11_19 = transects_func.salt_11_19
salt_12_19 = transects_func.salt_12_19
salt_1_20 = transects_func.salt_1_20
salt_2_20 = transects_func.salt_2_20
salt_3_20_a = transects_func.salt_3_20_a
salt_3_20_b = transects_func.salt_3_20_b
salt_9_20 = transects_func.salt_9_20
salt_10_20 = transects_func.salt_10_20
salt_11_20 = transects_func.salt_11_20
salt_12_20 = transects_func.salt_12_20
salt_1_21 = transects_func.salt_1_21
salt_2_21 = transects_func.salt_2_21
salt_11_21 = transects_func.salt_11_21
salt_12_21 = transects_func.salt_12_21
salt_1_22 = transects_func.salt_1_22
salt_2_22 = transects_func.salt_2_22
salt_3_22 = transects_func.salt_3_22
salt_4_22 = transects_func.salt_4_22
salt_5_22 = transects_func.salt_5_22
salt_6_22 = transects_func.salt_6_22
salt_8_22 = transects_func.salt_8_22
salt_9_22 = transects_func.salt_9_22
salt_10_22 = transects_func.salt_10_22
salt_11_22 = transects_func.salt_11_22
salt_12_22 = transects_func.salt_12_22
salt_1_23 = transects_func.salt_1_23
salt_2_23 = transects_func.salt_2_23
salt_3_23_a = transects_func.salt_3_23_a
salt_3_23_b = transects_func.salt_3_23_b
salt_4_23 = transects_func.salt_4_23
salt_5_23 = transects_func.salt_5_23
salt_6_23 = transects_func.salt_6_23
salt_7_23 = transects_func.salt_7_23
salt_8_23 = transects_func.salt_8_23
salt_10_23 = transects_func.salt_10_23
salt_11_23 = transects_func.salt_11_23
salt_12_23 = transects_func.salt_12_23
salt_1_24= transects_func.salt_1_24
salt_2_24_a= transects_func.salt_2_24_a
salt_2_24_b= transects_func.salt_2_24_b
salt_3_24= transects_func.salt_3_24
salt_4_24= transects_func.salt_4_24
salt_5_24= transects_func.salt_5_24
salt_6_24= transects_func.salt_6_24
salt_7_24= transects_func.salt_7_24
salt_8_24_a= transects_func.salt_8_24_a
salt_8_24_b= transects_func.salt_8_24_b
salt_10_24= transects_func.salt_10_24
salt_11_24= transects_func.salt_11_24
salt_3_25= transects_func.salt_3_25

# Time
time_12_14_a = transects_func.time_12_14_a
time_12_14_b = transects_func.time_12_14_b
time_1_15 = transects_func.time_1_15
time_2_15_a = transects_func.time_2_15_a
time_2_15_b = transects_func.time_2_15_b
time_3_15 = transects_func.time_3_15
time_4_15 = transects_func.time_4_15
time_5_15 = transects_func.time_5_15
time_6_15 = transects_func.time_6_15
time_7_15 = transects_func.time_7_15
time_8_15 = transects_func.time_8_15
time_9_15 = transects_func.time_9_15
time_10_15 = transects_func.time_10_15
time_11_15 = transects_func.time_11_15
time_12_15 = transects_func.time_12_15
time_1_16 = transects_func.time_1_16
time_3_16 = transects_func.time_3_16
time_4_16 = transects_func.time_4_16
time_5_16 = transects_func.time_5_16
time_6_16 = transects_func.time_6_16
time_7_16 = transects_func.time_7_16
time_8_16 = transects_func.time_8_16
time_9_16_a = transects_func.time_9_16_a
time_9_16_b = transects_func.time_9_16_b
time_10_16_a = transects_func.time_10_16_a
time_10_16_b = transects_func.time_10_16_b
time_11_16 = transects_func.time_11_16
time_12_16 = transects_func.time_12_16
time_1_17 = transects_func.time_1_17
time_2_17 = transects_func.time_2_17
time_3_17 = transects_func.time_3_17
time_4_17_a = transects_func.time_4_17_a
time_4_17_b = transects_func.time_4_17_b
time_5_17 = transects_func.time_5_17
time_6_17 = transects_func.time_6_17
time_7_17 = transects_func.time_7_17
time_8_17 = transects_func.time_8_17
time_9_17 = transects_func.time_9_17
time_10_17_a = transects_func.time_10_17_a
time_10_17_b = transects_func.time_10_17_b
time_11_17 = transects_func.time_11_17
time_4_18 = transects_func.time_4_18
time_5_18 = transects_func.time_5_18
time_6_18 = transects_func.time_6_18
time_8_18 = transects_func.time_8_18
time_9_18_a = transects_func.time_9_18_a
time_9_18_b = transects_func.time_9_18_b
time_11_18 = transects_func.time_11_18
time_12_18 = transects_func.time_12_18
time_1_19 = transects_func.time_1_19
time_2_19 = transects_func.time_2_19
time_3_19_a = transects_func.time_3_19_a
time_3_19_b = transects_func.time_3_19_b
time_4_19_a = transects_func.time_4_19_a
time_4_19_b = transects_func.time_4_19_b
time_6_19 = transects_func.time_6_19
time_7_19 = transects_func.time_7_19
time_8_19 = transects_func.time_8_19
time_9_19 = transects_func.time_9_19
time_10_19 = transects_func.time_10_19
time_11_19 = transects_func.time_11_19
time_12_19 = transects_func.time_12_19
time_1_20 = transects_func.time_1_20
time_2_20 = transects_func.time_2_20
time_3_20_a = transects_func.time_3_20_a
time_3_20_b = transects_func.time_3_20_b
time_9_20 = transects_func.time_9_20
time_10_20 = transects_func.time_10_20
time_11_20 = transects_func.time_11_20
time_12_20 = transects_func.time_12_20
time_1_21 = transects_func.time_1_21
time_2_21 = transects_func.time_2_21
time_11_21 = transects_func.time_11_21
time_12_21 = transects_func.time_12_21
time_1_22 = transects_func.time_1_22
time_2_22 = transects_func.time_2_22
time_3_22 = transects_func.time_3_22
time_4_22 = transects_func.time_4_22
time_5_22 = transects_func.time_5_22
time_6_22 = transects_func.time_6_22
time_8_22 = transects_func.time_8_22
time_9_22 = transects_func.time_9_22
time_10_22 = transects_func.time_10_22
time_11_22 = transects_func.time_11_22
time_12_22 = transects_func.time_12_22
time_1_23 = transects_func.time_1_23
time_2_23 = transects_func.time_2_23
time_3_23_a = transects_func.time_3_23_a
time_3_23_b = transects_func.time_3_23_b
time_4_23 = transects_func.time_4_23
time_5_23 = transects_func.time_5_23
time_6_23 = transects_func.time_6_23
time_7_23 = transects_func.time_7_23
time_8_23 = transects_func.time_8_23
time_10_23 = transects_func.time_10_23
time_11_23 = transects_func.time_11_23
time_12_23 = transects_func.time_12_23
time_1_24= transects_func.time_1_24
time_2_24_a= transects_func.time_2_24_a
time_2_24_b= transects_func.time_2_24_b
time_3_24= transects_func.time_3_24
time_4_24= transects_func.time_4_24
time_5_24= transects_func.time_5_24
time_6_24= transects_func.time_6_24
time_7_24= transects_func.time_7_24
time_8_24_a= transects_func.time_8_24_a
time_8_24_b= transects_func.time_8_24_b
time_10_24=transects_func.time_10_24
time_11_24=transects_func.time_11_24
time_3_25=transects_func.time_3_25

# Longitude
lon_12_14_a = transects_func.lon_12_14_a
lon_12_14_b = transects_func.lon_12_14_b
lon_1_15 = transects_func.lon_1_15
lon_2_15_a = transects_func.lon_2_15_a
lon_2_15_b = transects_func.lon_2_15_b
lon_3_15 = transects_func.lon_3_15
lon_4_15 = transects_func.lon_4_15
lon_5_15 = transects_func.lon_5_15
lon_6_15 = transects_func.lon_6_15
lon_7_15 = transects_func.lon_7_15
lon_8_15 = transects_func.lon_8_15
lon_9_15 = transects_func.lon_9_15
lon_10_15 = transects_func.lon_10_15
lon_11_15 = transects_func.lon_11_15
lon_12_15 = transects_func.lon_12_15
lon_1_16 = transects_func.lon_1_16
lon_3_16 = transects_func.lon_3_16
lon_4_16 = transects_func.lon_4_16
lon_5_16 = transects_func.lon_5_16
lon_6_16 = transects_func.lon_6_16
lon_7_16 = transects_func.lon_7_16
lon_8_16 = transects_func.lon_8_16
lon_9_16_a = transects_func.lon_9_16_a
lon_9_16_b = transects_func.lon_9_16_b
lon_10_16_a = transects_func.lon_10_16_a
lon_10_16_b = transects_func.lon_10_16_b
lon_11_16 = transects_func.lon_11_16
lon_12_16 = transects_func.lon_12_16
lon_1_17 = transects_func.lon_1_17
lon_2_17 = transects_func.lon_2_17
lon_3_17 = transects_func.lon_3_17
lon_4_17_a = transects_func.lon_4_17_a
lon_4_17_b = transects_func.lon_4_17_b
lon_5_17 = transects_func.lon_5_17
lon_6_17 = transects_func.lon_6_17
lon_7_17 = transects_func.lon_7_17
lon_8_17 = transects_func.lon_8_17
lon_9_17 = transects_func.lon_9_17
lon_10_17_a = transects_func.lon_10_17_a
lon_10_17_b = transects_func.lon_10_17_b
lon_11_17 = transects_func.lon_11_17
lon_4_18 = transects_func.lon_4_18
lon_5_18 = transects_func.lon_5_18
lon_6_18 = transects_func.lon_6_18
lon_8_18 = transects_func.lon_8_18
lon_9_18_a = transects_func.lon_9_18_a
lon_9_18_b = transects_func.lon_9_18_b
lon_11_18 = transects_func.lon_11_18
lon_12_18 = transects_func.lon_12_18
lon_1_19 = transects_func.lon_1_19
lon_2_19 = transects_func.lon_2_19
lon_3_19_a = transects_func.lon_3_19_a
lon_3_19_b = transects_func.lon_3_19_b
lon_4_19_a = transects_func.lon_4_19_a
lon_4_19_b = transects_func.lon_4_19_b
lon_6_19 = transects_func.lon_6_19
lon_7_19 = transects_func.lon_7_19
lon_8_19 = transects_func.lon_8_19
lon_9_19 = transects_func.lon_9_19
lon_10_19 = transects_func.lon_10_19
lon_11_19 = transects_func.lon_11_19
lon_12_19 = transects_func.lon_12_19
lon_1_20 = transects_func.lon_1_20
lon_2_20 = transects_func.lon_2_20
lon_3_20_a = transects_func.lon_3_20_a
lon_3_20_b = transects_func.lon_3_20_b
lon_9_20 = transects_func.lon_9_20
lon_10_20 = transects_func.lon_10_20
lon_11_20 = transects_func.lon_11_20
lon_12_20 = transects_func.lon_12_20
lon_1_21 = transects_func.lon_1_21
lon_2_21 = transects_func.lon_2_21
lon_11_21 = transects_func.lon_11_21
lon_12_21 = transects_func.lon_12_21
lon_1_22 = transects_func.lon_1_22
lon_2_22 = transects_func.lon_2_22
lon_3_22 = transects_func.lon_3_22
lon_4_22 = transects_func.lon_4_22
lon_5_22 = transects_func.lon_5_22
lon_6_22 = transects_func.lon_6_22
lon_8_22 = transects_func.lon_8_22
lon_9_22 = transects_func.lon_9_22
lon_10_22 = transects_func.lon_10_22
lon_11_22 = transects_func.lon_11_22
lon_12_22 = transects_func.lon_12_22
lon_1_23 = transects_func.lon_1_23
lon_2_23 = transects_func.lon_2_23
lon_3_23_a = transects_func.lon_3_23_a
lon_3_23_b = transects_func.lon_3_23_b
lon_4_23 = transects_func.lon_4_23
lon_5_23 = transects_func.lon_5_23
lon_6_23 = transects_func.lon_6_23
lon_7_23 = transects_func.lon_7_23
lon_8_23 = transects_func.lon_8_23
lon_10_23 = transects_func.lon_10_23
lon_11_23 = transects_func.lon_11_23
lon_12_23 = transects_func.lon_12_23
lon_1_24= transects_func.lon_1_24
lon_2_24_a= transects_func.lon_2_24_a
lon_2_24_b= transects_func.lon_2_24_b
lon_3_24= transects_func.lon_3_24
lon_4_24= transects_func.lon_4_24
lon_5_24= transects_func.lon_5_24
lon_6_24= transects_func.lon_6_24
lon_7_24= transects_func.lon_7_24
lon_8_24_a= transects_func.lon_8_24_a
lon_8_24_b= transects_func.lon_8_24_b
lon_10_24= transects_func.lon_10_24
lon_11_24= transects_func.lon_11_24
lon_3_25 = transects_func.lon_3_25


# Anomaly Calculations

# Temperature Anomaly
# Create Temperature Anomaly Array For Each Transect Line

print('\nCalculating temperature anomalies...')

# Nov 2014 Deployment
t_anom_12_14_a = np.subtract(temp_12_14_a, ds_z_t_an12) # Transect 1 Dec 2014
t_anom_12_14_b = np.subtract(temp_12_14_b, ds_z_t_an12) # Transect 2 Dec 2014
t_anom_1_15 = np.subtract(temp_1_15, ds_z_t_an1) # Transect 3 Jan 2015
t_anom_2_15_a = np.subtract(temp_2_15_a, ds_z_t_an2) # Transect 4 Feb 2015
t_anom_2_15_b = np.subtract(temp_2_15_b, ds_z_t_an2) # Transect 5 Feb 2015

# Mar 2015 Deployment
t_anom_3_15 = np.subtract(temp_3_15, ds_z_t_an3) # Transect 1 Mar 2015
t_anom_4_15 = np.subtract(temp_4_15, ds_z_t_an4) # Transect 2 Apr 2015
t_anom_5_15 = np.subtract(temp_5_15, ds_z_t_an5) # Transect 3 May 2015
t_anom_6_15 = np.subtract(temp_6_15, ds_z_t_an6) # Transect 4 Jun 2015
t_anom_7_15 = np.subtract(temp_7_15, ds_z_t_an7) # Transect 5 Jul 2015
t_anom_8_15 = np.subtract(temp_8_15, ds_z_t_an8) # Transect 6 Aug 2015
t_anom_9_15 = np.subtract(temp_9_15, ds_z_t_an9) # Transect 7 Sep 2015

# Sep 2015 Deployment
t_anom_10_15 = np.subtract(temp_10_15, ds_z_t_an10) # Transect 1 Oct 2015
t_anom_11_15 = np.subtract(temp_11_15, ds_z_t_an11) # Transect 2 Nov 2015
t_anom_12_15 = np.subtract(temp_12_15, ds_z_t_an12) # Transect 3 Dec 2015
t_anom_1_16 = np.subtract(temp_1_16, ds_z_t_an1) # Transect 4 Jan 2016
t_anom_3_16 = np.subtract(temp_3_16, ds_z_t_an3) # Transect 5 Mar 2016
t_anom_4_16 = np.subtract(temp_4_16, ds_z_t_an4) # Transect 6 Apr 2016
t_anom_5_16 = np.subtract(temp_5_16, ds_z_t_an5) # Transect 7 May 2016

# May 2016 Deployment
t_anom_6_16 = np.subtract(temp_6_16, ds_z_t_an6) # Transect 1 Jun 2016
t_anom_7_16 = np.subtract(temp_7_16, ds_z_t_an7) # Transect 2 Jul 2016
t_anom_8_16 = np.subtract(temp_8_16, ds_z_t_an8) # Transect 3 Aug 2016
t_anom_9_16_a = np.subtract(temp_9_16_a, ds_z_t_an9) # Transect 4 Sep 2016
t_anom_9_16_b = np.subtract(temp_9_16_b, ds_z_t_an9) # Transect 5 Sep 2016
t_anom_10_16_a = np.subtract(temp_10_16_a, ds_z_t_an10) # Transect 6 Oct 2016
t_anom_10_16_b = np.subtract(temp_10_16_b, ds_z_t_an10) # Transect 7 Oct 2016

# Oct 2016 Deployment
t_anom_11_16 = np.subtract(temp_11_16, ds_z_t_an11) # Transect 1 Nov 2016
t_anom_12_16 = np.subtract(temp_12_16, ds_z_t_an12) # Transect 2 Dec 2016
t_anom_1_17 = np.subtract(temp_1_17, ds_z_t_an1) # Transect 3 Jan 2017
t_anom_2_17 = np.subtract(temp_2_17, ds_z_t_an2) # Transect 4 Feb 2017
t_anom_3_17 = np.subtract(temp_3_17, ds_z_t_an3) # Transect 5 Mar 2017
t_anom_4_17_a = np.subtract(temp_4_17_a, ds_z_t_an4) # Transect 6 Apr 2017
t_anom_4_17_b = np.subtract(temp_4_17_b, ds_z_t_an4) # Transect 7 Apr 2017
t_anom_5_17 = np.subtract(temp_5_17, ds_z_t_an5) # Transect 8 May 2017

# Jun 2017 Deployment
t_anom_6_17 = np.subtract(temp_6_17, ds_z_t_an6) # Transect 1 Jun 2017
t_anom_7_17 = np.subtract(temp_7_17, ds_z_t_an7) # Transect 2 Jul 2017
t_anom_8_17 = np.subtract(temp_8_17, ds_z_t_an8) # Transect 3 Aug 2017
t_anom_9_17 = np.subtract(temp_9_17, ds_z_t_an9) # Transect 4 Sep 2017
t_anom_10_17_a = np.subtract(temp_10_17_a, ds_z_t_an10) # Transect 5 Oct 2017
t_anom_10_17_b = np.subtract(temp_10_17_b, ds_z_t_an10) # Transect 6 Oct 2017
t_anom_11_17 = np.subtract(temp_11_17, ds_z_t_an11) # Transect 7 Nov 2017

# Apr 2018 Deployment
t_anom_4_18 = np.subtract(temp_4_18, ds_z_t_an4) # Transect 1 Apr 2018
t_anom_5_18 = np.subtract(temp_5_18, ds_z_t_an5) # Transect 2 May 2018
t_anom_6_18 = np.subtract(temp_6_18, ds_z_t_an6) # Transect 3 Jun 2018
t_anom_8_18 = np.subtract(temp_8_18, ds_z_t_an8) # Transect 4 Aug 2018
t_anom_9_18_a = np.subtract(temp_9_18_a, ds_z_t_an9) # Transect 5 Sep 2018
t_anom_9_18_b = np.subtract(temp_9_18_b, ds_z_t_an9) # Transect 6 Sep 2018

# Nov 2018 Deployment
t_anom_11_18 = np.subtract(temp_11_18, ds_z_t_an11) # Transect 1 Nov 2018
t_anom_12_18 = np.subtract(temp_12_18, ds_z_t_an12) # Transect 2 Dec 2018
t_anom_1_19 = np.subtract(temp_1_19, ds_z_t_an1) # Transect 3 Jan 2019
t_anom_2_19 = np.subtract(temp_2_19, ds_z_t_an2) # Transect 4 Feb 2019
t_anom_3_19_a = np.subtract(temp_3_19_a, ds_z_t_an3) # Transect 5 Mar 2019
t_anom_3_19_b = np.subtract(temp_3_19_b, ds_z_t_an3) # Transect 6 Mar 2019
t_anom_4_19_a = np.subtract(temp_4_19_a, ds_z_t_an4) # Transect 7 Apr 2019

# Apr 2019 Deployment
t_anom_4_19_b = np.subtract(temp_4_19_b, ds_z_t_an4) # Transect 1 Apr 2019
t_anom_6_19 = np.subtract(temp_6_19, ds_z_t_an6) # Transect 2 Jun 2019
t_anom_7_19 = np.subtract(temp_7_19, ds_z_t_an7) # Transect 3 Jul 2019
t_anom_8_19 = np.subtract(temp_8_19, ds_z_t_an8) # Transect 4 Aug 2019

# Sep 2019 Deployment
t_anom_9_19 = np.subtract(temp_9_19, ds_z_t_an9) # Transect 1 Sep 2019
t_anom_10_19 = np.subtract(temp_10_19, ds_z_t_an10) # Transect 2 Oct 2019
t_anom_11_19 = np.subtract(temp_11_19, ds_z_t_an11) # Transect 3 Nov 2019
t_anom_12_19 = np.subtract(temp_12_19, ds_z_t_an12) # Transect 4 Dec 2019
t_anom_1_20 = np.subtract(temp_1_20, ds_z_t_an1) # Transect 5 Jan 2020
t_anom_2_20 = np.subtract(temp_2_20, ds_z_t_an2) # Transect 6 Feb 2020
t_anom_3_20_a = np.subtract(temp_3_20_a, ds_z_t_an3) # Transect 7 Mar 2020
t_anom_3_20_b = np.subtract(temp_3_20_b, ds_z_t_an3) # Transect 8 Mar 2020

# Sep 2020 Deployment
t_anom_9_20 = np.subtract(temp_9_20, ds_z_t_an9) # Transect 1 Sep 2020
t_anom_10_20 = np.subtract(temp_10_20, ds_z_t_an10) # Transect 2 Oct 2020
t_anom_11_20 = np.subtract(temp_11_20, ds_z_t_an11) # Transect 3 Nov 2020
t_anom_12_20 = np.subtract(temp_12_20, ds_z_t_an12) # Transect 4 Dec 2020
t_anom_1_21 = np.subtract(temp_1_21, ds_z_t_an1) # Transect 5 Jan 2021
t_anom_2_21 = np.subtract(temp_2_21, ds_z_t_an2) # Transect 6 Feb 2021

# Nov 2021 Deployment
t_anom_11_21 = np.subtract(temp_11_21, ds_z_t_an11) # Transect 1 Nov 2021
t_anom_12_21 = np.subtract(temp_12_21, ds_z_t_an12) # Transect 2 Dec 2021
t_anom_1_22 = np.subtract(temp_1_22, ds_z_t_an1) # Transect 3 Jan 2022
t_anom_2_22 = np.subtract(temp_2_22, ds_z_t_an2) # Transect 4 Feb 2022
t_anom_3_22 = np.subtract(temp_3_22, ds_z_t_an3) # Transect 5 Mar 2022
t_anom_4_22 = np.subtract(temp_4_22, ds_z_t_an4) # Transect 6 Apr 2022
t_anom_5_22 = np.subtract(temp_5_22, ds_z_t_an5) # Transect 7 May 2022
t_anom_6_22 = np.subtract(temp_6_22, ds_z_t_an6) # Transect 8 Jun 2022

# Jul 2022 Deployment
t_anom_8_22 = np.subtract(temp_8_22, ds_z_t_an8) # Transect 1 Aug 2022
t_anom_9_22 = np.subtract(temp_9_22, ds_z_t_an9) # Transect 2 Sep 2022
t_anom_10_22 = np.subtract(temp_10_22, ds_z_t_an10) # Transect 3 Oct 2022
t_anom_11_22 = np.subtract(temp_11_22, ds_z_t_an11) # Transect 4 Nov 2022
t_anom_12_22 = np.subtract(temp_12_22, ds_z_t_an12) # Transect 5 Dec 2022
t_anom_1_23 = np.subtract(temp_1_23, ds_z_t_an1) # Transect 6 Jan 2023

# Jan 2023 Deployment
t_anom_2_23 = np.subtract(temp_2_23, ds_z_t_an2) # Transect 1 Feb 2023
t_anom_3_23_a = np.subtract(temp_3_23_a, ds_z_t_an3) # Transect 2 Mar 2023
t_anom_3_23_b = np.subtract(temp_3_23_b, ds_z_t_an3) # Transect 3 Mar 2023
t_anom_4_23 = np.subtract(temp_4_23, ds_z_t_an4) # Transect 4 Apr 2023
t_anom_5_23 = np.subtract(temp_5_23, ds_z_t_an5) # Transect 5 May 2023
t_anom_6_23 = np.subtract(temp_6_23, ds_z_t_an6) # Transect 6 Jun 2023
t_anom_7_23 = np.subtract(temp_7_23, ds_z_t_an7) # Transect 7 Jul 2023
t_anom_8_23 = np.subtract(temp_8_23, ds_z_t_an8) # Transect 8 Aug 2023

# Oct 2023 Deployment
t_anom_10_23 = np.subtract(temp_10_23, ds_z_t_an10) # Transect 1 Oct 2023
t_anom_11_23 = np.subtract(temp_11_23, ds_z_t_an11) # Transect 2 Nov 2023
t_anom_12_23 = np.subtract(temp_12_23, ds_z_t_an12) # Transect 3 Dec 2023
t_anom_1_24 = np.subtract(temp_1_24, ds_z_t_an1) # Transect 4 Jan 2024
t_anom_2_24_a = np.subtract(temp_2_24_a, ds_z_t_an2) # Transect 5 Feb 2024
t_anom_2_24_b = np.subtract(temp_2_24_b, ds_z_t_an2) # Transect 6 Feb 2024
t_anom_3_24 = np.subtract(temp_3_24, ds_z_t_an3) # Transect 7 Mar 2024

# Apr 2024 Deployment
t_anom_4_24 = np.subtract(temp_4_24, ds_z_t_an4) # Transect 1 Apr 2024
t_anom_5_24 = np.subtract(temp_5_24, ds_z_t_an5) # Transect 2 May 2024
t_anom_6_24 = np.subtract(temp_6_24, ds_z_t_an6) # Transect 3 June 2024
t_anom_7_24 = np.subtract(temp_7_24, ds_z_t_an7) # Transect 4 July 2024
t_anom_8_24_a = np.subtract(temp_8_24_a, ds_z_t_an8) # Transect 5 Aug 2024
t_anom_8_24_b = np.subtract(temp_8_24_b, ds_z_t_an8) # Transect 6 Aug 2024

# Oct 2024 Deployment
t_anom_10_24 = np.subtract(temp_10_24, ds_z_t_an10) # Transect 1 Oct 2024
t_anom_11_24 = np.subtract(temp_11_24, ds_z_t_an11) # Transect 2 Nov 2024

# Mar 2025 Deployment
t_anom_3_25 = np.subtract(temp_3_25, ds_z_t_an3) # Transect 1 Mar 2025


# Salinity Anomaly
# Create Salinity Anomaly Array For Each Transect Line

print('\nCalculating salinity anomalies...')

# Nov 2014 Deployment
s_anom_12_14_a = np.subtract(salt_12_14_a, ds_z_s_an12) # Transect 1 Dec 2014
s_anom_12_14_b = np.subtract(salt_12_14_b, ds_z_s_an12) # Transect 2 Dec 2014
s_anom_1_15 = np.subtract(salt_1_15, ds_z_s_an1) # Transect 3 Jan 2015
s_anom_2_15_a = np.subtract(salt_2_15_a, ds_z_s_an2) # Transect 4 Feb 2015
s_anom_2_15_b = np.subtract(salt_2_15_b, ds_z_s_an2) # Transect 5 Feb 2015

# Mar 2015 Deployment
s_anom_3_15 = np.subtract(salt_3_15, ds_z_s_an3) # Transect 1 Mar 2015
s_anom_4_15 = np.subtract(salt_4_15, ds_z_s_an4) # Transect 2 Apr 2015
s_anom_5_15 = np.subtract(salt_5_15, ds_z_s_an5) # Transect 3 May 2015
s_anom_6_15 = np.subtract(salt_6_15, ds_z_s_an6) # Transect 4 Jun 2015
s_anom_7_15 = np.subtract(salt_7_15, ds_z_s_an7) # Transect 5 Jul 2015
s_anom_8_15 = np.subtract(salt_8_15, ds_z_s_an8) # Transect 6 Aug 2015
s_anom_9_15 = np.subtract(salt_9_15, ds_z_s_an9) # Transect 7 Sep 2015

# Sep 2015 Deployment
s_anom_10_15 = np.subtract(salt_10_15, ds_z_s_an10) # Transect 1 Oct 2015
s_anom_11_15 = np.subtract(salt_11_15, ds_z_s_an11) # Transect 1 Nov 2015
s_anom_12_15 = np.subtract(salt_12_15, ds_z_s_an12) # Transect 1 Dec 2015
s_anom_1_16 = np.subtract(salt_1_16, ds_z_s_an1) # Transect 1 Jan 2016
s_anom_3_16 = np.subtract(salt_3_16, ds_z_s_an3) # Transect 1 Mar 2016
s_anom_4_16 = np.subtract(salt_4_16, ds_z_s_an4) # Transect 1 Apr 2016
s_anom_5_16 = np.subtract(salt_5_16, ds_z_s_an5) # Transect 1 May 2016

# May 2016 Deployment
s_anom_6_16 = np.subtract(salt_6_16, ds_z_s_an6) # Transect 1 Jun 2016
s_anom_7_16 = np.subtract(salt_7_16, ds_z_s_an7) # Transect 2 Jul 2016
s_anom_8_16 = np.subtract(salt_8_16, ds_z_s_an8) # Transect 3 Aug 2016
s_anom_9_16_a = np.subtract(salt_9_16_a, ds_z_s_an9) # Transect 4 Sep 2016
s_anom_9_16_b = np.subtract(salt_9_16_b, ds_z_s_an9) # Transect 5 Sep 2016
s_anom_10_16_a = np.subtract(salt_10_16_a, ds_z_s_an10) # Transect 6 Oct 2016
s_anom_10_16_b = np.subtract(salt_10_16_b, ds_z_s_an10) # Transect 7 Oct 2016

# Oct 2016 Deployment
s_anom_11_16 = np.subtract(salt_11_16, ds_z_s_an11) # Transect 1 Nov 2016
s_anom_12_16 = np.subtract(salt_12_16, ds_z_s_an12) # Transect 2 Dec 2016
s_anom_1_17 = np.subtract(salt_1_17, ds_z_s_an1) # Transect 3 Jan 2017
s_anom_2_17 = np.subtract(salt_2_17, ds_z_s_an2) # Transect 4 Feb 2017
s_anom_3_17 = np.subtract(salt_3_17, ds_z_s_an3) # Transect 5 Mar 2017
s_anom_4_17_a = np.subtract(salt_4_17_a, ds_z_s_an4) # Transect 6 Apr 2017
s_anom_4_17_b = np.subtract(salt_4_17_b, ds_z_s_an4) # Transect 7 Apr 2017
s_anom_5_17 = np.subtract(salt_5_17, ds_z_s_an5) # Transect 8 May 2017

# Jun 2017 Deployment
s_anom_6_17 = np.subtract(salt_6_17, ds_z_s_an6) # Transect 1 Jun 2017
s_anom_7_17 = np.subtract(salt_7_17, ds_z_s_an7) # Transect 2 Jul 2017
s_anom_8_17 = np.subtract(salt_8_17, ds_z_s_an8) # Transect 3 Aug 2017
s_anom_9_17 = np.subtract(salt_9_17, ds_z_s_an9) # Transect 4 Sep 2017
s_anom_10_17_a = np.subtract(salt_10_17_a, ds_z_s_an10) # Transect 5 Oct 2017
s_anom_10_17_b = np.subtract(salt_10_17_b, ds_z_s_an10) # Transect 6 Oct 2017
s_anom_11_17 = np.subtract(salt_11_17, ds_z_s_an11) # Transect 7 Nov 2017

# Apr 2018 Deployment
s_anom_4_18 = np.subtract(salt_4_18, ds_z_s_an4) # Transect 1 Apr 2018
s_anom_5_18 = np.subtract(salt_5_18, ds_z_s_an5) # Transect 2 May 2018
s_anom_6_18 = np.subtract(salt_6_18, ds_z_s_an6) # Transect 3 Jun 2018
s_anom_8_18 = np.subtract(salt_8_18, ds_z_s_an8) # Transect 4 Aug 2018
s_anom_9_18_a = np.subtract(salt_9_18_a, ds_z_s_an9) # Transect 5 Sep 2018
s_anom_9_18_b = np.subtract(salt_9_18_b, ds_z_s_an9) # Transect 6 Sep 2018

# Nov 2018 Deployment
s_anom_11_18 = np.subtract(salt_11_18, ds_z_s_an11) # Transect 1 Nov 2018
s_anom_12_18 = np.subtract(salt_12_18, ds_z_s_an12) # Transect 2 Dec 2018
s_anom_1_19 = np.subtract(salt_1_19, ds_z_s_an1) # Transect 3 Jan 2019
s_anom_2_19 = np.subtract(salt_2_19, ds_z_s_an2) # Transect 4 Feb 2019
s_anom_3_19_a = np.subtract(salt_3_19_a, ds_z_s_an3) # Transect 5 Mar 2019
s_anom_3_19_b = np.subtract(salt_3_19_b, ds_z_s_an3) # Transect 6 Mar 2019
s_anom_4_19_a = np.subtract(salt_4_19_a, ds_z_s_an4) # Transect 7 Apr 2019

# Apr 2019 Deployment
s_anom_4_19_b = np.subtract(salt_4_19_b, ds_z_s_an4) # Transect 1 Apr 2019
s_anom_6_19 = np.subtract(salt_6_19, ds_z_s_an6) # Transect 2 Jun 2019
s_anom_7_19 = np.subtract(salt_7_19, ds_z_s_an7) # Transect 3 Jul 2019
s_anom_8_19 = np.subtract(salt_8_19, ds_z_s_an8) # Transect 4 Aug 2019

# Sep 2019 Deployment
s_anom_9_19 = np.subtract(salt_9_19, ds_z_s_an9) # Transect 1 Sep 2019
s_anom_10_19 = np.subtract(salt_10_19, ds_z_s_an10) # Transect 2 Oct 2019
s_anom_11_19 = np.subtract(salt_11_19, ds_z_s_an11) # Transect 3 Nov 2019
s_anom_12_19 = np.subtract(salt_12_19, ds_z_s_an12) # Transect 4 Dec 2019
s_anom_1_20 = np.subtract(salt_1_20, ds_z_s_an1) # Transect 5 Jan 2020
s_anom_2_20 = np.subtract(salt_2_20, ds_z_s_an2) # Transect 6 Feb 2020
s_anom_3_20_a = np.subtract(salt_3_20_a, ds_z_s_an3) # Transect 7 Mar 2020
s_anom_3_20_b = np.subtract(salt_3_20_b, ds_z_s_an3) # Transect 8 Mar 2020

# Sep 2020 Deployment
s_anom_9_20 = np.subtract(salt_9_20, ds_z_s_an9) # Transect 1 Sep 2020
s_anom_10_20 = np.subtract(salt_10_20, ds_z_s_an10) # Transect 2 Oct 2020
s_anom_11_20 = np.subtract(salt_11_20, ds_z_s_an11) # Transect 3 Nov 2020
s_anom_12_20 = np.subtract(salt_12_20, ds_z_s_an12) # Transect 4 Dec 2020
s_anom_1_21 = np.subtract(salt_1_21, ds_z_s_an1) # Transect 5 Jan 2021
s_anom_2_21 = np.subtract(salt_2_21, ds_z_s_an2) # Transect 6 Feb 2021

# Nov 2021 Deployment
s_anom_11_21 = np.subtract(salt_11_21, ds_z_s_an11) # Transect 1 Nov 2021
s_anom_12_21 = np.subtract(salt_12_21, ds_z_s_an12) # Transect 2 Dec 2021
s_anom_1_22 = np.subtract(salt_1_22, ds_z_s_an1) # Transect 3 Jan 2022
s_anom_2_22 = np.subtract(salt_2_22, ds_z_s_an2) # Transect 4 Feb 2022
s_anom_3_22 = np.subtract(salt_3_22, ds_z_s_an3) # Transect 5 Mar 2022
s_anom_4_22 = np.subtract(salt_4_22, ds_z_s_an4) # Transect 6 Apr 2022
s_anom_5_22 = np.subtract(salt_5_22, ds_z_s_an5) # Transect 7 May 2022
s_anom_6_22 = np.subtract(salt_6_22, ds_z_s_an6) # Transect 8 Jun 2022

# Jul 2022 Deployment
s_anom_8_22 = np.subtract(salt_8_22, ds_z_s_an8) # Transect 1 Aug 2022
s_anom_9_22 = np.subtract(salt_9_22, ds_z_s_an9) # Transect 2 Sep 2022
s_anom_10_22 = np.subtract(salt_10_22, ds_z_s_an10) # Transect 3 Oct 2022
s_anom_11_22 = np.subtract(salt_11_22, ds_z_s_an11) # Transect 4 Nov 2022
s_anom_12_22 = np.subtract(salt_12_22, ds_z_s_an12) # Transect 5 Dec 2022
s_anom_1_23 = np.subtract(salt_1_23, ds_z_s_an1) # Transect 6 Jan 2023

# Jan 2023 Deployment
s_anom_2_23 = np.subtract(salt_2_23, ds_z_s_an2) # Transect 1 Feb 2023
s_anom_3_23_a = np.subtract(salt_3_23_a, ds_z_s_an3) # Transect 2 Mar 2023
s_anom_3_23_b = np.subtract(salt_3_23_b, ds_z_s_an3) # Transect 3 Mar 2023
s_anom_4_23 = np.subtract(salt_4_23, ds_z_s_an4) # Transect 4 Apr 2023
s_anom_5_23 = np.subtract(salt_5_23, ds_z_s_an5) # Transect 5 May 2023
s_anom_6_23 = np.subtract(salt_6_23, ds_z_s_an6) # Transect 6 Jun 2023
s_anom_7_23 = np.subtract(salt_7_23, ds_z_s_an7) # Transect 7 Jul 2023
s_anom_8_23 = np.subtract(salt_8_23, ds_z_s_an8) # Transect 8 Aug 2023

# Oct 2023 Deployment
s_anom_10_23 = np.subtract(salt_10_23, ds_z_s_an10) # Transect 1 Oct 2023
s_anom_11_23 = np.subtract(salt_11_23, ds_z_s_an11) # Transect 2 Nov 2023
s_anom_12_23 = np.subtract(salt_12_23, ds_z_s_an12) # Transect 3 Dec 2023
s_anom_1_24 = np.subtract(salt_1_24, ds_z_s_an1) # Transect 4 Jan 2024
s_anom_2_24_a = np.subtract(salt_2_24_a, ds_z_s_an2) # Transect 5 Feb 2024
s_anom_2_24_b = np.subtract(salt_2_24_b, ds_z_s_an2) # Transect 6 Feb 2024
s_anom_3_24 = np.subtract(salt_3_24, ds_z_s_an3) # Transect 7 Mar 2024

# Apr 2024 Deployment
s_anom_4_24 = np.subtract(salt_4_24, ds_z_s_an4) # Transect 1 Apr 2024
s_anom_5_24 = np.subtract(salt_5_24, ds_z_s_an5) # Transect 2 May 2024
s_anom_6_24 = np.subtract(salt_6_24, ds_z_s_an6) # Transect 3 June 2024
s_anom_7_24 = np.subtract(salt_7_24, ds_z_s_an7) # Transect 4 July 2024
s_anom_8_24_a = np.subtract(salt_8_24_a, ds_z_s_an8) # Transect 5 Aug 2024
s_anom_8_24_b = np.subtract(salt_8_24_b, ds_z_s_an8) # Transect 6 Aug 2024

# Oct 2024 Deployment
s_anom_10_24 = np.subtract(salt_10_24, ds_z_s_an10) # Transect 1 Oct 2024
s_anom_11_24 = np.subtract(salt_11_24, ds_z_s_an11) # Transect 2 Nov 2024

# Mar 2025 Deployment
s_anom_3_25 = np.subtract(salt_3_25, ds_z_s_an3) # Transect 1 Mar 2025

# 200km Inshore Average Timeseries

# Data
# Transect Times
transect_times = {
    'tran_10_14': np.array([datetime(2014,10,9).toordinal()]),   # For cutoff values
    'tran_11_14': np.array([datetime(2014,11,9).toordinal()]),   # For cutoff values
    'tran_12_14_a':np.array([datetime(2014,12,9).toordinal()]),
    'tran_12_14_b':np.array([datetime(2014,12,28).toordinal()]),
    'tran_1_15':np.array([datetime(2015,1,23).toordinal()]),
    'tran_2_15_a':np.array([datetime(2015,2,12).toordinal()]),
    'tran_2_15_b':np.array([datetime(2015,2,24).toordinal()]),
    'tran_3_15':np.array([datetime(2015,3,26).toordinal()]),
    'tran_4_15':np.array([datetime(2015,4,28).toordinal()]),
    'tran_5_15':np.array([datetime(2015,5,30).toordinal()]),
    'tran_6_15':np.array([datetime(2015,6,30).toordinal()]),
    'tran_7_15':np.array([datetime(2015,7,29).toordinal()]),
    'tran_8_15':np.array([datetime(2015,8,24).toordinal()]),
    'tran_9_15':np.array([datetime(2015,9,10).toordinal()]),
    'tran_10_15':np.array([datetime(2015,10,9).toordinal()]),
    'tran_11_15':np.array([datetime(2015,11,17).toordinal()]),
    'tran_12_15':np.array([datetime(2015,12,23).toordinal()]),
    'tran_1_16':np.array([datetime(2016,1,30).toordinal()]),
    'tran_3_16':np.array([datetime(2016,3,4).toordinal()]),
    'tran_4_16':np.array([datetime(2016,4,14).toordinal()]),
    # 'tran_5_16':np.array([datetime(2016,5,15).toordinal()]),   # Something is wrong on this transect
    'tran_6_16':np.array([datetime(2016,6,10).toordinal()]),
    'tran_7_16':np.array([datetime(2016,7,10).toordinal()]),
    'tran_8_16':np.array([datetime(2016,8,11).toordinal()]),
    'tran_9_16_a':np.array([datetime(2016,9,10).toordinal()]),
    'tran_9_16_b':np.array([datetime(2016,9,28).toordinal()]),
    'tran_10_16_a':np.array([datetime(2016,10,11).toordinal()]),
    'tran_10_16_b':np.array([datetime(2016,10,18).toordinal()]),
    'tran_11_16':np.array([datetime(2016,11,10).toordinal()]),
    'tran_12_16':np.array([datetime(2016,12,10).toordinal()]),
    'tran_1_17':np.array([datetime(2017,1,10).toordinal()]),
    'tran_2_17':np.array([datetime(2017,2,9).toordinal()]),
    'tran_3_17':np.array([datetime(2017,3,9).toordinal()]),
    'tran_4_17_a':np.array([datetime(2017,4,8).toordinal()]),
    'tran_4_17_b':np.array([datetime(2017,4,28).toordinal()]),
    'tran_5_17':np.array([datetime(2017,5,22).toordinal()]),
    'tran_6_17':np.array([datetime(2017,6,17).toordinal()]),
    'tran_7_17':np.array([datetime(2017,7,15).toordinal()]),
    'tran_8_17':np.array([datetime(2017,8,13).toordinal()]),
    'tran_9_17':np.array([datetime(2017,9,17).toordinal()]),
    'tran_10_17_a':np.array([datetime(2017,10,14).toordinal()]),
    'tran_10_17_b':np.array([datetime(2017,10,27).toordinal()]),
    # 'tran_11_17':np.array([datetime(2017,11,4).toordinal()]),   # Messes with interpolation between deployments    
    'tran_4_18':np.array([datetime(2018,4,30).toordinal()]),
    'tran_5_18':np.array([datetime(2018,5,28).toordinal()]),
    'tran_6_18':np.array([datetime(2018,6,29).toordinal()]),
    'tran_8_18':np.array([datetime(2018,8,3).toordinal()]),
    'tran_9_18_a':np.array([datetime(2018,9,9).toordinal()]),
    # 'tran_9_18_b':np.array([datetime(2018,9,30).toordinal()]),   # Something is wrong on this transect
    'tran_11_18':np.array([datetime(2018,11,14).toordinal()]),
    'tran_12_18':np.array([datetime(2018,12,24).toordinal()]),
    'tran_1_19':np.array([datetime(2019,1,25).toordinal()]),
    'tran_2_19':np.array([datetime(2019,2,19).toordinal()]),
    'tran_3_19_a':np.array([datetime(2019,3,13).toordinal()]),
    'tran_3_19_b':np.array([datetime(2019,3,28).toordinal()]),
    'tran_4_19_a':np.array([datetime(2019,4,6).toordinal()]),
    'tran_4_19_b':np.array([datetime(2019,4,22).toordinal()]),
    'tran_6_19':np.array([datetime(2019,6,3).toordinal()]),
    'tran_7_19':np.array([datetime(2019,7,4).toordinal()]),
    'tran_8_19':np.array([datetime(2019,8,6).toordinal()]),    
    'tran_9_19':np.array([datetime(2019,9,30).toordinal()]),
    'tran_10_19':np.array([datetime(2019,10,28).toordinal()]),
    'tran_11_19':np.array([datetime(2019,11,24).toordinal()]),
    'tran_12_19':np.array([datetime(2019,12,19).toordinal()]),
    'tran_1_20':np.array([datetime(2020,1,17).toordinal()]),
    'tran_2_20':np.array([datetime(2020,2,15).toordinal()]),
    'tran_3_20_a':np.array([datetime(2020,3,5).toordinal()]),
    'tran_3_20_b':np.array([datetime(2020,3,13).toordinal()]),
    'tran_9_20':np.array([datetime(2020,9,29).toordinal()]),
    'tran_10_20':np.array([datetime(2020,10,24).toordinal()]),
    'tran_11_20':np.array([datetime(2020,11,19).toordinal()]),
    'tran_12_20':np.array([datetime(2020,12,15).toordinal()]),
    'tran_1_21':np.array([datetime(2021,1,10).toordinal()]),
    # 'tran_2_21':np.array([datetime(2021,2,1).toordinal()]),  # The dates are wrong on this transect
    'tran_11_21':np.array([datetime(2021,11,27).toordinal()]),
    'tran_12_21':np.array([datetime(2021,12,27).toordinal()]),
    'tran_1_22':np.array([datetime(2022,1,22).toordinal()]),
    'tran_2_22':np.array([datetime(2022,2,22).toordinal()]),
    'tran_3_22':np.array([datetime(2022,3,29).toordinal()]),
    'tran_4_22':np.array([datetime(2022,5,3).toordinal()]),
    'tran_5_22':np.array([datetime(2022,5,29).toordinal()]),
    'tran_6_22':np.array([datetime(2022,6,9).toordinal()]),
    'tran_8_22':np.array([datetime(2022,8,11).toordinal()]),
    'tran_9_22':np.array([datetime(2022,9,15).toordinal()]),
    'tran_10_22':np.array([datetime(2022,10,20).toordinal()]),
    'tran_11_22':np.array([datetime(2022,11,27).toordinal()]),
    'tran_12_22':np.array([datetime(2022,12,20).toordinal()]),
    'tran_1_23':np.array([datetime(2023,1,19).toordinal()]),
    'tran_2_23':np.array([datetime(2023,2,7).toordinal()]),
    'tran_3_23_a':np.array([datetime(2023,3,7).toordinal()]),
    'tran_3_23_b':np.array([datetime(2023,3,29).toordinal()]),
    'tran_4_23':np.array([datetime(2023,4,27).toordinal()]),
    'tran_5_23':np.array([datetime(2023,5,22).toordinal()]),
    'tran_6_23':np.array([datetime(2023,6,22).toordinal()]),
    'tran_7_23':np.array([datetime(2023,7,15).toordinal()]),
    'tran_8_23':np.array([datetime(2023,8,9).toordinal()]),
    'tran_10_23':np.array([datetime(2023,11,12).toordinal()]),
    'tran_11_23':np.array([datetime(2023,11,28).toordinal()]),
    'tran_12_23':np.array([datetime(2023,12,21).toordinal()]),
    'tran_1_24':np.array([datetime(2024,1,10).toordinal()]),
    'tran_2_24_a':np.array([datetime(2024,2,2).toordinal()]),
    'tran_2_24_b':np.array([datetime(2024,2,24).toordinal()]),
    'tran_3_24':np.array([datetime(2024,3,15).toordinal()]),
    'tran_4_24':np.array([datetime(2024,4,17).toordinal()]),
    'tran_5_24':np.array([datetime(2024,5,18).toordinal()]),  
    'tran_6_24':np.array([datetime(2024,6,11).toordinal()]),  
    # 'tran_7_24':np.array([datetime(2024,7,11).toordinal()]), # Bad salinity data
    # 'tran_8_24_a':np.array([datetime(2024,8,7).toordinal()]), # Bad salinity data
    # 'tran_8_24_b':np.array([datetime(2024,8,19).toordinal()]), # Bad salinity data
    'tran_10_24':np.array([datetime(2024,10,28).toordinal()]), 
    'tran_11_24':np.array([datetime(2024,11,22).toordinal()]),
    'tran_3_25':np.array([datetime(2025,3,13).toordinal()]),
    'tran_4_25':np.array([datetime(2025,4,15).toordinal()]),   # For cutoff values
    'tran_5_25':np.array([datetime(2025,5,15).toordinal()]),   # For cutoff values
}


# Temperature
transects_temp = {
    '10_14': t_anom_12_14_a,   # Repeat for cutoff values
    '11_14': t_anom_12_14_a,   # Repeat for cutoff values
    '12_14_a':t_anom_12_14_a,
    '12_14_b':t_anom_12_14_b,
    '1_15':t_anom_1_15,
    '2_15_a':t_anom_2_15_a,
    '2_15_b':t_anom_2_15_b,
    '3_15':t_anom_3_15,
    '4_15':t_anom_4_15,
    '5_15':t_anom_5_15,
    '6_15':t_anom_6_15,
    '7_15':t_anom_7_15,
    '8_15':t_anom_8_15,
    '9_15':t_anom_9_15,
    '10_15':t_anom_10_15,
    '11_15':t_anom_11_15,
    '12_15':t_anom_12_15,
    '1_16':t_anom_1_16,
    '3_16':t_anom_3_16,
    '4_16':t_anom_4_16,
    # '5_16':t_anom_5_16,   # Something is wrong on this transect
    '6_16':t_anom_6_16,
    '7_16':t_anom_7_16,
    '8_16':t_anom_8_16,
    '9_16_a':t_anom_9_16_a,
    '9_16_b':t_anom_9_16_b,
    '10_16_a':t_anom_10_16_a,
    '10_16_b':t_anom_10_16_b,
    '11_16':t_anom_11_16,
    '12_16':t_anom_12_16,
    '1_17':t_anom_1_17,
    '2_17':t_anom_2_17,
    '3_17':t_anom_3_17,
    '4_17_a':t_anom_4_17_a,
    '4_17_b':t_anom_4_17_b,
    '5_17':t_anom_5_17,
    '6_17':t_anom_6_17,
    '7_17':t_anom_7_17,
    '8_17':t_anom_8_17,
    '9_17':t_anom_9_17,
    '10_17_a':t_anom_10_17_a,
    '10_17_b':t_anom_10_17_b,
    # '11_17':t_anom_11_17,   # Messes with interpolation between deployments
    '4_18':t_anom_4_18,
    '5_18':t_anom_5_18,
    '6_18':t_anom_6_18,
    '8_18':t_anom_8_18,
    '9_18_a':t_anom_9_18_a,
    # '9_18_b':t_anom_9_18_b,   # Something is wrong on this transect
    '11_18':t_anom_11_18,
    '12_18':t_anom_12_18,
    '1_19':t_anom_1_19,
    '2_19':t_anom_2_19,
    '3_19_a':t_anom_3_19_a,
    '3_19_b':t_anom_3_19_b,
    '4_19_a':t_anom_4_19_a,
    '4_19_b':t_anom_4_19_b,
    '6_19':t_anom_6_19,
    '7_19':t_anom_7_19,
    '8_19':t_anom_8_19,
    '9_19':t_anom_9_19, 
    '10_19':t_anom_10_19,
    '11_19':t_anom_11_19,
    '12_19':t_anom_12_19,
    '1_20':t_anom_1_20,
    '2_20':t_anom_2_20,
    '3_20_a':t_anom_3_20_a,
    '3_20_b':t_anom_3_20_b,
    '9_20':t_anom_9_20,
    '10_20':t_anom_10_20,
    '11_20':t_anom_11_20,
    '12_20':t_anom_12_20,
    '1_21':t_anom_1_21,
    # '2_21':t_anom_2_21,  # The dates are wrong on this transect
    '11_21':t_anom_11_21,
    '12_21':t_anom_12_21,
    '1_22':t_anom_1_22,
    '2_22':t_anom_2_22,
    '3_22':t_anom_3_22,
    '4_22':t_anom_4_22,
    '5_22':t_anom_5_22,
    '6_22':t_anom_6_22,
    '8_22':t_anom_8_22,
    '9_22':t_anom_9_22,
    '10_22':t_anom_10_22,
    '11_22':t_anom_11_22,
    '12_22':t_anom_12_22,
    '1_23':t_anom_1_23,
    '2_23':t_anom_2_23,
    '3_23_a':t_anom_3_23_a,
    '3_23_b':t_anom_3_23_b,
    '4_23':t_anom_4_23,
    '5_23':t_anom_5_23,
    '6_23':t_anom_6_23,
    '7_23':t_anom_7_23,
    '8_23':t_anom_8_23,
    '10_23':t_anom_10_23,
    '11_23':t_anom_11_23,
    '12_23':t_anom_12_23,
    '1_24':t_anom_1_24,
    '2_24_a':t_anom_2_24_a,
    '2_24_b':t_anom_2_24_b,
    '3_24': t_anom_3_24,
    '4_24': t_anom_4_24,
    '5_24': t_anom_5_24,   
    '6_24': t_anom_6_24,   
    # '7_24': t_anom_7_24, # Bad salinity data
    # '8_24_a': t_anom_8_24_a, # Bad salinity data
    # '8_24_b': t_anom_8_24_b, # Bad salinity data
    '10_24': t_anom_10_24, 
    '11_24': t_anom_11_24, 
    '3_25': t_anom_3_25,   # Repeating for cutoff values
    '4_25': t_anom_3_25,   # Repeating for cutoff values
    '5_25': t_anom_3_25,   # Repeating for cutoff values
}

combined_temp_data = []

print('\nCreating a mean depth profile for each transect...')
for transect, array in transects_temp.items():
    transects_temp[transect] = np.mean(array, axis=1)   # Creates a profile of the mean values across depth

for transect, array in transects_temp.items():
    transects_temp[transect] = xr.DataArray(array)   # Converts the numpy array to an xarray DataArray for the next step
    
print('\nAdding transect time to the temp anomaly data...')
for (transect, array), (transect_time, time) in zip(transects_temp.items(), transect_times.items()):
    transects_temp[transect] = array.expand_dims(time=time)   # Adds the time point from transect_times to the DataArray

for transect, array in transects_temp.items():
    combined_temp_data.append(array)   # Appends the DataArray to the list: combined_temp_data

print('\nConcatenating new dataset "combined_temp"...')
combined_temp = xr.concat(combined_temp_data, dim='time')   # Concatenates all of the data together


# Replicating surface values up to 10m above surface to prevent cutoff during filtering
print('\nReplicating surface values up to 10m above the surface...')
surf_vals = combined_temp[:, 1]

surf_vals2 = xr.DataArray(surf_vals)
surf_vals3 = xr.DataArray(surf_vals)

surf_vals2['depth'] = -5
surf_vals3['depth'] = -10

combined_temp = xr.concat((surf_vals2, combined_temp), dim='depth')
combined_temp = xr.concat((surf_vals3, combined_temp), dim='depth')

# Replace surface values with data at 5 meters depth to rid of NaN's
combined_temp[:,2] = combined_temp[:,3]

print('\nGridding the temperature data...') # Generate a regular grid to interpolate the data
xgrid = np.arange(combined_temp['time'].min(), combined_temp['time'].max(), 30) # Every 30 days in time
ygrid = np.arange(-10,1000,5) # Every 5m in depth

print('\nInterpolating the temperature data...')
combined_temp = combined_temp.interp(time=xgrid,depth=ygrid, method='linear') # Interpolate the data over the new grid
temp_Xgrid, temp_Ygrid = np.meshgrid(combined_temp['time'], combined_temp['depth']) # Use meshgrid to create a regular grid of time and depth

temp = combined_temp.values.T # Transpose the temperature data
temp = pd.DataFrame(temp) # Make it a pandas dataframe

print('\nApplying a 3-month boxcar filter...')
temp_box = temp.T.rolling(window=3, center=True, win_type='boxcar').mean() # Boxcar Filter every 3 transects (90 days)
temp_box = temp_box.T.rolling(window=4, center=True, win_type='boxcar').mean() # Boxcar Filter every 4 x 5m (20m)

# temp_roll = temp.rolling(window=3, center=True, win_type='boxcar').mean() # Rolling boxcar filter every 3 transects (90 days)

fifty_meters = temp_box.T[12] # Extract fifty-meters values
zero_meters = temp_box.T[2] # Extract surface values

fifty_meters = xr.DataArray(fifty_meters) # Save to xarray data array
zero_meters = xr.DataArray(zero_meters) # Save to xarray data array
thi_time = combined_temp['time'] # Save the Trinidad Head Index time as "thi_time"


# Salinity

transects_salt = {
    '10_14': s_anom_12_14_a,   # Repeat for cutoff values
    '11_14': s_anom_12_14_a,   # Repeat for cutoff values
    '12_14_a':s_anom_12_14_a,
    '12_14_b':s_anom_12_14_b,
    '1_15':s_anom_1_15,
    '2_15_a':s_anom_2_15_a,
    '2_15_b':s_anom_2_15_b,
    '3_15':s_anom_3_15,
    '4_15':s_anom_4_15,
    '5_15':s_anom_5_15,
    '6_15':s_anom_6_15,
    '7_15':s_anom_7_15,
    '8_15':s_anom_8_15,
    '9_15':s_anom_9_15,    
    '10_15':s_anom_10_15,
    '11_15':s_anom_11_15,
    '12_15':s_anom_12_15,
    '1_16':s_anom_1_16,
    '3_16':s_anom_3_16,
    '4_16':s_anom_4_16,
    # '5_16':s_anom_5_16,   # Something is wrong on this transect
    '6_16':s_anom_6_16,
    '7_16':s_anom_7_16,
    '8_16':s_anom_8_16,
    '9_16_a':s_anom_9_16_a,
    '9_16_b':s_anom_9_16_b,
    '10_16_a':s_anom_10_16_a,
    '10_16_b':s_anom_10_16_b,
    '11_16':s_anom_11_16,
    '12_16':s_anom_12_16,
    '1_17':s_anom_1_17,
    '2_17':s_anom_2_17,
    '3_17':s_anom_3_17,
    '4_17_a':s_anom_4_17_a,
    '4_17_b':s_anom_4_17_b,
    '5_17':s_anom_5_17,
    '6_17':s_anom_6_17,
    '7_17':s_anom_7_17,
    '8_17':s_anom_8_17,
    '9_17':s_anom_9_17,
    '10_17_a':s_anom_10_17_a,
    '10_17_b':s_anom_10_17_b,
    # '11_17':s_anom_11_17,   # Messes with interpolation between deployments
    '4_18':s_anom_4_18,
    '5_18':s_anom_5_18,
    '6_18':s_anom_6_18,
    '8_18':s_anom_8_18,
    '9_18_a':s_anom_9_18_a,
    # '9_18_b':s_anom_9_18_b,   # Something is wrong on this transect
    '11_18':s_anom_11_18,
    '12_18':s_anom_12_18,
    '1_19':s_anom_1_19,
    '2_19':s_anom_2_19,
    '3_19_a':s_anom_3_19_a,
    '3_19_b':s_anom_3_19_b,
    '4_19_a':s_anom_4_19_a,
    '4_19_b':s_anom_4_19_b,
    '6_19':s_anom_6_19,
    '7_19':s_anom_7_19,
    '8_19':s_anom_8_19,
    '9_19':s_anom_9_19, 
    '10_19':s_anom_10_19,
    '11_19':s_anom_11_19,
    '12_19':s_anom_12_19,
    '1_20':s_anom_1_20,
    '2_20':s_anom_2_20,
    '3_20_a':s_anom_3_20_a,
    '3_20_b':s_anom_3_20_b,
    '9_20':s_anom_9_20,
    '10_20':s_anom_10_20,
    '11_20':s_anom_11_20,
    '12_20':s_anom_12_20,
    '1_21':s_anom_1_21,
    # '2_21':s_anom_2_21,  # The dates are wrong on this transect
    '11_21':s_anom_11_21,
    '12_21':s_anom_12_21,
    '1_22':s_anom_1_22,
    '2_22':s_anom_2_22,
    '3_22':s_anom_3_22,
    '4_22':s_anom_4_22,
    '5_22':s_anom_5_22,
    '6_22':s_anom_6_22,
    '8_22':s_anom_8_22,
    '9_22':s_anom_9_22,
    '10_22':s_anom_10_22,
    '11_22':s_anom_11_22,
    '12_22':s_anom_12_22,
    '1_23':s_anom_1_23,
    '2_23':s_anom_2_23,
    '3_23_a':s_anom_3_23_a,
    '3_23_b':s_anom_3_23_b,
    '4_23':s_anom_4_23,
    '5_23':s_anom_5_23,
    '6_23':s_anom_6_23,
    '7_23':s_anom_7_23,
    '8_23':s_anom_8_23,
    '10_23':s_anom_10_23,
    '11_23':s_anom_11_23,
    '12_23':s_anom_12_23,
    '1_24':s_anom_1_24,
    '2_24_a':s_anom_2_24_a,
    '2_24_b':s_anom_2_24_b,
    '3_24': s_anom_3_24,
    '4_24': s_anom_4_24,
    '5_24': s_anom_5_24,   
    '6_24': s_anom_6_24,   
    # '7_24': s_anom_7_24, # Bad salinity data
    # '8_24_a': s_anom_8_24_a, # Bad salinity data
    # '8_24_b': s_anom_8_24_b, # Bad salinity data
    '10_24': s_anom_10_24, 
    '11_24': s_anom_11_24, 
    '3_25': s_anom_3_25,  # Repeat for cutoff values
    '4_25': s_anom_3_25,  # Repeat for cutoff values
    '5_25': s_anom_3_25,  # Repeat for cutoff values
}

combined_salt_data = []

print('\nCreating a mean depth profile for each transect...')
for transect, array in transects_salt.items():
    transects_salt[transect] = np.mean(array, axis=1)

for transect, array in transects_salt.items():
    transects_salt[transect] = xr.DataArray(array)
    
print('\nAdding transect time to the salinity anomaly data...')
for (transect, array), (transect_time, time) in zip(transects_salt.items(), transect_times.items()):
    transects_salt[transect] = array.expand_dims(time=time)
    
for transect, array in transects_salt.items():
    combined_salt_data.append(array)
    
print('\nConcatenating new dataset "combined_salt"...')
combined_salt = xr.concat(combined_salt_data, dim='time')

# Replicating surface values up to 10m above surface to prevent cutoff during filtering
print('\nReplicating surface values up to 10m above the surface...')
surf_vals = combined_salt[:, 1]

surf_vals = xr.DataArray(surf_vals)
surf_vals2 = xr.DataArray(surf_vals)

surf_vals['depth'] = -5
surf_vals2['depth'] = -10

combined_salt = xr.concat((surf_vals, combined_salt), dim='depth')
combined_salt = xr.concat((surf_vals2, combined_salt), dim='depth')

# Replace surface values with data at 5 meters depth to rid of NaN's
combined_salt[:,2] = combined_salt[:,3]

print('\nGridding the salinity data...') # Generate a regular grid to interpolate the data
xgrid = np.arange(combined_salt['time'].min(), combined_salt['time'].max(), 30) # Every 30 days in time
ygrid = np.arange(-10,1000, 5) # Every 5m depth

print('\nInterpolating the salinity data...')
combined_salt = combined_salt.interp(time=xgrid,depth=ygrid) # Interpolate the data over the new grid
salt_Xgrid, salt_Ygrid = np.meshgrid(combined_salt['time'], combined_salt['depth']) # Meshgrid the time and depth

salt = combined_salt.values.T # Transpose the salinity data
salt = pd.DataFrame(salt) # Make it a pandas dataframe

print('\nApplying a 3-month boxcar filter...')
salt_box = salt.T.rolling(window=3, center=True, win_type='boxcar').mean() # Boxcar Filter every 3 transects (90 days)
salt_box = salt_box.T.rolling(window=4, center=True, win_type='boxcar').mean() # Boxcar Filter every 4 x 5m (20m)

# salt_roll = salt.rolling(window=3, center=True, win_type='boxcar').mean()


# Plots

# Boundaries
# Set Colorbar and Contour Line Ranges
boundaries_temp = [-4, -3.5, -3, -2.5, -2, -1.5, -1, -0.5, 0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4]
levels_temp = [-4, -3.5, -3, -2.5, -2, -1.5, -1, -0.5, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4]
boundaries_salt = [-.6, -.4, -.2, 0, .2, .4, .6]
levels_salt = [-.6, -.4, -.2, .2, .4, .6]
boundaries_oxy = [0, 50, 100, 150, 200, 250, 300]

divnorm_temp=colors.TwoSlopeNorm(vcenter=0., vmin=-4, vmax=4)
divnorm_salt=colors.TwoSlopeNorm(vcenter=0., vmin=-.75, vmax=.75)

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S") # Timestamp for file naming


# Contour Plots

# Plot the figure: Trinidad Head Averaged Over Inshore 200km (Filtered)
print(f'\nPlotting t_anom_timeseries_{timestamp}.png...')
fig, (ax3, ax4) = plt.subplots(2, 1, figsize=(14,8), dpi=300)

plot3 = ax3.contourf(temp_Xgrid, temp_Ygrid, temp_box, cmap='RdYlBu_r', norm=divnorm_temp, levels=boundaries_temp)
lines3 = ax3.contour(temp_Xgrid, temp_Ygrid, temp_box, colors='black', norm=divnorm_temp, levels=levels_temp, alpha=0.75)
deployment1_nov_14 = ax3.hlines(y=570, xmin=datetime(2014,12,4).toordinal(), xmax=datetime(2015,3,9).toordinal(), color='k')
deployment1_mar_15 = ax3.hlines(y=570, xmin=datetime(2015,3,9).toordinal(), xmax=datetime(2015,9,17).toordinal(), color='k')
deployment1_sep_15 = ax3.hlines(y=570, xmin=datetime(2015,9,17).toordinal(), xmax=datetime(2016,5,16).toordinal(), color='k')
deployment1_may_16 = ax3.hlines(y=570, xmin=datetime(2016,5,23).toordinal(), xmax=datetime(2016,10,21).toordinal(), color='k')
deployment1_oct_16 = ax3.hlines(y=570, xmin=datetime(2016,10,21).toordinal(), xmax=datetime(2017,6,5).toordinal(), color='k')
deployment1_jun_17 = ax3.hlines(y=570, xmin=datetime(2017,6,5).toordinal(), xmax=datetime(2017,11,6).toordinal(), color='k')
deployment1_apr_18 = ax3.hlines(y=570, xmin=datetime(2018,4,17).toordinal(), xmax=datetime(2018,10,2).toordinal(), color='k')
deployment1_nov_18 = ax3.hlines(y=570, xmin=datetime(2018,11,7).toordinal(), xmax=datetime(2019,4,9).toordinal(), color='k')
deployment1_apr_19 = ax3.hlines(y=570, xmin=datetime(2019,4,9).toordinal(), xmax=datetime(2019,8,19).toordinal(), color='k')
deployment1_sep_19 = ax3.hlines(y=570, xmin=datetime(2019,9,16).toordinal(), xmax=datetime(2020,3,19).toordinal(), color='k')
deployment1_sep_20 = ax3.hlines(y=570, xmin=datetime(2020,9,16).toordinal(), xmax=datetime(2021,2,6).toordinal(), color='k')
deployment1_nov_21 = ax3.hlines(y=570, xmin=datetime(2021,11,12).toordinal(), xmax=datetime(2022,6,16).toordinal(), color='k')
deployment1_jul_22 = ax3.hlines(y=570, xmin=datetime(2022,7,29).toordinal(), xmax=datetime(2023,1,26).toordinal(), color='k')
deployment1_jan_23 = ax3.hlines(y=570, xmin=datetime(2023,1,26).toordinal(), xmax=datetime(2023,8,14).toordinal(), color='k')
deployment1_oct_23 = ax3.hlines(y=570, xmin=datetime(2023,10,13).toordinal(), xmax=datetime(2024,4,12).toordinal(), color='k')
deployment1_apr_24 = ax3.hlines(y=570, xmin=datetime(2024,4,12).toordinal(), xmax=datetime(2024,8,9).toordinal(), color='k')
deployment1_oct_24 = ax3.hlines(y=570, xmin=datetime(2024,10,21).toordinal(), xmax=datetime(2024,12,4).toordinal(), color='k')
deployment1_mar_25 = ax3.hlines(y=570, xmin=datetime(2025,3,21).toordinal(), xmax=temp_Xgrid.max(), color='k')
ax3.clabel(lines3, lines3.levels, inline=True, fontsize=10)
ax3.invert_yaxis()
ax3.set_ylabel('Depth (m)')
ax3.text(datetime(2022,7,15).toordinal(), 530, 'Temperature Anomaly', fontsize='large')
ax3.set_yticks((0, 200, 400, 600))
ax3.set_xticks((datetime(2015,1,1).toordinal(), datetime(2016,1,1).toordinal(), datetime(2017,1,1).toordinal(), datetime(2018,1,1).toordinal(), datetime(2019,1,1).toordinal(), datetime(2020,1,1).toordinal(), datetime(2021,1,1).toordinal(),
               datetime(2022,1,1).toordinal(), datetime(2023,1,1).toordinal(), datetime(2024,1,1).toordinal(), datetime(2025,1,1).toordinal()))
ax3.set_xticklabels(('2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024', '2025'))
ax3.set_xlim(datetime(2014,12,4).toordinal(), datetime(2025,5,1).toordinal())
ax3.set_ylim(600, 0)
ax3.spines[:].set_linewidth(2)
ax3.tick_params(width=2, top=True, right=True, direction='in')
ax3.set_title('Trinidad Head Averaged Over Inshore 200km (Filtered)', pad=10)
cbar1 = plt.colorbar(plot3, shrink=0.5, location='right', pad=0.015)
cbar1.outline.set_linewidth(2)
cbar1.set_label(label=r'($\degree$C)', rotation=0, labelpad=10)

plot4 = ax4.contourf(salt_Xgrid, salt_Ygrid, salt_box, cmap='BrBG_r', norm=divnorm_salt, levels=boundaries_salt)
lines4 = ax4.contour(salt_Xgrid, salt_Ygrid, salt_box, colors='black', norm=divnorm_salt, levels=levels_salt, alpha=0.75)
deployment2_nov_14 = ax4.hlines(y=570, xmin=datetime(2014,12,4).toordinal(), xmax=datetime(2015,3,9).toordinal(), color='k')
deployment2_mar_15 = ax4.hlines(y=570, xmin=datetime(2015,3,9).toordinal(), xmax=datetime(2015,9,17).toordinal(), color='k')
deployment2_sep_15 = ax4.hlines(y=570, xmin=datetime(2015,9,17).toordinal(), xmax=datetime(2016,5,16).toordinal(), color='k')
deployment2_may_16 = ax4.hlines(y=570, xmin=datetime(2016,5,23).toordinal(), xmax=datetime(2016,10,21).toordinal(), color='k')
deployment2_oct_16 = ax4.hlines(y=570, xmin=datetime(2016,10,21).toordinal(), xmax=datetime(2017,6,5).toordinal(), color='k')
deployment2_jun_17 = ax4.hlines(y=570, xmin=datetime(2017,6,5).toordinal(), xmax=datetime(2017,11,6).toordinal(), color='k')
deployment2_apr_18 = ax4.hlines(y=570, xmin=datetime(2018,4,17).toordinal(), xmax=datetime(2018,10,2).toordinal(), color='k')
deployment2_nov_18 = ax4.hlines(y=570, xmin=datetime(2018,11,7).toordinal(), xmax=datetime(2019,4,9).toordinal(), color='k')
deployment2_apr_19 = ax4.hlines(y=570, xmin=datetime(2019,4,9).toordinal(), xmax=datetime(2019,8,19).toordinal(), color='k')
deployment2_sep_19 = ax4.hlines(y=570, xmin=datetime(2019,9,16).toordinal(), xmax=datetime(2020,3,19).toordinal(), color='k')
deployment2_sep_20 = ax4.hlines(y=570, xmin=datetime(2020,9,16).toordinal(), xmax=datetime(2021,2,6).toordinal(), color='k')
deployment2_nov_21 = ax4.hlines(y=570, xmin=datetime(2021,11,12).toordinal(), xmax=datetime(2022,6,16).toordinal(), color='k')
deployment2_jul_22 = ax4.hlines(y=570, xmin=datetime(2022,7,29).toordinal(), xmax=datetime(2023,1,26).toordinal(), color='k')
deployment2_jan_23 = ax4.hlines(y=570, xmin=datetime(2023,1,26).toordinal(), xmax=datetime(2023,8,14).toordinal(), color='k')
deployment2_oct_23 = ax4.hlines(y=570, xmin=datetime(2023,10,13).toordinal(), xmax=datetime(2024,4,12).toordinal(), color='k')
deployment2_apr_24 = ax4.hlines(y=570, xmin=datetime(2024,4,12).toordinal(), xmax=datetime(2024,8,9).toordinal(), color='k')
deployment2_oct_24 = ax4.hlines(y=570, xmin=datetime(2024,10,21).toordinal(), xmax=datetime(2024,12,4).toordinal(), color='k')
deployment2_mar_25 = ax4.hlines(y=570, xmin=datetime(2025,3,21).toordinal(), xmax=salt_Xgrid.max(), color='k')
ax4.clabel(lines4, lines4.levels, inline=True, fontsize=10)
ax4.invert_yaxis()
ax4.set_ylabel('Depth (m)')
ax4.text(datetime(2022,10,20).toordinal(), 530, 'Salinity Anomaly', fontsize='large')
ax4.set_xlabel('Year')
ax4.set_yticks((0, 200, 400, 600))
ax4.set_xticks((datetime(2015,1,1).toordinal(), datetime(2016,1,1).toordinal(), datetime(2017,1,1).toordinal(), datetime(2018,1,1).toordinal(), datetime(2019,1,1).toordinal(), datetime(2020,1,1).toordinal(), datetime(2021,1,1).toordinal(),
               datetime(2022,1,1).toordinal(), datetime(2023,1,1).toordinal(), datetime(2024,1,1).toordinal(), datetime(2025,1,1).toordinal()))
ax4.set_xticklabels(('2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024', '2025'))
ax4.set_xlim(datetime(2014,12,4).toordinal(), datetime(2025,5,1).toordinal())
ax4.set_ylim(600, 0)
ax4.spines[:].set_linewidth(2)
ax4.tick_params(width=2, top=True, right=True, direction='in')
cbar2 = plt.colorbar(plot4, shrink=0.5, location='right', pad=0.015)
cbar2.outline.set_linewidth(2)
cbar2.set_label(label=r'(PSU)', rotation=0, labelpad=10)
plt.tight_layout()
plt.savefig(f'C:/Users/marqjace/OneDrive - Oregon State University/Desktop/Python/TH-Line_timeseries/figures/t_anom_timeseries_{timestamp}.png')


# # Plot the figure: Grid
# fig, (ax5, ax6) = plt.subplots(2, 1, figsize=(14,8), dpi=300)

# scat5 = ax5.scatter(temp_Xgrid, temp_Ygrid, s=2)
# deployment1_nov_14 = ax5.hlines(y=570, xmin=datetime(2014,12,4).toordinal(), xmax=datetime(2015,3,9).toordinal(), color='k')
# deployment1_sep_15 = ax5.hlines(y=570, xmin=datetime(2015,9,17).toordinal(), xmax=datetime(2016,5,16).toordinal(), color='k')
# deployment1_may_16 = ax5.hlines(y=570, xmin=datetime(2016,5,23).toordinal(), xmax=datetime(2016,10,21).toordinal(), color='k')
# deployment1_oct_16 = ax5.hlines(y=570, xmin=datetime(2016,10,21).toordinal(), xmax=datetime(2017,6,5).toordinal(), color='k')
# deployment1_jun_17 = ax5.hlines(y=570, xmin=datetime(2017,6,5).toordinal(), xmax=datetime(2017,11,6).toordinal(), color='k')
# deployment1_apr_18 = ax5.hlines(y=570, xmin=datetime(2018,4,17).toordinal(), xmax=datetime(2018,10,2).toordinal(), color='k')
# deployment1_nov_18 = ax5.hlines(y=570, xmin=datetime(2018,11,7).toordinal(), xmax=datetime(2019,4,9).toordinal(), color='k')
# deployment1_apr_19 = ax5.hlines(y=570, xmin=datetime(2019,4,9).toordinal(), xmax=datetime(2019,8,19).toordinal(), color='k')
# deployment1_sep_19 = ax5.hlines(y=570, xmin=datetime(2019,9,16).toordinal(), xmax=datetime(2020,3,19).toordinal(), color='k')
# deployment1_sep_20 = ax5.hlines(y=570, xmin=datetime(2020,9,16).toordinal(), xmax=datetime(2021,2,6).toordinal(), color='k')
# deployment1_nov_21 = ax5.hlines(y=570, xmin=datetime(2021,11,12).toordinal(), xmax=datetime(2022,6,16).toordinal(), color='k')
# deployment1_jul_22 = ax5.hlines(y=570, xmin=datetime(2022,7,29).toordinal(), xmax=datetime(2023,1,26).toordinal(), color='k')
# deployment1_jan_23 = ax5.hlines(y=570, xmin=datetime(2023,1,26).toordinal(), xmax=datetime(2023,8,14).toordinal(), color='k')
# deployment1_oct_23 = ax5.hlines(y=570, xmin=datetime(2023,10,13).toordinal(), xmax=datetime(2024,4,12).toordinal(), color='k')
# deployment1_apr_24 = ax5.hlines(y=570, xmin=datetime(2024,4,12).toordinal(), xmax=datetime(2024,8,9).toordinal(), color='k')
# deployment1_oct_24 = ax5.hlines(y=570, xmin=datetime(2024,10,21).toordinal(), xmax=datetime(2024,12,4).toordinal(), color='k')
# deployment1_mar_25 = ax5.hlines(y=570, xmin=datetime(2025,3,21).toordinal(), xmax=temp_Xgrid.max(), color='k')
# # ax5.clabel(lines1, lines1.levels, inline=True, fontsize=10)
# ax5.invert_yaxis()
# ax5.set_ylabel('Depth (m)')
# ax5.text(datetime(2022,8,1).toordinal(), 530, 'Temperature Anomaly', fontsize='large')
# ax5.set_yticks((0, 200, 400, 600))
# ax5.set_xticks((datetime(2015,1,1).toordinal(), datetime(2016,1,1).toordinal(), datetime(2017,1,1).toordinal(), datetime(2018,1,1).toordinal(), datetime(2019,1,1).toordinal(), datetime(2020,1,1).toordinal(), datetime(2021,1,1).toordinal(),
#                datetime(2022,1,1).toordinal(), datetime(2023,1,1).toordinal(), datetime(2024,1,1).toordinal(), datetime(2025,1,1).toordinal()))
# ax5.set_xticklabels(('2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024', '2025'))
# ax5.set_xlim(datetime(2014,12,4).toordinal(), datetime(2025,5,1).toordinal())
# ax5.set_ylim(600, 0)
# ax5.spines[:].set_linewidth(2)
# ax5.tick_params(width=2, top=True, right=True, direction='in')
# ax5.set_title('Trinidad Head Averaged Over Inshore 200km', pad=10)
# cbar1 = plt.colorbar(scat5, shrink=0.5, location='right', pad=0.015)
# cbar1.outline.set_linewidth(2)
# cbar1.set_label(label=r'($\degree$C)', rotation=0, labelpad=10)

# scat6 = ax6.scatter(salt_Xgrid, salt_Ygrid, s=2)
# deployment2_nov_14 = ax6.hlines(y=570, xmin=datetime(2014,12,4).toordinal(), xmax=datetime(2015,3,9).toordinal(), color='k')
# deployment2_sep_15 = ax6.hlines(y=570, xmin=datetime(2015,9,17).toordinal(), xmax=datetime(2016,5,16).toordinal(), color='k')
# deployment2_may_16 = ax6.hlines(y=570, xmin=datetime(2016,5,23).toordinal(), xmax=datetime(2016,10,21).toordinal(), color='k')
# deployment2_oct_16 = ax6.hlines(y=570, xmin=datetime(2016,10,21).toordinal(), xmax=datetime(2017,6,5).toordinal(), color='k')
# deployment2_jun_17 = ax6.hlines(y=570, xmin=datetime(2017,6,5).toordinal(), xmax=datetime(2017,11,6).toordinal(), color='k')
# deployment2_apr_18 = ax6.hlines(y=570, xmin=datetime(2018,4,17).toordinal(), xmax=datetime(2018,10,2).toordinal(), color='k')
# deployment2_nov_18 = ax6.hlines(y=570, xmin=datetime(2018,11,7).toordinal(), xmax=datetime(2019,4,9).toordinal(), color='k')
# deployment2_apr_19 = ax6.hlines(y=570, xmin=datetime(2019,4,9).toordinal(), xmax=datetime(2019,8,19).toordinal(), color='k')
# deployment2_sep_19 = ax6.hlines(y=570, xmin=datetime(2019,9,16).toordinal(), xmax=datetime(2020,3,19).toordinal(), color='k')
# deployment2_sep_20 = ax6.hlines(y=570, xmin=datetime(2020,9,16).toordinal(), xmax=datetime(2021,2,6).toordinal(), color='k')
# deployment2_nov_21 = ax6.hlines(y=570, xmin=datetime(2021,11,12).toordinal(), xmax=datetime(2022,6,16).toordinal(), color='k')
# deployment2_jul_22 = ax6.hlines(y=570, xmin=datetime(2022,7,29).toordinal(), xmax=datetime(2023,1,26).toordinal(), color='k')
# deployment2_jan_23 = ax6.hlines(y=570, xmin=datetime(2023,1,26).toordinal(), xmax=datetime(2023,8,14).toordinal(), color='k')
# deployment2_oct_23 = ax6.hlines(y=570, xmin=datetime(2023,10,13).toordinal(), xmax=datetime(2024,4,12).toordinal(), color='k')
# deployment2_apr_24 = ax6.hlines(y=570, xmin=datetime(2024,4,12).toordinal(), xmax=datetime(2024,8,9).toordinal(), color='k')
# deployment2_oct_24 = ax6.hlines(y=570, xmin=datetime(2024,10,21).toordinal(), xmax=datetime(2024,12,4).toordinal(), color='k')
# deployment2_mar_25 = ax6.hlines(y=570, xmin=datetime(2025,3,21).toordinal(), xmax=salt_Xgrid.max(), color='k')
# # ax6.clabel(lines2, lines2.levels, inline=True, fontsize=10)
# ax6.invert_yaxis()
# ax6.set_ylabel('Depth (m)')
# ax6.text(datetime(2022,11,1).toordinal(), 530, 'Salinity Anomaly', fontsize='large')
# ax6.set_xlabel('Year')
# ax6.set_yticks((0, 200, 400, 600))
# ax6.set_xticks((datetime(2015,1,1).toordinal(), datetime(2016,1,1).toordinal(), datetime(2017,1,1).toordinal(), datetime(2018,1,1).toordinal(), datetime(2019,1,1).toordinal(), datetime(2020,1,1).toordinal(), datetime(2021,1,1).toordinal(),
#                datetime(2022,1,1).toordinal(), datetime(2023,1,1).toordinal(), datetime(2024,1,1).toordinal(), datetime(2025,1,1).toordinal()))
# ax6.set_xticklabels(('2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024', '2025'))
# ax6.set_xlim(datetime(2014,12,4).toordinal(), datetime(2025,5,1).toordinal())
# ax6.set_ylim(600, 0)
# ax6.spines[:].set_linewidth(2)
# ax6.tick_params(width=2, top=True, right=True, direction='in')
# # ax6.set_title('Salinity Anomaly', pad=10)
# cbar2 = plt.colorbar(scat6, shrink=0.5, location='right', pad=0.015)
# cbar2.outline.set_linewidth(2)
# cbar2.set_label(label=r'(PSU)', rotation=0, labelpad=10)
# plt.tight_layout()

# Plot the figure: Temperature Anomaly Indices
print(f'\nPlotting t_anom_indices_MOCI_{timestamp}.png...')
fig, ax = plt.subplots(1,1, figsize=(18,7), dpi=300)

ax2 = ax.twinx()

oni_plot = ax.plot(scti_time, oni, label='Oceanic Nino index (NOAA)', c='k')
scti_plot = ax.plot(scti_time, scti, label='So Cal T index (Rudnick)', c='blue')
thi_plot = ax.plot(thi_time, fifty_meters, label='Trinidad Head index', c='magenta')
moci_plot = ax2.plot(norcal_time, norcal_moci, label='California Multivariate Ocean Climate Indicator', c='green')

ax.set_xticks((datetime(2008,1,1).toordinal(), datetime(2010,1,1).toordinal(), datetime(2012,1,1).toordinal(), datetime(2014,1,1).toordinal(), datetime(2016,1,1).toordinal(), datetime(2018,1,1).toordinal(), datetime(2020,1,1).toordinal(),
               datetime(2022,1,1).toordinal(), datetime(2024,1,1).toordinal(), datetime(2025,1,1).toordinal()))
# ax.set_yticks((-2, -1, 0, 1, 2, 3, 4))
ax.set_xticklabels(('2008', '2010', '2012', '2014', '2016', '2018', '2020', '2022', '2024', '2025'), fontsize='x-large')
# ax.set_yticklabels((-2, -1, 0, 1, 2, 3, 4), fontsize='x-large')
ax.set_ylabel(r'Temperature Anomaly ($\degree$C)', fontsize='x-large')
ax2.set_ylabel(r'MOCI Index', fontsize='x-large')
ax2.set_ylim(-8, 15)
ax2.set_yticks([-4, 0, 4, 8, 12])
ax2.set_yticklabels(['-4', '0', '4', '8', '12'])
ax.set_xlabel('Year', fontsize='x-large')
ax.set_xlim(datetime(2006,6,1).toordinal(), datetime(2025,6,1).toordinal())
ax.spines[:].set_linewidth(2)
ax.tick_params(width=2, top=True, right=False, direction='in')
ax2.spines[:].set_linewidth(2)
ax2.tick_params(width=2, top=True, right=True, direction='in')
plt.title('Temperature Anomaly Indices', pad=15, fontsize='x-large')
lns = oni_plot + scti_plot + thi_plot + moci_plot
labs = [l.get_label() for l in lns]
ax.legend(lns, labs, loc=2, frameon=False, fontsize='x-large', labelcolor='linecolor')
plt.axvspan(datetime(2006,6,1).toordinal(), datetime(2025,6,1).toordinal(), ymin=0, ymax=0.35, alpha=0.15, color='gray')
plt.savefig(f'C:/Users/marqjace/OneDrive - Oregon State University/Desktop/Python/TH-Line_timeseries/figures/t_anom_indices_MOCI_{timestamp}.png')


# Plot the figure: Temperature Anomaly Indices
print(f'\nPlotting t_anom_indices_{timestamp}.png...')
fig, ax = plt.subplots(1,1, figsize=(18,7), dpi=300)

ax2 = ax.twinx()

oni_plot = ax.plot(scti_time, oni, label='Oceanic Nino index (NOAA)', c='k')
scti_plot = ax.plot(scti_time, scti, label='So Cal T index (Rudnick)', c='blue')
thi_plot = ax.plot(thi_time, fifty_meters, label='Trinidad Head index', c='magenta')
# moci_plot = ax2.plot(norcal_time, norcal_moci, label='California Multivariate Ocean Climate Indicator', c='green')

ax.set_xticks((datetime(2008,1,1).toordinal(), datetime(2010,1,1).toordinal(), datetime(2012,1,1).toordinal(), datetime(2014,1,1).toordinal(), datetime(2016,1,1).toordinal(), datetime(2018,1,1).toordinal(), datetime(2020,1,1).toordinal(),
               datetime(2022,1,1).toordinal(), datetime(2024,1,1).toordinal(), datetime(2025,1,1).toordinal()))
# ax.set_yticks((-2, -1, 0, 1, 2, 3, 4))
ax.set_xticklabels(('2008', '2010', '2012', '2014', '2016', '2018', '2020', '2022', '2024', '2025'), fontsize='x-large')
# ax.set_yticklabels((-2, -1, 0, 1, 2, 3, 4), fontsize='x-large')
ax.set_ylabel(r'Temperature Anomaly ($\degree$C)', fontsize='x-large')
ax2.set_ylabel(r'MOCI Index', fontsize='x-large')
ax2.set_ylim(-8, 15)
ax2.set_yticks([-4, 0, 4, 8, 12])
ax2.set_yticklabels(['-4', '0', '4', '8', '12'])
ax.set_xlabel('Year', fontsize='x-large')
ax.set_xlim(datetime(2006,6,1).toordinal(), datetime(2025,6,1).toordinal())
ax.spines[:].set_linewidth(2)
ax.tick_params(width=2, top=True, right=False, direction='in')
ax2.spines[:].set_linewidth(2)
ax2.tick_params(width=2, top=True, right=True, direction='in')
plt.title('Temperature Anomaly Indices', pad=15, fontsize='x-large')
lns = oni_plot + scti_plot + thi_plot
labs = [l.get_label() for l in lns]
ax.legend(lns, labs, loc=2, frameon=False, fontsize='x-large', labelcolor='linecolor')
plt.axvspan(datetime(2006,6,1).toordinal(), datetime(2025,6,1).toordinal(), ymin=0, ymax=0.35, alpha=0.15, color='gray')
plt.savefig(f"C:/Users/marqjace/OneDrive - Oregon State University/Desktop/Python/TH-Line_timeseries/figures/t_anom_indices_{timestamp}.png")
