#!/usr/bin/env python
# coding: utf-8

import numpy as np
import xarray as xr
from scipy.interpolate import griddata
from datetime import datetime

def transect(filepath):
    # Temp & Salt Grid
    xn, yn = 36, 200
    xmin, xmax = -126.625, -124.375
    ymin, ymax = 0, 1000
    xgrid = np.linspace(xmin, xmax, xn)
    ygrid = np.linspace(ymin, ymax, yn)
    Xgrid, Ygrid = np.meshgrid(xgrid, ygrid)
    
    # Load dataset
    ds = xr.open_dataset(filepath, decode_times=False)
    depth = ds.depth
    lon = ds.longitude
    temp = ds.temp_raw
    salt = ds.salt_raw
    gmt_epoch_times = ds.time_raw.values
    time = [datetime.utcfromtimestamp(t) for t in gmt_epoch_times]

    # Debugging: Print shapes and types of loaded data
    print(f"File: {filepath}")
    print(f"depth shape: {depth.shape}, type: {type(depth)}")
    print(f"lon shape: {lon.shape}, type: {type(lon)}")
    print(f"temp shape: {temp.shape}, type: {type(temp)}")
    print(f"salt shape: {salt.shape}, type: {type(salt)}")
    print(f"time length: {len(time)}, type: {type(time)}")

    # Interpolate using "linear" method
    temp_interp = griddata((lon, depth), temp, (Xgrid, Ygrid), method='linear')
    salt_interp = griddata((lon, depth), salt, (Xgrid, Ygrid), method='linear')

    # Debugging: Print shapes of interpolated data
    print(f"temp_interp shape: {temp_interp.shape}, type: {type(temp_interp)}")
    print(f"salt_interp shape: {salt_interp.shape}, type: {type(salt_interp)}")

    return {
        'lon': lon,
        'depth': depth,
        'temp': temp,
        'salt': salt,
        'time': time,
        'temp_interp': temp_interp,
        'salt_interp': salt_interp,
    }

def process_all_transects(filepaths):
    results = {}
    for i, filepath in enumerate(filepaths, start=1):
        results[i] = transect(filepath)
    return results

# Example usage for multiple months
filepaths_deployments = [
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

# Process all transects
results = process_all_transects(filepaths_deployments)

# Extract temperature and salinity interpolations
temp_data = {f'temp_{i}': results[i]['temp_interp'] for i in results}
salt_data = {f'salt_{i}': results[i]['salt_interp'] for i in results}

# Extract time and longitude data
time_data = {f'time_{i}': results[i]['time'] for i in results}
lon_data = {f'lon_{i}': results[i]['lon'] for i in results}