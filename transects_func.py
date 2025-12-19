#!/usr/bin/env python
# coding: utf-8

import numpy as np
import xarray as xr
from scipy.interpolate import griddata
from datetime import datetime

def transect(filepath, transect_idx):
    # Temp & Salt Grid

    # Set up new grid (36 points is 2.25 deg longitude for every 5 km, 200 points depth to 1000m is every 5 meters)
    # number of grid points:
    # xn, yn = 50, 200
    xn, yn = 36, 200

    # grid window
    xmin, xmax = -126.625, -124.375
    ymin, ymax = 0, 1000

    # Generate a regular grid to interpolate the data
    xgrid = np.linspace(xmin, xmax, xn)
    ygrid = np.linspace(ymin, ymax, yn)
    Xgrid, Ygrid = np.meshgrid(xgrid, ygrid)
    
    # Load dataset
    ds = xr.open_dataset(filepath, decode_times=False)

   # variable assignment for conveniant access
    depth = ds.depth
    lon = ds.longitude
    temp = ds.temp_raw
    salt = ds.salt_raw
    # Convert time from GMT epoch to datetime
    gmt_epoch_times = ds.time_raw.values  # Extract the raw epoch times as a NumPy array
    time = [datetime.utcfromtimestamp(t) for t in gmt_epoch_times]

    # Interpolate using "linear" method

    temp_interp = griddata(points = (lon, depth),
                values = temp,
                xi = (Xgrid, Ygrid),
                method = 'linear')

    salt_interp = griddata(points = (lon, depth),
                values = salt,
                xi = (Xgrid, Ygrid),
                method = 'linear')
    
    if "salt_corrected" in ds.data_vars:
        salt_corrected = ds.salt_corrected

        salt_corrected_interp = griddata(points = (lon, depth),
                values = salt_corrected,
                xi = (Xgrid, Ygrid),
                method = 'linear')
        
        return {
        'lon': lon,
        'depth': depth,
        'temp': temp,
        'salt': salt,
        'time': time,
        'temp_interp': temp_interp,
        'salt_interp': salt_interp,
        'salt_corrected_interp': salt_corrected_interp,
        # 'temp_interp_hovmoller': temp_interp_hovmoller,
        }
    else:
        return {
        'lon': lon,
        'depth': depth,
        'temp': temp,
        'salt': salt,
        'time': time,
        'temp_interp': temp_interp,
        'salt_interp': salt_interp,
        }

    # # Return variables you want to save
    # return {
    #     'lon': lon,
    #     'depth': depth,
    #     'temp': temp,
    #     'salt': salt,
    #     'time': time,
    #     'temp_interp': temp_interp,
    #     'salt_interp': salt_interp,
    #     # 'temp_interp_hovmoller': temp_interp_hovmoller,
    # }

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

    # Mar 2025 Deployment
    r'C:/Users/marqjace/TH_line/deployments/mar_2025/transect1/corrected/3_25_merged.nc',
    r'C:/Users/marqjace/TH_line/deployments/mar_2025/transect2/corrected/4_25_a_merged.nc',
    r'C:/Users/marqjace/TH_line/deployments/mar_2025/transect3/corrected/4_25_b_merged.nc',
    r'C:/Users/marqjace/TH_line/deployments/mar_2025/transect4/corrected/5_25_merged.nc',
    r'C:/Users/marqjace/TH_line/deployments/mar_2025/transect5/corrected/6_25_a_merged.nc',
    r'C:/Users/marqjace/TH_line/deployments/mar_2025/transect6/corrected/6_25_b_merged.nc',
    r'C:/Users/marqjace/TH_line/deployments/mar_2025/transect7/corrected/7_25_merged.nc',
    r'C:/Users/marqjace/TH_line/deployments/mar_2025/transect8/corrected/8_25_a_merged.nc',
    r'C:/Users/marqjace/TH_line/deployments/mar_2025/transect9/corrected/9_25_a_merged.nc',
    r'C:/Users/marqjace/TH_line/deployments/mar_2025/transect10/corrected/9_25_b_merged.nc',
    r'C:/Users/marqjace/TH_line/deployments/mar_2025/transect11/corrected/10_25_a_merged.nc',
    r'C:/Users/marqjace/TH_line/deployments/mar_2025/transect12/corrected/10_25_b_merged.nc',

    # Nov 2025 Deployment
    r'C:/Users/marqjace/TH_line/deployments/nov_2025/transect1/11_25_merged.nc',
]

# Dictionary to store the results
results = {}

for i, filepath in enumerate(filepaths_deployments, start=1):
    print(f'Processing {filepath}...')
    result = transect(filepath, transect_idx=i)
    results[i] = result  # Store the result by month index

# Now the 'results' dictionary contains all the variables for each month.

# Temperature
temp_12_14_a = results[1]['temp_interp']
temp_12_14_b = results[2]['temp_interp']
temp_1_15 = results[3]['temp_interp']
temp_2_15_a = results[4]['temp_interp']
temp_2_15_b = results[5]['temp_interp']
temp_3_15 = results[6]['temp_interp']
temp_4_15 = results[7]['temp_interp']
temp_5_15 = results[8]['temp_interp']
temp_6_15 = results[9]['temp_interp']
temp_7_15 = results[10]['temp_interp']
temp_8_15 = results[11]['temp_interp']
temp_9_15 = results[12]['temp_interp']
temp_10_15 = results[13]['temp_interp']
temp_11_15 = results[14]['temp_interp']
temp_12_15 = results[15]['temp_interp']
temp_1_16 = results[16]['temp_interp']
temp_3_16 = results[17]['temp_interp']
temp_4_16 = results[18]['temp_interp']
temp_5_16 = results[19]['temp_interp']
temp_6_16 = results[20]['temp_interp']
temp_7_16 = results[21]['temp_interp']
temp_8_16 = results[22]['temp_interp']
temp_9_16_a = results[23]['temp_interp']
temp_9_16_b = results[24]['temp_interp']
temp_10_16_a = results[25]['temp_interp']
temp_10_16_b = results[26]['temp_interp']
temp_11_16 = results[27]['temp_interp']
temp_12_16 = results[28]['temp_interp']
temp_1_17 = results[29]['temp_interp']
temp_2_17 = results[30]['temp_interp']
temp_3_17 = results[31]['temp_interp']
temp_4_17_a = results[32]['temp_interp']
temp_4_17_b = results[33]['temp_interp']
temp_5_17 = results[34]['temp_interp']
temp_6_17 = results[35]['temp_interp']
temp_7_17 = results[36]['temp_interp']
temp_8_17 = results[37]['temp_interp']
temp_9_17 = results[38]['temp_interp']
temp_10_17_a = results[39]['temp_interp']
temp_10_17_b = results[40]['temp_interp']
temp_11_17 = results[41]['temp_interp']
temp_4_18 = results[42]['temp_interp']
temp_5_18 = results[43]['temp_interp']
temp_6_18 = results[44]['temp_interp']
temp_8_18 = results[45]['temp_interp']
temp_9_18_a = results[46]['temp_interp']
temp_9_18_b = results[47]['temp_interp']
temp_11_18 = results[48]['temp_interp']
temp_12_18 = results[49]['temp_interp']
temp_1_19 = results[50]['temp_interp']
temp_2_19 = results[51]['temp_interp']
temp_3_19_a = results[52]['temp_interp']
temp_3_19_b = results[53]['temp_interp']
temp_4_19_a = results[54]['temp_interp']
temp_4_19_b = results[55]['temp_interp']
temp_6_19 = results[56]['temp_interp']
temp_7_19 = results[57]['temp_interp']
temp_8_19 = results[58]['temp_interp']
temp_9_19 = results[59]['temp_interp']
temp_10_19 = results[60]['temp_interp']
temp_11_19 = results[61]['temp_interp']
temp_12_19 = results[62]['temp_interp']
temp_1_20 = results[63]['temp_interp']
temp_2_20 = results[64]['temp_interp']
temp_3_20_a = results[65]['temp_interp']
temp_3_20_b = results[66]['temp_interp']
temp_9_20 = results[67]['temp_interp']
temp_10_20 = results[68]['temp_interp']
temp_11_20 = results[69]['temp_interp']
temp_12_20 = results[70]['temp_interp']
temp_1_21 = results[71]['temp_interp']
temp_2_21 = results[72]['temp_interp']
temp_11_21 = results[73]['temp_interp']
temp_12_21 = results[74]['temp_interp']
temp_1_22 = results[75]['temp_interp']
temp_2_22 = results[76]['temp_interp']
temp_3_22 = results[77]['temp_interp']
temp_4_22 = results[78]['temp_interp']
temp_5_22 = results[79]['temp_interp']
temp_6_22 = results[80]['temp_interp']
temp_8_22 = results[81]['temp_interp']
temp_9_22 = results[82]['temp_interp']
temp_10_22 = results[83]['temp_interp']
temp_11_22 = results[84]['temp_interp']
temp_12_22 = results[85]['temp_interp']
temp_1_23 = results[86]['temp_interp']
temp_2_23 = results[87]['temp_interp']
temp_3_23_a = results[88]['temp_interp']
temp_3_23_b = results[89]['temp_interp']
temp_4_23 = results[90]['temp_interp']
temp_5_23 = results[91]['temp_interp']
temp_6_23 = results[92]['temp_interp']
temp_7_23 = results[93]['temp_interp']
temp_8_23 = results[94]['temp_interp']
temp_10_23 = results[95]['temp_interp']
temp_11_23 = results[96]['temp_interp']
temp_12_23 = results[97]['temp_interp']
temp_1_24= results[98]['temp_interp']
temp_2_24_a= results[99]['temp_interp']
temp_2_24_b= results[100]['temp_interp']
temp_3_24= results[101]['temp_interp']
temp_4_24= results[102]['temp_interp']
temp_5_24= results[103]['temp_interp']
temp_6_24= results[104]['temp_interp']
temp_7_24= results[105]['temp_interp']
temp_8_24_a= results[106]['temp_interp']
temp_8_24_b= results[107]['temp_interp']
temp_10_24= results[108]['temp_interp']
temp_11_24= results[109]['temp_interp']
temp_3_25= results[110]['temp_interp']
temp_4_25_a= results[111]['temp_interp']
temp_4_25_b= results[112]['temp_interp']
temp_5_25 = results[113]['temp_interp']
temp_6_25_a = results[114]['temp_interp']
temp_6_25_b = results[115]['temp_interp']
temp_7_25 = results[116]['temp_interp']
temp_8_25_a = results[117]['temp_interp']
temp_9_25_a = results[118]['temp_interp']
temp_9_25_b = results[119]['temp_interp']
temp_10_25_a = results[120]['temp_interp']
temp_10_25_b = results[121]['temp_interp']
temp_11_25 = results[122]['temp_interp']


# Salinity
salt_12_14_a = results[1]['salt_interp']
salt_12_14_b = results[2]['salt_interp']
salt_1_15 = results[3]['salt_interp']
salt_2_15_a = results[4]['salt_interp']
salt_2_15_b = results[5]['salt_interp']
salt_3_15 = results[6]['salt_interp']
salt_4_15 = results[7]['salt_interp']
salt_5_15 = results[8]['salt_interp']
salt_6_15 = results[9]['salt_interp']
salt_7_15 = results[10]['salt_interp']
salt_8_15 = results[11]['salt_interp']
salt_9_15 = results[12]['salt_interp']
salt_10_15 = results[13]['salt_interp']
salt_11_15 = results[14]['salt_interp']
salt_12_15 = results[15]['salt_interp']
salt_1_16 = results[16]['salt_interp']
salt_3_16 = results[17]['salt_interp']
salt_4_16 = results[18]['salt_interp']
salt_5_16 = results[19]['salt_interp']
salt_6_16 = results[20]['salt_interp']
salt_7_16 = results[21]['salt_interp']
salt_8_16 = results[22]['salt_interp']
salt_9_16_a = results[23]['salt_interp']
salt_9_16_b = results[24]['salt_interp']
salt_10_16_a = results[25]['salt_interp']
salt_10_16_b = results[26]['salt_interp']
salt_11_16 = results[27]['salt_interp']
salt_12_16 = results[28]['salt_interp']
salt_1_17 = results[29]['salt_interp']
salt_2_17 = results[30]['salt_interp']
salt_3_17 = results[31]['salt_interp']
salt_4_17_a = results[32]['salt_interp']
salt_4_17_b = results[33]['salt_interp']
salt_5_17 = results[34]['salt_interp']
salt_6_17 = results[35]['salt_interp']
salt_7_17 = results[36]['salt_interp']
salt_8_17 = results[37]['salt_interp']
salt_9_17 = results[38]['salt_interp']
salt_10_17_a = results[39]['salt_interp']
salt_10_17_b = results[40]['salt_interp']
salt_11_17 = results[41]['salt_interp']
salt_4_18 = results[42]['salt_interp']
salt_5_18 = results[43]['salt_interp']
salt_6_18 = results[44]['salt_interp']
salt_8_18 = results[45]['salt_interp']
salt_9_18_a = results[46]['salt_interp']
salt_9_18_b = results[47]['salt_interp']
salt_11_18 = results[48]['salt_interp']
salt_12_18 = results[49]['salt_interp']
salt_1_19 = results[50]['salt_interp']
salt_2_19 = results[51]['salt_interp']
salt_3_19_a = results[52]['salt_interp']
salt_3_19_b = results[53]['salt_interp']
salt_4_19_a = results[54]['salt_interp']
salt_4_19_b = results[55]['salt_interp']
salt_6_19 = results[56]['salt_interp']
salt_7_19 = results[57]['salt_interp']
salt_8_19 = results[58]['salt_interp']
salt_9_19 = results[59]['salt_interp']
salt_10_19 = results[60]['salt_interp']
salt_11_19 = results[61]['salt_interp']
salt_12_19 = results[62]['salt_interp']
salt_1_20 = results[63]['salt_interp']
salt_2_20 = results[64]['salt_interp']
salt_3_20_a = results[65]['salt_interp']
salt_3_20_b = results[66]['salt_interp']
salt_9_20 = results[67]['salt_interp']
salt_10_20 = results[68]['salt_interp']
salt_11_20 = results[69]['salt_interp']
salt_12_20 = results[70]['salt_interp']
salt_1_21 = results[71]['salt_interp']
salt_2_21 = results[72]['salt_interp']
salt_11_21 = results[73]['salt_interp']
salt_12_21 = results[74]['salt_interp']
salt_1_22 = results[75]['salt_interp']
salt_2_22 = results[76]['salt_interp']
salt_3_22 = results[77]['salt_interp']
salt_4_22 = results[78]['salt_interp']
salt_5_22 = results[79]['salt_interp']
salt_6_22 = results[80]['salt_interp']
salt_8_22 = results[81]['salt_interp']
salt_9_22 = results[82]['salt_interp']
salt_10_22 = results[83]['salt_interp']
salt_11_22 = results[84]['salt_interp']
salt_12_22 = results[85]['salt_interp']
salt_1_23 = results[86]['salt_interp']
salt_2_23 = results[87]['salt_interp']
salt_3_23_a = results[88]['salt_interp']
salt_3_23_b = results[89]['salt_interp']
salt_4_23 = results[90]['salt_interp']
salt_5_23 = results[91]['salt_interp']
salt_6_23 = results[92]['salt_interp']
salt_7_23 = results[93]['salt_interp']
salt_8_23 = results[94]['salt_interp']
salt_10_23 = results[95]['salt_interp']
salt_11_23 = results[96]['salt_interp']
salt_12_23 = results[97]['salt_interp']
salt_1_24= results[98]['salt_interp']
salt_2_24_a= results[99]['salt_interp']
salt_2_24_b= results[100]['salt_interp']
salt_3_24= results[101]['salt_interp']
salt_4_24= results[102]['salt_interp']
salt_5_24= results[103]['salt_interp']
salt_6_24= results[104]['salt_interp']
salt_7_24= results[105]['salt_interp']
salt_8_24_a= results[106]['salt_interp']
salt_8_24_b= results[107]['salt_interp']
salt_10_24= results[108]['salt_interp']
salt_11_24= results[109]['salt_interp']
salt_3_25= results[110]['salt_corrected_interp']
salt_4_25_a= results[111]['salt_corrected_interp']
salt_4_25_b= results[112]['salt_corrected_interp']
salt_5_25 = results[113]['salt_corrected_interp']
salt_6_25_a = results[114]['salt_corrected_interp']
salt_6_25_b = results[115]['salt_corrected_interp']
salt_7_25 = results[116]['salt_corrected_interp']
salt_8_25_a = results[117]['salt_corrected_interp']
salt_9_25_a = results[118]['salt_corrected_interp']
salt_9_25_b = results[119]['salt_corrected_interp']
salt_10_25_a = results[120]['salt_corrected_interp']
salt_10_25_b = results[121]['salt_corrected_interp']
salt_11_25 = results[122]['salt_interp']

# Time
time_12_14_a = results[1]['time']
time_12_14_b = results[2]['time']
time_1_15 = results[3]['time']
time_2_15_a = results[4]['time']
time_2_15_b = results[5]['time']
time_3_15 = results[6]['time']
time_4_15 = results[7]['time']
time_5_15 = results[8]['time']
time_6_15 = results[9]['time']
time_7_15 = results[10]['time']
time_8_15 = results[11]['time']
time_9_15 = results[12]['time']
time_10_15 = results[13]['time']
time_11_15 = results[14]['time']
time_12_15 = results[15]['time']
time_1_16 = results[16]['time']
time_3_16 = results[17]['time']
time_4_16 = results[18]['time']
time_5_16 = results[19]['time']
time_6_16 = results[20]['time']
time_7_16 = results[21]['time']
time_8_16 = results[22]['time']
time_9_16_a = results[23]['time']
time_9_16_b = results[24]['time']
time_10_16_a = results[25]['time']
time_10_16_b = results[26]['time']
time_11_16 = results[27]['time']
time_12_16 = results[28]['time']
time_1_17 = results[29]['time']
time_2_17 = results[30]['time']
time_3_17 = results[31]['time']
time_4_17_a = results[32]['time']
time_4_17_b = results[33]['time']
time_5_17 = results[34]['time']
time_6_17 = results[35]['time']
time_7_17 = results[36]['time']
time_8_17 = results[37]['time']
time_9_17 = results[38]['time']
time_10_17_a = results[39]['time']
time_10_17_b = results[40]['time']
time_11_17 = results[41]['time']
time_4_18 = results[42]['time']
time_5_18 = results[43]['time']
time_6_18 = results[44]['time']
time_8_18 = results[45]['time']
time_9_18_a = results[46]['time']
time_9_18_b = results[47]['time']
time_11_18 = results[48]['time']
time_12_18 = results[49]['time']
time_1_19 = results[50]['time']
time_2_19 = results[51]['time']
time_3_19_a = results[52]['time']
time_3_19_b = results[53]['time']
time_4_19_a = results[54]['time']
time_4_19_b = results[55]['time']
time_6_19 = results[56]['time']
time_7_19 = results[57]['time']
time_8_19 = results[58]['time']
time_9_19 = results[59]['time']
time_10_19 = results[60]['time']
time_11_19 = results[61]['time']
time_12_19 = results[62]['time']
time_1_20 = results[63]['time']
time_2_20 = results[64]['time']
time_3_20_a = results[65]['time']
time_3_20_b = results[66]['time']
time_9_20 = results[67]['time']
time_10_20 = results[68]['time']
time_11_20 = results[69]['time']
time_12_20 = results[70]['time']
time_1_21 = results[71]['time']
time_2_21 = results[72]['time']
time_11_21 = results[73]['time']
time_12_21 = results[74]['time']
time_1_22 = results[75]['time']
time_2_22 = results[76]['time']
time_3_22 = results[77]['time']
time_4_22 = results[78]['time']
time_5_22 = results[79]['time']
time_6_22 = results[80]['time']
time_8_22 = results[81]['time']
time_9_22 = results[82]['time']
time_10_22 = results[83]['time']
time_11_22 = results[84]['time']
time_12_22 = results[85]['time']
time_1_23 = results[86]['time']
time_2_23 = results[87]['time']
time_3_23_a = results[88]['time']
time_3_23_b = results[89]['time']
time_4_23 = results[90]['time']
time_5_23 = results[91]['time']
time_6_23 = results[92]['time']
time_7_23 = results[93]['time']
time_8_23 = results[94]['time']
time_10_23 = results[95]['time']
time_11_23 = results[96]['time']
time_12_23 = results[97]['time']
time_1_24= results[98]['time']
time_2_24_a= results[99]['time']
time_2_24_b= results[100]['time']
time_3_24= results[101]['time']
time_4_24= results[102]['time']
time_5_24= results[103]['time']
time_6_24= results[104]['time']
time_7_24= results[105]['time']
time_8_24_a= results[106]['time']
time_8_24_b= results[107]['time']
time_10_24= results[108]['time']
time_11_24= results[109]['time']
time_3_25= results[110]['time']
time_4_25_a= results[111]['time']
time_4_25_b= results[112]['time']
time_5_25 = results[113]['time']
time_6_25_a = results[114]['time']
time_6_25_b = results[115]['time']
time_7_25 = results[116]['time']
time_8_25_a = results[117]['time']
time_9_25_a = results[118]['time']
time_9_25_b = results[119]['time']
time_10_25_a = results[120]['time']
time_10_25_b = results[121]['time']
time_11_25 = results[122]['time']

# Longitude
lon_12_14_a = results[1]['lon']
lon_12_14_b = results[2]['lon']
lon_1_15 = results[3]['lon']
lon_2_15_a = results[4]['lon']
lon_2_15_b = results[5]['lon']
lon_3_15 = results[6]['lon']
lon_4_15 = results[7]['lon']
lon_5_15 = results[8]['lon']
lon_6_15 = results[9]['lon']
lon_7_15 = results[10]['lon']
lon_8_15 = results[11]['lon']
lon_9_15 = results[12]['lon']
lon_10_15 = results[13]['lon']
lon_11_15 = results[14]['lon']
lon_12_15 = results[15]['lon']
lon_1_16 = results[16]['lon']
lon_3_16 = results[17]['lon']
lon_4_16 = results[18]['lon']
lon_5_16 = results[19]['lon']
lon_6_16 = results[20]['lon']
lon_7_16 = results[21]['lon']
lon_8_16 = results[22]['lon']
lon_9_16_a = results[23]['lon']
lon_9_16_b = results[24]['lon']
lon_10_16_a = results[25]['lon']
lon_10_16_b = results[26]['lon']
lon_11_16 = results[27]['lon']
lon_12_16 = results[28]['lon']
lon_1_17 = results[29]['lon']
lon_2_17 = results[30]['lon']
lon_3_17 = results[31]['lon']
lon_4_17_a = results[32]['lon']
lon_4_17_b = results[33]['lon']
lon_5_17 = results[34]['lon']
lon_6_17 = results[35]['lon']
lon_7_17 = results[36]['lon']
lon_8_17 = results[37]['lon']
lon_9_17 = results[38]['lon']
lon_10_17_a = results[39]['lon']
lon_10_17_b = results[40]['lon']
lon_11_17 = results[41]['lon']
lon_4_18 = results[42]['lon']
lon_5_18 = results[43]['lon']
lon_6_18 = results[44]['lon']
lon_8_18 = results[45]['lon']
lon_9_18_a = results[46]['lon']
lon_9_18_b = results[47]['lon']
lon_11_18 = results[48]['lon']
lon_12_18 = results[49]['lon']
lon_1_19 = results[50]['lon']
lon_2_19 = results[51]['lon']
lon_3_19_a = results[52]['lon']
lon_3_19_b = results[53]['lon']
lon_4_19_a = results[54]['lon']
lon_4_19_b = results[55]['lon']
lon_6_19 = results[56]['lon']
lon_7_19 = results[57]['lon']
lon_8_19 = results[58]['lon']
lon_9_19 = results[59]['lon']
lon_10_19 = results[60]['lon']
lon_11_19 = results[61]['lon']
lon_12_19 = results[62]['lon']
lon_1_20 = results[63]['lon']
lon_2_20 = results[64]['lon']
lon_3_20_a = results[65]['lon']
lon_3_20_b = results[66]['lon']
lon_9_20 = results[67]['lon']
lon_10_20 = results[68]['lon']
lon_11_20 = results[69]['lon']
lon_12_20 = results[70]['lon']
lon_1_21 = results[71]['lon']
lon_2_21 = results[72]['lon']
lon_11_21 = results[73]['lon']
lon_12_21 = results[74]['lon']
lon_1_22 = results[75]['lon']
lon_2_22 = results[76]['lon']
lon_3_22 = results[77]['lon']
lon_4_22 = results[78]['lon']
lon_5_22 = results[79]['lon']
lon_6_22 = results[80]['lon']
lon_8_22 = results[81]['lon']
lon_9_22 = results[82]['lon']
lon_10_22 = results[83]['lon']
lon_11_22 = results[84]['lon']
lon_12_22 = results[85]['lon']
lon_1_23 = results[86]['lon']
lon_2_23 = results[87]['lon']
lon_3_23_a = results[88]['lon']
lon_3_23_b = results[89]['lon']
lon_4_23 = results[90]['lon']
lon_5_23 = results[91]['lon']
lon_6_23 = results[92]['lon']
lon_7_23 = results[93]['lon']
lon_8_23 = results[94]['lon']
lon_10_23 = results[95]['lon']
lon_11_23 = results[96]['lon']
lon_12_23 = results[97]['lon']
lon_1_24= results[98]['lon']
lon_2_24_a= results[99]['lon']
lon_2_24_b= results[100]['lon']
lon_3_24= results[101]['lon']
lon_4_24= results[102]['lon']
lon_5_24= results[103]['lon']
lon_6_24= results[104]['lon']
lon_7_24= results[105]['lon']
lon_8_24_a= results[106]['lon']
lon_8_24_b= results[107]['lon']
lon_10_24= results[108]['lon']
lon_11_24= results[109]['lon']
lon_3_25= results[110]['lon']
lon_4_25_a= results[111]['lon']
lon_4_25_b= results[112]['lon']
lon_5_25 = results[113]['lon']
lon_6_25_a = results[114]['lon']
lon_6_25_b = results[115]['lon']
lon_7_25 = results[116]['lon']
lon_8_25_a = results[117]['lon']
lon_9_25_a = results[118]['lon']
lon_9_25_b = results[119]['lon']
lon_10_25_a = results[120]['lon']
lon_10_25_b = results[121]['lon']
lon_11_25 = results[122]['lon']


# # Temperature Hovmoller
# hov_12_14_a = results[1]['temp_interp_hovmoller']
# hov_12_14_b = results[2]['temp_interp_hovmoller']
# hov_1_15 = results[3]['temp_interp_hovmoller']
# hov_2_15_a = results[4]['temp_interp_hovmoller']
# hov_2_15_b = results[5]['temp_interp_hovmoller']
# hov_3_15 = results[6]['temp_interp_hovmoller']
# hov_4_15 = results[7]['temp_interp_hovmoller']
# hov_5_15 = results[8]['temp_interp_hovmoller']
# hov_6_15 = results[9]['temp_interp_hovmoller']
# hov_7_15 = results[10]['temp_interp_hovmoller']
# hov_8_15 = results[11]['temp_interp_hovmoller']
# hov_9_15 = results[12]['temp_interp_hovmoller']
# hov_10_15 = results[13]['temp_interp_hovmoller']
# hov_11_15 = results[14]['temp_interp_hovmoller']
# hov_12_15 = results[15]['temp_interp_hovmoller']
# hov_1_16 = results[16]['temp_interp_hovmoller']
# hov_3_16 = results[17]['temp_interp_hovmoller']
# hov_4_16 = results[18]['temp_interp_hovmoller']
# hov_5_16 = results[19]['temp_interp_hovmoller']
# hov_6_16 = results[20]['temp_interp_hovmoller']
# hov_7_16 = results[21]['temp_interp_hovmoller']
# hov_8_16 = results[22]['temp_interp_hovmoller']
# hov_9_16_a = results[23]['temp_interp_hovmoller']
# hov_9_16_b = results[24]['temp_interp_hovmoller']
# hov_10_16_a = results[25]['temp_interp_hovmoller']
# hov_10_16_b = results[26]['temp_interp_hovmoller']
# hov_11_16 = results[27]['temp_interp_hovmoller']
# hov_12_16 = results[28]['temp_interp_hovmoller']
# hov_1_17 = results[29]['temp_interp_hovmoller']
# hov_2_17 = results[30]['temp_interp_hovmoller']
# hov_3_17 = results[31]['temp_interp_hovmoller']
# hov_4_17_a = results[32]['temp_interp_hovmoller']
# hov_4_17_b = results[33]['temp_interp_hovmoller']
# hov_5_17 = results[34]['temp_interp_hovmoller']
# hov_6_17 = results[35]['temp_interp_hovmoller']
# hov_7_17 = results[36]['temp_interp_hovmoller']
# hov_8_17 = results[37]['temp_interp_hovmoller']
# hov_9_17 = results[38]['temp_interp_hovmoller']
# hov_10_17_a = results[39]['temp_interp_hovmoller']
# hov_10_17_b = results[40]['temp_interp_hovmoller']
# hov_11_17 = results[41]['temp_interp_hovmoller']
# hov_4_18 = results[42]['temp_interp_hovmoller']
# hov_5_18 = results[43]['temp_interp_hovmoller']
# hov_6_18 = results[44]['temp_interp_hovmoller']
# hov_8_18 = results[45]['temp_interp_hovmoller']
# hov_9_18_a = results[46]['temp_interp_hovmoller']
# hov_9_18_b = results[47]['temp_interp_hovmoller']
# hov_11_18 = results[48]['temp_interp_hovmoller']
# hov_12_18 = results[49]['temp_interp_hovmoller']
# hov_1_19 = results[50]['temp_interp_hovmoller']
# hov_2_19 = results[51]['temp_interp_hovmoller']
# hov_3_19_a = results[52]['temp_interp_hovmoller']
# hov_3_19_b = results[53]['temp_interp_hovmoller']
# hov_4_19_a = results[54]['temp_interp_hovmoller']
# hov_4_19_b = results[55]['temp_interp_hovmoller']
# hov_6_19 = results[56]['temp_interp_hovmoller']
# hov_7_19 = results[57]['temp_interp_hovmoller']
# hov_8_19 = results[58]['temp_interp_hovmoller']
# hov_9_19 = results[59]['temp_interp_hovmoller']
# hov_10_19 = results[60]['temp_interp_hovmoller']
# hov_11_19 = results[61]['temp_interp_hovmoller']
# hov_12_19 = results[62]['temp_interp_hovmoller']
# hov_1_20 = results[63]['temp_interp_hovmoller']
# hov_2_20 = results[64]['temp_interp_hovmoller']
# hov_3_20_a = results[65]['temp_interp_hovmoller']
# hov_3_20_b = results[66]['temp_interp_hovmoller']
# hov_9_20 = results[67]['temp_interp_hovmoller']
# hov_10_20 = results[68]['temp_interp_hovmoller']
# hov_11_20 = results[69]['temp_interp_hovmoller']
# hov_12_20 = results[70]['temp_interp_hovmoller']
# hov_1_21 = results[71]['temp_interp_hovmoller']
# hov_2_21 = results[72]['temp_interp_hovmoller']
# hov_11_21 = results[73]['temp_interp_hovmoller']
# hov_12_21 = results[74]['temp_interp_hovmoller']
# hov_1_22 = results[75]['temp_interp_hovmoller']
# hov_2_22 = results[76]['temp_interp_hovmoller']
# hov_3_22 = results[77]['temp_interp_hovmoller']
# hov_4_22 = results[78]['temp_interp_hovmoller']
# hov_5_22 = results[79]['temp_interp_hovmoller']
# hov_6_22 = results[80]['temp_interp_hovmoller']
# hov_8_22 = results[81]['temp_interp_hovmoller']
# hov_9_22 = results[82]['temp_interp_hovmoller']
# hov_10_22 = results[83]['temp_interp_hovmoller']
# hov_11_22 = results[84]['temp_interp_hovmoller']
# hov_12_22 = results[85]['temp_interp_hovmoller']
# hov_1_23 = results[86]['temp_interp_hovmoller']
# hov_2_23 = results[87]['temp_interp_hovmoller']
# hov_3_23_a = results[88]['temp_interp_hovmoller']
# hov_3_23_b = results[89]['temp_interp_hovmoller']
# hov_4_23 = results[90]['temp_interp_hovmoller']
# hov_5_23 = results[91]['temp_interp_hovmoller']
# hov_6_23 = results[92]['temp_interp_hovmoller']
# hov_7_23 = results[93]['temp_interp_hovmoller']
# hov_8_23 = results[94]['temp_interp_hovmoller']
# hov_10_23 = results[95]['temp_interp_hovmoller']
# hov_11_23 = results[96]['temp_interp_hovmoller']
# hov_12_23 = results[97]['temp_interp_hovmoller']
# hov_1_24 = results[98]['temp_interp_hovmoller']
# hov_2_24_a = results[99]['temp_interp_hovmoller']
# hov_2_24_b= results[100]['temp_interp_hovmoller']
# hov_3_24 = results[101]['temp_interp_hovmoller']
# hov_4_24 = results[102]['temp_interp_hovmoller']
# hov_5_24 = results[103]['temp_interp_hovmoller']
# hov_6_24 = results[104]['temp_interp_hovmoller']
# hov_7_24 = results[105]['temp_interp_hovmoller']
# hov_8_24_a = results[106]['temp_interp_hovmoller']
# hov_8_24_b = results[107]['temp_interp_hovmoller']
# hov_10_24 = results[108]['temp_interp_hovmoller']