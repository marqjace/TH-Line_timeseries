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
import transects_func_new


# Open WOA Climatology Data
# Data Access Here: https://www.ncei.noaa.gov/access/world-ocean-atlas-2018/bin/woa18.pl

# WOA Temperature
ds_z_t_an = {
    'jan': woa_temp.woa_temp_jan,
    'feb': woa_temp.woa_temp_feb,
    'mar': woa_temp.woa_temp_mar,
    'apr': woa_temp.woa_temp_apr,
    'may': woa_temp.woa_temp_may,
    'jun': woa_temp.woa_temp_jun,
    'jul': woa_temp.woa_temp_jul,
    'aug': woa_temp.woa_temp_aug,
    'sep': woa_temp.woa_temp_sep,
    'oct': woa_temp.woa_temp_oct,
    'nov': woa_temp.woa_temp_nov,
    'dec': woa_temp.woa_temp_dec
}

# WOA Salinity
ds_z_s_an = {
    'jan': woa_salt.woa_salt_jan,
    'feb': woa_salt.woa_salt_feb,
    'mar': woa_salt.woa_salt_mar,
    'apr': woa_salt.woa_salt_apr,
    'may': woa_salt.woa_salt_may,
    'jun': woa_salt.woa_salt_jun,
    'jul': woa_salt.woa_salt_jul,
    'aug': woa_salt.woa_salt_aug,
    'sep': woa_salt.woa_salt_sep,
    'oct': woa_salt.woa_salt_oct,
    'nov': woa_salt.woa_salt_nov,
    'dec': woa_salt.woa_salt_dec
}


# SCTI / ONI Data
# Data Access Here: https://spraydata.ucsd.edu/products/socal-index/

dat = xr.open_dataset(r'C:/Users/marqjace/TH_line/scti_oni/socal_index_monthly_v1_8571_f367_229e_U1723054143245.nc', decode_times=False)

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
dat2 = pd.read_csv(r'C:/Users/marqjace/TH_line/california_moci/california_moci.csv')
dat2 = dat2.drop(['FID', 'Year', 'Season', 'months', 'geometry'], axis=1)
dat2 = dat2.set_index(['time'])

# Norcal Only
norcal = dat2.where(dat2['location'] == 'North California (38-42N)')

norcal_time = norcal.index
norcal_moci = norcal['moci']

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


def extract_month(key):
    """Extract the month number and map it to abbreviation."""

    month_map = {
    '1': 'jan', '2': 'feb', '3': 'mar', '4': 'apr',
    '5': 'may', '6': 'jun', '7': 'jul', '8': 'aug',
    '9': 'sep', '10': 'oct', '11': 'nov', '12': 'dec'
    }
    
    # Split by underscore and take the first part
    month_number = key.split('_')[0]
    # Map to month abbreviation
    return month_map.get(month_number, None)

# Filepaths of individual transects
filepaths = [

    # Nov 2014 Deployment
    r'C:/Users/marqjace/TH_line/deployments/nov_2014/transect1/12_14_a_merged.nc',
    r'C:/Users/marqjace/TH_line/deployments/nov_2014/transect2/12_14_b_merged.nc',
    r'C:/Users/marqjace/TH_line/deployments/nov_2014/transect3/1_15_merged.nc',
    r'C:/Users/marqjace/TH_line/deployments/nov_2014/transect4/2_15_a_merged.nc',
    r'C:/Users/marqjace/TH_line/deployments/nov_2014/transect5/2_15_b_merged.nc',

    # Mar 2015 Deployment
    r'C:/Users/marqjace/TH_line/deployments/mar_2015/transect1/3_15_merged.nc',
    r'C:/Users/marqjace/TH_line/deployments/mar_2015/transect2/4_15_merged.nc',
    r'C:/Users/marqjace/TH_line/deployments/mar_2015/transect3/5_15_merged.nc',
    r'C:/Users/marqjace/TH_line/deployments/mar_2015/transect4/6_15_merged.nc',
    r'C:/Users/marqjace/TH_line/deployments/mar_2015/transect5/7_15_merged.nc',
    r'C:/Users/marqjace/TH_line/deployments/mar_2015/transect6/8_15_merged.nc',
    r'C:/Users/marqjace/TH_line/deployments/mar_2015/transect7/9_15_merged.nc',

    # Sep 2015 Deployment
    r'C:/Users/marqjace/TH_line/deployments/sep_2015/transect1/10_15_merged.nc',
    r'C:/Users/marqjace/TH_line/deployments/sep_2015/transect2/11_15_merged.nc',
    r'C:/Users/marqjace/TH_line/deployments/sep_2015/transect3/12_15_merged.nc',
    r'C:/Users/marqjace/TH_line/deployments/sep_2015/transect4/1_16_merged.nc',
    r'C:/Users/marqjace/TH_line/deployments/sep_2015/transect5/3_16_merged.nc',
    r'C:/Users/marqjace/TH_line/deployments/sep_2015/transect6/4_16_merged.nc',
    r'C:/Users/marqjace/TH_line/deployments/sep_2015/transect7/5_16_merged.nc',

    # May 2016 Deployment
    r'C:/Users/marqjace/TH_line/deployments/may_2016/transect1/6_16_merged.nc',
    r'C:/Users/marqjace/TH_line/deployments/may_2016/transect2/7_16_merged.nc',
    r'C:/Users/marqjace/TH_line/deployments/may_2016/transect3/8_16_merged.nc',
    r'C:/Users/marqjace/TH_line/deployments/may_2016/transect4/9_16_a_merged.nc',
    r'C:/Users/marqjace/TH_line/deployments/may_2016/transect5/9_16_b_merged.nc',
    r'C:/Users/marqjace/TH_line/deployments/may_2016/transect6/10_16_a_merged.nc',
    r'C:/Users/marqjace/TH_line/deployments/may_2016/transect7/10_16_b_merged.nc',

    # Oct 2016 Deployment
    r'C:/Users/marqjace/TH_line/deployments/oct_2016/transect1/11_16_merged.nc',
    r'C:/Users/marqjace/TH_line/deployments/oct_2016/transect2/12_16_merged.nc',
    r'C:/Users/marqjace/TH_line/deployments/oct_2016/transect3/1_17_merged.nc',
    r'C:/Users/marqjace/TH_line/deployments/oct_2016/transect4/2_17_merged.nc',
    r'C:/Users/marqjace/TH_line/deployments/oct_2016/transect5/3_17_merged.nc',
    r'C:/Users/marqjace/TH_line/deployments/oct_2016/transect6/4_17_a_merged.nc',
    r'C:/Users/marqjace/TH_line/deployments/oct_2016/transect7/4_17_b_merged.nc',
    r'C:/Users/marqjace/TH_line/deployments/oct_2016/transect8/5_17_merged.nc',

    # Jun 2017 Deployment
    r'C:/Users/marqjace/TH_line/deployments/jun_2017/transect1/6_17_merged.nc',
    r'C:/Users/marqjace/TH_line/deployments/jun_2017/transect2/7_17_merged.nc',
    r'C:/Users/marqjace/TH_line/deployments/jun_2017/transect3/8_17_merged.nc',
    r'C:/Users/marqjace/TH_line/deployments/jun_2017/transect4/9_17_merged.nc',
    r'C:/Users/marqjace/TH_line/deployments/jun_2017/transect5/10_17_a_merged.nc',
    r'C:/Users/marqjace/TH_line/deployments/jun_2017/transect6/10_17_b_merged.nc',
    r'C:/Users/marqjace/TH_line/deployments/jun_2017/transect7/11_17_merged.nc',

    # Apr 2018 Deployment
    r'C:/Users/marqjace/TH_line/deployments/apr_2018/transect1/4_18_merged.nc',
    r'C:/Users/marqjace/TH_line/deployments/apr_2018/transect2/5_18_merged.nc',
    r'C:/Users/marqjace/TH_line/deployments/apr_2018/transect3/6_18_merged.nc',
    r'C:/Users/marqjace/TH_line/deployments/apr_2018/transect4/8_18_merged.nc',
    r'C:/Users/marqjace/TH_line/deployments/apr_2018/transect5/9_18_a_merged.nc',
    r'C:/Users/marqjace/TH_line/deployments/apr_2018/transect6/9_18_b_merged.nc',

    # Nov 2018 Deployment
    r'C:/Users/marqjace/TH_line/deployments/nov_2018/transect1/11_18_merged.nc',
    r'C:/Users/marqjace/TH_line/deployments/nov_2018/transect2/12_18_merged.nc',
    r'C:/Users/marqjace/TH_line/deployments/nov_2018/transect3/1_19_merged.nc',
    r'C:/Users/marqjace/TH_line/deployments/nov_2018/transect4/2_19_merged.nc',
    r'C:/Users/marqjace/TH_line/deployments/nov_2018/transect5/3_19_a_merged.nc',
    r'C:/Users/marqjace/TH_line/deployments/nov_2018/transect6/3_19_b_merged.nc',
    r'C:/Users/marqjace/TH_line/deployments/nov_2018/transect7/4_19_a_merged.nc',

    # Apr 2019 Deployment
    r'C:/Users/marqjace/TH_line/deployments/apr_2019/transect1/4_19_b_merged.nc',
    r'C:/Users/marqjace/TH_line/deployments/apr_2019/transect2/6_19_merged.nc',
    r'C:/Users/marqjace/TH_line/deployments/apr_2019/transect3/7_19_merged.nc',
    r'C:/Users/marqjace/TH_line/deployments/apr_2019/transect4/8_19_merged.nc',

    # Sep 2019 Deployment
    r'C:/Users/marqjace/TH_line/deployments/sep_2019/transect1/9_19_merged.nc',
    r'C:/Users/marqjace/TH_line/deployments/sep_2019/transect2/10_19_merged.nc',
    r'C:/Users/marqjace/TH_line/deployments/sep_2019/transect3/11_19_merged.nc',
    r'C:/Users/marqjace/TH_line/deployments/sep_2019/transect4/12_19_merged.nc',
    r'C:/Users/marqjace/TH_line/deployments/sep_2019/transect5/1_20_merged.nc',
    r'C:/Users/marqjace/TH_line/deployments/sep_2019/transect6/2_20_merged.nc',
    r'C:/Users/marqjace/TH_line/deployments/sep_2019/transect7/3_20_a_merged.nc',
    r'C:/Users/marqjace/TH_line/deployments/sep_2019/transect8/3_20_b_merged.nc',

    # Sep 2020 Deployment
    r'C:/Users/marqjace/TH_line/deployments/sep_2020/transect1/9_20_merged.nc',
    r'C:/Users/marqjace/TH_line/deployments/sep_2020/transect2/10_20_merged.nc',
    r'C:/Users/marqjace/TH_line/deployments/sep_2020/transect3/11_20_merged.nc',
    r'C:/Users/marqjace/TH_line/deployments/sep_2020/transect4/12_20_merged.nc',
    r'C:/Users/marqjace/TH_line/deployments/sep_2020/transect5/1_21_merged.nc',
    r'C:/Users/marqjace/TH_line/deployments/sep_2020/transect6/2_21_merged.nc',

    # Nov 2021 Deployment
    r'C:/Users/marqjace/TH_line/deployments/nov_2021/transect1/11_21_merged.nc',
    r'C:/Users/marqjace/TH_line/deployments/nov_2021/transect2/12_21_merged.nc',
    r'C:/Users/marqjace/TH_line/deployments/nov_2021/transect3/1_22_merged.nc',
    r'C:/Users/marqjace/TH_line/deployments/nov_2021/transect4/2_22_merged.nc',
    r'C:/Users/marqjace/TH_line/deployments/nov_2021/transect5/3_22_merged.nc',
    r'C:/Users/marqjace/TH_line/deployments/nov_2021/transect6/4_22_merged.nc',
    r'C:/Users/marqjace/TH_line/deployments/nov_2021/transect7/5_22_merged.nc',
    r'C:/Users/marqjace/TH_line/deployments/nov_2021/transect8/6_22_merged.nc',

    # Jul 2022 Deployment
    r'C:/Users/marqjace/TH_line/deployments/jul_2022/transect1/8_22_merged.nc',
    r'C:/Users/marqjace/TH_line/deployments/jul_2022/transect2/9_22_merged.nc',
    r'C:/Users/marqjace/TH_line/deployments/jul_2022/transect3/10_22_merged.nc',
    r'C:/Users/marqjace/TH_line/deployments/jul_2022/transect4/11_22_merged.nc',
    r'C:/Users/marqjace/TH_line/deployments/jul_2022/transect5/12_22_merged.nc',
    r'C:/Users/marqjace/TH_line/deployments/jul_2022/transect6/1_23_merged.nc',

    # Jan 2023 Deployment
    r'C:/Users/marqjace/TH_line/deployments/jan_2023/transect1/2_23_merged.nc',
    r'C:/Users/marqjace/TH_line/deployments/jan_2023/transect2/3_23_a_merged.nc',
    r'C:/Users/marqjace/TH_line/deployments/jan_2023/transect3/3_23_b_merged.nc',
    r'C:/Users/marqjace/TH_line/deployments/jan_2023/transect4/4_23_merged.nc',
    r'C:/Users/marqjace/TH_line/deployments/jan_2023/transect5/5_23_merged.nc',
    r'C:/Users/marqjace/TH_line/deployments/jan_2023/transect6/6_23_merged.nc',
    r'C:/Users/marqjace/TH_line/deployments/jan_2023/transect7/7_23_merged.nc',
    r'C:/Users/marqjace/TH_line/deployments/jan_2023/transect8/8_23_merged.nc',

    # Oct 2023 Deployment
    r'C:/Users/marqjace/TH_line/deployments/oct_2023/transect1/10_23_merged.nc',
    r'C:/Users/marqjace/TH_line/deployments/oct_2023/transect2/11_23_merged.nc',
    r'C:/Users/marqjace/TH_line/deployments/oct_2023/transect3/12_23_merged.nc',
    r'C:/Users/marqjace/TH_line/deployments/oct_2023/transect4/1_24_merged.nc',
    r'C:/Users/marqjace/TH_line/deployments/oct_2023/transect5/2_24_a_merged.nc',
    r'C:/Users/marqjace/TH_line/deployments/oct_2023/transect6/2_24_b_merged.nc',
    r'C:/Users/marqjace/TH_line/deployments/oct_2023/transect7/3_24_merged.nc',

    # Apr 2024 Deployment
    r'C:/Users/marqjace/TH_line/deployments/apr_2024/transect1/4_24_merged.nc',
    r'C:/Users/marqjace/TH_line/deployments/apr_2024/transect2/5_24_merged.nc',
    r'C:/Users/marqjace/TH_line/deployments/apr_2024/transect3/6_24_merged.nc',
    r'C:/Users/marqjace/TH_line/deployments/apr_2024/transect4/7_24_merged.nc',
    r'C:/Users/marqjace/TH_line/deployments/apr_2024/transect5/8_24_a_merged.nc',
    r'C:/Users/marqjace/TH_line/deployments/apr_2024/transect6/8_24_b_merged.nc',

    # Oct 2024 Deployment
    r'C:/Users/marqjace/TH_line/deployments/oct_2024/transect1/10_24_merged.nc',
    r'C:/Users/marqjace/TH_line/deployments/oct_2024/transect2/11_24_merged.nc',
    r'C:/Users/marqjace/TH_line/deployments/mar_2025/transect1/3_25_merged.nc',
]

# Process the transects (grids them and puts them into a dictionary)
transects_func_new.batch_process(filepaths)

# Interpolated & Gridded Temperature
temp_12_14_a = transects_func_new.temperature_data['12_14_a'],
temp_12_14_b = transects_func_new.temperature_data['12_14_b'],
temp_1_15 = transects_func_new.temperature_data['1_15'],
temp_2_15_a = transects_func_new.temperature_data['2_15_a'],
temp_2_15_b = transects_func_new.temperature_data['2_15_b'],
temp_3_15 = transects_func_new.temperature_data['1_15'],
temp_4_15 = transects_func_new.temperature_data['1_15'],
temp_5_15 = transects_func_new.temperature_data['1_15'],
temp_6_15 = transects_func_new.temperature_data,
temp_7_15 = transects_func_new.temperature_data,
temp_8_15 = transects_func_new.temperature_data,
temp_9_15 = transects_func_new.temperature_data,
temp_10_15 = transects_func_new.temperature_data,
temp_11_15 = transects_func_new.temperature_data,
temp_12_15 = transects_func_new.temperature_data,
temp_1_16 = transects_func_new.temperature_data,
temp_3_16 = transects_func_new.temperature_data,
temp_4_16 = transects_func_new.temperature_data,
temp_5_16 = transects_func_new.temperature_data
temp_6_16 = transects_func_new.temperature_data,
temp_7_16 = transects_func_new.temperature_data,
temp_8_16 = transects_func_new.temperature_data,
temp_9_16_a = transects_func_new.temperature_data,
temp_9_16_b = transects_func_new.temperature_data,
temp_10_16_a = transects_func_new.temperature_data,
temp_10_16_b = transects_func_new.temperature_data,
temp_11_16 = transects_func_new.temperature_data,
temp_12_16 = transects_func_new.temperature_data,
temp_1_17 = transects_func_new.temperature_data,
temp_2_17 = transects_func_new.temperature_data,
temp_3_17 = transects_func_new.temperature_data,
temp_4_17_a = transects_func_new.temperature_data,
temp_4_17_b = transects_func_new.temperature_data,
temp_5_17 = transects_func_new.temperature_data,
temp_6_17 = transects_func_new.temperature_data,
temp_7_17 = transects_func_new.temperature_data,
temp_8_17 = transects_func_new.temperature_data,
temp_9_17 = transects_func_new.temperature_data,
temp_10_17_a = transects_func_new.temperature_data,
temp_10_17_b = transects_func_new.temperature_data,
temp_11_17 = transects_func_new.temperature_data,
temp_4_18 = transects_func_new.temperature_data,
temp_5_18 = transects_func_new.temperature_data,
temp_6_18 = transects_func_new.temperature_data,
temp_8_18 = transects_func_new.temperature_data,
temp_9_18_a = transects_func_new.temperature_data,
temp_9_18_b = transects_func_new.temperature_data,
temp_11_18 = transects_func_new.temperature_data,
temp_12_18 = transects_func_new.temperature_data,
temp_1_19 = transects_func_new.temperature_data,
temp_2_19 = transects_func_new.temperature_data,
temp_3_19_a = transects_func_new.temperature_data,
temp_3_19_b = transects_func_new.temperature_data,
temp_4_19_a = transects_func_new.temperature_data,
temp_4_19_b = transects_func_new.temperature_data,
temp_6_19 = transects_func_new.temperature_data,
temp_7_19 = transects_func_new.temperature_data,
temp_8_19 = transects_func_new.temperature_data,
temp_9_19 = transects_func_new.temperature_data,
temp_10_19 = transects_func_new.temperature_data,
temp_11_19 = transects_func_new.temperature_data,
temp_12_19 = transects_func_new.temperature_data,
temp_1_20 = transects_func_new.temperature_data,
temp_2_20 = transects_func_new.temperature_data,
temp_3_20_a = transects_func_new.temperature_data,
temp_3_20_b = transects_func_new.temperature_data,
temp_9_20 = transects_func_new.temperature_data,
temp_10_20 = transects_func_new.temperature_data,
temp_11_20 = transects_func_new.temperature_data,
temp_12_20 = transects_func_new.temperature_data,
temp_1_21 = transects_func_new.temperature_data,
temp_2_21 = transects_func_new.temperature_data,
temp_11_21 = transects_func_new.temperature_data,
temp_12_21 = transects_func_new.temperature_data,
temp_1_22 = transects_func_new.temperature_data,
temp_2_22 = transects_func_new.temperature_data,
temp_3_22 = transects_func_new.temperature_data,
temp_4_22 = transects_func_new.temperature_data,
temp_5_22 = transects_func_new.temperature_data,
temp_6_22 = transects_func_new.temperature_data,
temp_8_22 = transects_func_new.temperature_data,
temp_9_22 = transects_func_new.temperature_data,
temp_10_22 = transects_func_new.temperature_data,
temp_11_22 = transects_func_new.temperature_data,
temp_12_22 = transects_func_new.temperature_data,
temp_1_23 = transects_func_new.temperature_data,
temp_2_23 = transects_func_new.temperature_data,
temp_3_23_a = transects_func_new.temperature_data,
temp_3_23_b = transects_func_new.temperature_data,
temp_4_23 = transects_func_new.temperature_data,
temp_5_23 = transects_func_new.temperature_data,
temp_6_23 = transects_func_new.temperature_data,
temp_7_23 = transects_func_new.temperature_data,
temp_8_23 = transects_func_new.temperature_data,
temp_10_23 = transects_func_new.temperature_data,
temp_11_23 = transects_func_new.temperature_data,
temp_12_23 = transects_func_new.temperature_data,
temp_1_24 = transects_func_new.temperature_data,
temp_2_24_a = transects_func_new.temperature_data,
temp_2_24_b = transects_func_new.temperature_data,
temp_3_24 = transects_func_new.temperature_data,
temp_4_24 = transects_func_new.temperature_data,
temp_5_24 = transects_func_new.temperature_data,
temp_6_24 = transects_func_new.temperature_data,
temp_7_24 = transects_func_new.temperature_data,
temp_8_24_a = transects_func_new.temperature_data,
temp_8_24_b = transects_func_new.temperature_data,
temp_10_24 = transects_func_new.temperature_data,
temp_11_24 = transects_func_new.temperature_data,
temp_3_25 = transects_func_new.temperature_data,


# print(temp_anomaly)

# # Example of accessing individual transects and their data
# for transect_name, temp_data in temperature.items()=
#     print(temp_data)
    # print(f"Transect: {transect_name}")
    # print(f"Temperature DataArray: {temp_data}")
    # print(f"Temperature values: {temp_data.values}")