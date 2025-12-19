#!/usr/bin/env python
# coding: utf-8

# Imports
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
from matplotlib import colors
from datetime import datetime
from scipy.interpolate import griddata
import pandas as pd
import woa_temp
import woa_salt
import transects_func
import anomaly


# Open WOA Climatology Data
# Data Access Here: https://www.ncei.noaa.gov/access/world-ocean-atlas-2018/bin/woa18.pl

# WOA Temperature
woa_temp_months = {
    '1': woa_temp.woa_temp_jan,
    '2': woa_temp.woa_temp_feb,
    '3': woa_temp.woa_temp_mar,
    '4': woa_temp.woa_temp_apr,
    '5': woa_temp.woa_temp_may,
    '6': woa_temp.woa_temp_jun,
    '7': woa_temp.woa_temp_jul,
    '8': woa_temp.woa_temp_aug,
    '9': woa_temp.woa_temp_sep,
    '10': woa_temp.woa_temp_oct,
    '11': woa_temp.woa_temp_nov,
    '12': woa_temp.woa_temp_dec
}

# WOA Salinity
woa_salt_months = {
    '1': woa_salt.woa_salt_jan,
    '2': woa_salt.woa_salt_feb,
    '3': woa_salt.woa_salt_mar,
    '4': woa_salt.woa_salt_apr,
    '5': woa_salt.woa_salt_may,
    '6': woa_salt.woa_salt_jun,
    '7': woa_salt.woa_salt_jul,
    '8': woa_salt.woa_salt_aug,
    '9': woa_salt.woa_salt_sep,
    '10': woa_salt.woa_salt_oct,
    '11': woa_salt.woa_salt_nov,
    '12': woa_salt.woa_salt_dec
}


# SCTI / ONI Data
# Data Access Here: https://spraydata.ucsd.edu/products/socal-index/

with xr.open_dataset(r'C:/Users/marqjace/TH_line/scti_oni/socal_index_monthly_v1_8571_f367_229e_U1766170430759.nc', decode_times=False) as dat:
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
# García-Reyes, M. and Sydeman, W.J. (2017). California Multivariate Ocean Climate Indicator (MOCI) [Data set, V2]. Farallon Institute website, http://www.faralloninstitute.org/moci. Accessed [28 May 2025].
with open(r'C:/Users/marqjace/TH_line/california_moci/CaliforniaMOCI.csv', 'r') as file:
    dat2 = pd.read_csv(file)
dat2 = dat2.drop(['Year', 'Season', 'Central California (34.5-38N)', 'Southern California (32-34.5N)'], axis=1)
dat2 = dat2.set_index(['time'])

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

# # Filepaths of individual transects
# filepaths = [

#     # Nov 2014 Deployment
#     r'C:/Users/marqjace/TH_line/deployments/nov_2014/transect1/12_14_a_merged.nc',
#     r'C:/Users/marqjace/TH_line/deployments/nov_2014/transect2/12_14_b_merged.nc',
#     r'C:/Users/marqjace/TH_line/deployments/nov_2014/transect3/1_15_merged.nc',
# ]

# # Process the transects (grids them and puts them into a dictionary)
# transects_func_new.batch_process(filepaths)

# Interpolated & Gridded Temperature
temp_transects = {
    '10_14' : transects_func.temp_12_14_a, # For cutoff values
    '11_14' : transects_func.temp_12_14_a, # For cutoff values
    '12_14_a' : transects_func.temp_12_14_a,
    '12_14_b' : transects_func.temp_12_14_b,
    '1_15' : transects_func.temp_1_15,
    '2_15_a': transects_func.temp_2_15_a,
    '2_15_b': transects_func.temp_2_15_b,
    '3_15': transects_func.temp_3_15,
    '4_15': transects_func.temp_4_15,
    '5_15': transects_func.temp_5_15,
    '6_15': transects_func.temp_6_15,
    '7_15': transects_func.temp_7_15,
    '8_15': transects_func.temp_8_15,
    '9_15': transects_func.temp_9_15,
    '10_15': transects_func.temp_10_15,
    '11_15': transects_func.temp_11_15,
    '12_15': transects_func.temp_12_15,
    '1_16': transects_func.temp_1_16,
    '3_16': transects_func.temp_3_16,
    '4_16': transects_func.temp_4_16,
    '5_16': transects_func.temp_5_16,
    '6_16': transects_func.temp_6_16,
    '7_16': transects_func.temp_7_16,
    '8_16': transects_func.temp_8_16,
    '9_16_a': transects_func.temp_9_16_a,
    '9_16_b': transects_func.temp_9_16_b,
    '10_16_a': transects_func.temp_10_16_a,
    '10_16_b': transects_func.temp_10_16_b,
    '11_16': transects_func.temp_11_16,
    '12_16': transects_func.temp_12_16,
    '1_17': transects_func.temp_1_17,
    '2_17': transects_func.temp_2_17,
    '3_17': transects_func.temp_3_17,
    '4_17_a': transects_func.temp_4_17_a,
    '4_17_b': transects_func.temp_4_17_b,
    '5_17': transects_func.temp_5_17,
    '6_17': transects_func.temp_6_17,
    '7_17': transects_func.temp_7_17,
    '8_17': transects_func.temp_8_17,
    '9_17': transects_func.temp_9_17,
    '10_17_a': transects_func.temp_10_17_a,
    '10_17_b': transects_func.temp_10_17_b,
    '11_17': transects_func.temp_11_17,   # Something is wrong on this transect
    '4_18': transects_func.temp_4_18,
    '5_18': transects_func.temp_5_18,
    '6_18': transects_func.temp_6_18,
    '8_18': transects_func.temp_8_18,
    '9_18_a': transects_func.temp_9_18_a,
    '9_18_b': transects_func.temp_9_18_b,   # Something is wrong on this transect
    '11_18': transects_func.temp_11_18,
    '12_18': transects_func.temp_12_18,
    '1_19': transects_func.temp_1_19,
    '2_19': transects_func.temp_2_19,
    '3_19_a': transects_func.temp_3_19_a,
    '3_19_b': transects_func.temp_3_19_b,
    '4_19_a': transects_func.temp_4_19_a,
    '4_19_b': transects_func.temp_4_19_b,
    '6_19': transects_func.temp_6_19,
    '7_19': transects_func.temp_7_19,
    '8_19': transects_func.temp_8_19,
    '9_19': transects_func.temp_9_19,
    '10_19': transects_func.temp_10_19,
    '11_19': transects_func.temp_11_19,
    '12_19': transects_func.temp_12_19,
    '1_20': transects_func.temp_1_20,
    '2_20': transects_func.temp_2_20,
    '3_20_a': transects_func.temp_3_20_a,
    '3_20_b': transects_func.temp_3_20_b,
    '9_20': transects_func.temp_9_20,
    '10_20': transects_func.temp_10_20,
    '11_20': transects_func.temp_11_20,
    '12_20': transects_func.temp_12_20,
    '1_21': transects_func.temp_1_21,
    '2_21': transects_func.temp_2_21,   # Something is wrong on this transect
    '11_21': transects_func.temp_11_21,
    '12_21': transects_func.temp_12_21,
    '1_22': transects_func.temp_1_22,
    '2_22': transects_func.temp_2_22,
    '3_22': transects_func.temp_3_22,
    '4_22': transects_func.temp_4_22,
    '5_22': transects_func.temp_5_22,
    '6_22': transects_func.temp_6_22,
    '8_22': transects_func.temp_8_22,
    '9_22': transects_func.temp_9_22,
    '10_22': transects_func.temp_10_22,
    '11_22': transects_func.temp_11_22,
    '12_22': transects_func.temp_12_22,
    '1_23': transects_func.temp_1_23,
    '2_23': transects_func.temp_2_23,
    '3_23_a': transects_func.temp_3_23_a,
    '3_23_b': transects_func.temp_3_23_b,
    '4_23': transects_func.temp_4_23,
    '5_23': transects_func.temp_5_23,
    '6_23': transects_func.temp_6_23,
    '7_23': transects_func.temp_7_23,
    '8_23': transects_func.temp_8_23,
    '10_23': transects_func.temp_10_23,
    '11_23': transects_func.temp_11_23,
    '12_23': transects_func.temp_12_23,
    '1_24': transects_func.temp_1_24,
    '2_24_a': transects_func.temp_2_24_a,
    '2_24_ b': transects_func.temp_2_24_b,
    '3_24': transects_func.temp_3_24,
    '4_24': transects_func.temp_4_24,
    '5_24': transects_func.temp_5_24,
    '6_24': transects_func.temp_6_24,
    '7_24': transects_func.temp_7_24,   # Something is wrong on this transect
    '8_24_a': transects_func.temp_8_24_a,   # Something is wrong on this transect
    '8_24_b': transects_func.temp_8_24_b,   # Something is wrong on this transect
    '10_24': transects_func.temp_10_24,
    '11_24': transects_func.temp_11_24,
    '3_25': transects_func.temp_3_25,
    '4_25_a': transects_func.temp_4_25_a,
    '4_25_b': transects_func.temp_4_25_b,
    '5_25': transects_func.temp_5_25, 
    '6_25_a': transects_func.temp_6_25_a,
    '6_25_b': transects_func.temp_6_25_b,
    '7_25': transects_func.temp_7_25,
    '8_25_a': transects_func.temp_8_25_a, 
    '9_25_a': transects_func.temp_9_25_a,
    '9_25_b': transects_func.temp_9_25_b,
    '10_25_a': transects_func.temp_10_25_a,
    '10_25_b': transects_func.temp_10_25_b,
    '11_25': transects_func.temp_11_25,
    '12_25': transects_func.temp_11_25, # For cutoff values
    '1_26': transects_func.temp_11_25, # For cutoff values
    }

salt_transects = {
    '10_14' : transects_func.salt_12_14_a, # For cutoff values
    '11_14' : transects_func.salt_12_14_a, # For cutoff values
    '12_14_a' : transects_func.salt_12_14_a,
    '12_14_b' : transects_func.salt_12_14_b,
    '1_15' : transects_func.salt_1_15,
    '2_15_a': transects_func.salt_2_15_a,
    '2_15_b': transects_func.salt_2_15_b,
    '3_15': transects_func.salt_3_15,
    '4_15': transects_func.salt_4_15,
    '5_15': transects_func.salt_5_15,
    '6_15': transects_func.salt_6_15,
    '7_15': transects_func.salt_7_15,
    '8_15': transects_func.salt_8_15,
    '9_15': transects_func.salt_9_15,
    '10_15': transects_func.salt_10_15,
    '11_15': transects_func.salt_11_15,
    '12_15': transects_func.salt_12_15,
    '1_16': transects_func.salt_1_16,
    '3_16': transects_func.salt_3_16,
    '4_16': transects_func.salt_4_16,
    '5_16': transects_func.salt_5_16,
    '6_16': transects_func.salt_6_16,
    '7_16': transects_func.salt_7_16,
    '8_16': transects_func.salt_8_16,
    '9_16_a': transects_func.salt_9_16_a,
    '9_16_b': transects_func.salt_9_16_b,
    '10_16_a': transects_func.salt_10_16_a,
    '10_16_b': transects_func.salt_10_16_b,
    '11_16': transects_func.salt_11_16,
    '12_16': transects_func.salt_12_16,
    '1_17': transects_func.salt_1_17,
    '2_17': transects_func.salt_2_17,
    '3_17': transects_func.salt_3_17,
    '4_17_a': transects_func.salt_4_17_a,
    '4_17_b': transects_func.salt_4_17_b,
    '5_17': transects_func.salt_5_17,
    '6_17': transects_func.salt_6_17,
    '7_17': transects_func.salt_7_17,
    '8_17': transects_func.salt_8_17,
    '9_17': transects_func.salt_9_17,
    '10_17_a': transects_func.salt_10_17_a,
    '10_17_b': transects_func.salt_10_17_b,
    '11_17': transects_func.salt_11_17,   # Something is wrong on this transect
    '4_18': transects_func.salt_4_18,
    '5_18': transects_func.salt_5_18,
    '6_18': transects_func.salt_6_18,
    '8_18': transects_func.salt_8_18,
    '9_18_a': transects_func.salt_9_18_a,
    '9_18_b': transects_func.salt_9_18_b,   # Something is wrong on this transect
    '11_18': transects_func.salt_11_18,
    '12_18': transects_func.salt_12_18,
    '1_19': transects_func.salt_1_19,
    '2_19': transects_func.salt_2_19,
    '3_19_a': transects_func.salt_3_19_a,
    '3_19_b': transects_func.salt_3_19_b,
    '4_19_a': transects_func.salt_4_19_a,
    '4_19_b': transects_func.salt_4_19_b,
    '6_19': transects_func.salt_6_19,
    '7_19': transects_func.salt_7_19,
    '8_19': transects_func.salt_8_19,
    '9_19': transects_func.salt_9_19,
    '10_19': transects_func.salt_10_19,
    '11_19': transects_func.salt_11_19,
    '12_19': transects_func.salt_12_19,
    '1_20': transects_func.salt_1_20,
    '2_20': transects_func.salt_2_20,
    '3_20_a': transects_func.salt_3_20_a,
    '3_20_b': transects_func.salt_3_20_b,
    '9_20': transects_func.salt_9_20,
    '10_20': transects_func.salt_10_20,
    '11_20': transects_func.salt_11_20,
    '12_20': transects_func.salt_12_20,
    '1_21': transects_func.salt_1_21,
    '2_21': transects_func.salt_2_21,   # Something is wrong on this transect
    '11_21': transects_func.salt_11_21,
    '12_21': transects_func.salt_12_21,
    '1_22': transects_func.salt_1_22,
    '2_22': transects_func.salt_2_22,
    '3_22': transects_func.salt_3_22,
    '4_22': transects_func.salt_4_22,
    '5_22': transects_func.salt_5_22,
    '6_22': transects_func.salt_6_22,
    '8_22': transects_func.salt_8_22,
    '9_22': transects_func.salt_9_22,
    '10_22': transects_func.salt_10_22,
    '11_22': transects_func.salt_11_22,
    '12_22': transects_func.salt_12_22,
    '1_23': transects_func.salt_1_23,
    '2_23': transects_func.salt_2_23,
    '3_23_a': transects_func.salt_3_23_a,
    '3_23_b': transects_func.salt_3_23_b,
    '4_23': transects_func.salt_4_23,
    '5_23': transects_func.salt_5_23,
    '6_23': transects_func.salt_6_23,
    '7_23': transects_func.salt_7_23,
    '8_23': transects_func.salt_8_23,
    '10_23': transects_func.salt_10_23,
    '11_23': transects_func.salt_11_23,
    '12_23': transects_func.salt_12_23,
    '1_24': transects_func.salt_1_24,
    '2_24_a': transects_func.salt_2_24_a,
    '2_24_ b': transects_func.salt_2_24_b,
    '3_24': transects_func.salt_3_24,
    '4_24': transects_func.salt_4_24,
    '5_24': transects_func.salt_5_24,
    '6_24': transects_func.salt_6_24,
    '7_24': transects_func.salt_7_24,   # Something is wrong on this transect
    '8_24_a': transects_func.salt_8_24_a,   # Something is wrong on this transect
    '8_24_b': transects_func.salt_8_24_b,   # Something is wrong on this transect
    '10_24': transects_func.salt_10_24,
    '11_24': transects_func.salt_11_24,
    '3_25': transects_func.salt_3_25,
    '4_25_a': transects_func.salt_4_25_a,
    '4_25_b': transects_func.salt_4_25_b,
    '5_25': transects_func.salt_5_25,
    '6_25_a': transects_func.salt_6_25_a,
    '6_25_b': transects_func.salt_6_25_b,
    '7_25': transects_func.salt_7_25,
    '8_25_a': transects_func.salt_8_25_a,
    '9_25_a': transects_func.salt_9_25_a,
    '9_25_b': transects_func.salt_9_25_b,
    '10_25_a': transects_func.salt_10_25_a,
    '10_25_b': transects_func.salt_10_25_b,
    '11_25': transects_func.salt_11_25,
    '12_25': transects_func.salt_11_25, # For cutoff values
    '1_26': transects_func.salt_11_25, # For cutoff values
    '6_25_a': transects_func.salt_6_25_a,
    '6_25_b': transects_func.salt_6_25_b,
    '7_25': transects_func.salt_7_25,
    '8_25_a': transects_func.salt_8_25_a,
    '9_25_a': transects_func.salt_9_25_a,
    '9_25_b': transects_func.salt_9_25_b,
    '10_25_a': transects_func.salt_10_25_a,
    '10_25_b': transects_func.salt_10_25_b,
    '11_25': transects_func.salt_11_25,
    '12_25': transects_func.salt_11_25, # For cutoff values
    '1_26': transects_func.salt_11_25, # For cutoff values
    }

temp_anom = anomaly.temperature_anomaly(temp_transects, woa_temp_months)
salt_anom = anomaly.salinity_anomaly(salt_transects, woa_salt_months)

temp_anoms = {
    '10_14': temp_anom[0], # For cutoff values
    '11_14': temp_anom[1], # For cutoff values
    '12_14_a': temp_anom[2],
    '12_14_b': temp_anom[3],
    '1_15': temp_anom[4], 
    '2_15_a': temp_anom[5],
    '2_15_b': temp_anom[6],
    '3_15': temp_anom[7],
    '4_15': temp_anom[8],
    '5_15': temp_anom[9],
    '6_15': temp_anom[10],
    '7_15': temp_anom[11],
    '8_15': temp_anom[12],
    '9_15': temp_anom[13],
    '10_15': temp_anom[14],
    '11_15': temp_anom[15],
    '12_15': temp_anom[16],
    '1_16': temp_anom[17],
    '3_16': temp_anom[18],
    '4_16': temp_anom[19],
    # '5_16': temp_anom[20],   # Something is wrong on this transet
    '6_16': temp_anom[21],
    '7_16': temp_anom[22],
    '8_16': temp_anom[23],
    '9_16_a': temp_anom[24],
    '9_16_b': temp_anom[25],
    '10_16_a': temp_anom[26],
    '10_16_b': temp_anom[27],
    '11_16': temp_anom[28],
    '12_16': temp_anom[29],
    '1_17': temp_anom[30],
    '2_17': temp_anom[31],
    '3_17': temp_anom[32],
    '4_17_a': temp_anom[33],
    '4_17_b': temp_anom[34],
    '5_17': temp_anom[35],
    '6_17': temp_anom[36],
    '7_17': temp_anom[37],
    '8_17': temp_anom[38],
    '9_17': temp_anom[39],
    '10_17_a': temp_anom[40],
    '10_17_b': temp_anom[41],
    # '11_17': temp_anom[42],   # Something is wrong on this transect
    '4_18': temp_anom[43],
    '5_18': temp_anom[44],
    '6_18': temp_anom[45],
    '8_18': temp_anom[46],
    '9_18_a': temp_anom[47],
    # '9_18_b': temp_anom[48],   # Something is wrong on this transect
    '11_18': temp_anom[49],
    '12_18': temp_anom[50],
    '1_19': temp_anom[51],
    '2_19': temp_anom[52],
    '3_19_a': temp_anom[53],
    '3_19_b': temp_anom[54],
    '4_19_a': temp_anom[55],
    '4_19_b': temp_anom[56],
    '6_19': temp_anom[57],
    '7_19': temp_anom[58],
    '8_19': temp_anom[59],
    '9_19': temp_anom[60],
    '10_19': temp_anom[61],
    '11_19': temp_anom[62],
    '12_19': temp_anom[63],
    '1_20': temp_anom[64],
    '2_20': temp_anom[65],
    '3_20_a': temp_anom[66],
    '3_20_b': temp_anom[67],
    '9_20': temp_anom[68],
    '10_20': temp_anom[69],
    '11_20': temp_anom[70],
    '12_20': temp_anom[71],
    '1_21': temp_anom[72],
    # '2_21': temp_anom[73],   # Something is wrong on this transect
    '11_21': temp_anom[74],
    '12_21': temp_anom[75],
    '1_22': temp_anom[76],
    '2_22': temp_anom[77],
    '3_22': temp_anom[78],
    '4_22': temp_anom[79],
    '5_22': temp_anom[80],
    '6_22': temp_anom[81],
    '8_22': temp_anom[82],
    '9_22': temp_anom[83],
    '10_22': temp_anom[84],
    '11_22': temp_anom[85],
    '12_22': temp_anom[86],
    '1_23': temp_anom[87],
    '2_23': temp_anom[88],
    '3_23_a': temp_anom[89],
    '3_23_b': temp_anom[90],
    '4_23': temp_anom[91],
    '5_23': temp_anom[92],
    '6_23': temp_anom[93],
    '7_23': temp_anom[94],
    '8_23': temp_anom[95],
    '10_23': temp_anom[96],
    '11_23': temp_anom[97],
    '12_23': temp_anom[98],
    '1_24': temp_anom[99],
    '2_24_a': temp_anom[100],
    '2_24_ b': temp_anom[101],
    '3_24': temp_anom[102],
    '4_24': temp_anom[103],
    '5_24': temp_anom[104],
    '6_24': temp_anom[105],
    # '7_24': temp_anom[106],   # Something is wrong on this transect
    # '8_24_a': temp_anom[107],   # Something is wrong on this transect
    # '8_24_b': temp_anom[108],   # Something is wrong on this transect
    '10_24': temp_anom[109],
    '11_24': temp_anom[110],
    '3_25': temp_anom[111],
    '4_25_a': temp_anom[112],
    '4_25_b': temp_anom[113],
    '5_25': temp_anom[114],
    '6_25_a': temp_anom[115],
    '6_25_b': temp_anom[116],
    '7_25': temp_anom[117],
    '8_25_a': temp_anom[118],
    '9_25_a': temp_anom[119],
    '9_25_b': temp_anom[120],
    '10_25_a': temp_anom[121],
    '10_25_b': temp_anom[122],
    '11_25': temp_anom[123],
    '12_25': temp_anom[123], # For cutoff values
    '1_26': temp_anom[123], # For cutoff values
}

salt_anoms = {
    '10_14': salt_anom[0], # For cutoff values
    '11_14': salt_anom[1], # For cutoff values
    '12_14_a': salt_anom[2],
    '12_14_b': salt_anom[3],
    '1_15': salt_anom[4], 
    '2_15_a': salt_anom[5],
    '2_15_b': salt_anom[6],
    '3_15': salt_anom[7],
    '4_15': salt_anom[8],
    '5_15': salt_anom[9],
    '6_15': salt_anom[10],
    '7_15': salt_anom[11],
    '8_15': salt_anom[12],
    '9_15': salt_anom[13],
    '10_15': salt_anom[14],
    '11_15': salt_anom[15],
    '12_15': salt_anom[16],
    '1_16': salt_anom[17],
    '3_16': salt_anom[18],
    '4_16': salt_anom[19],
    # '5_16': salt_anom[20],   # Something is wrong on this transet
    '6_16': salt_anom[21],
    '7_16': salt_anom[22],
    '8_16': salt_anom[23],
    '9_16_a': salt_anom[24],
    '9_16_b': salt_anom[25],
    '10_16_a': salt_anom[26],
    '10_16_b': salt_anom[27],
    '11_16': salt_anom[28],
    '12_16': salt_anom[29],
    '1_17': salt_anom[30],
    '2_17': salt_anom[31],
    '3_17': salt_anom[32],
    '4_17_a': salt_anom[33],
    '4_17_b': salt_anom[34],
    '5_17': salt_anom[35],
    '6_17': salt_anom[36],
    '7_17': salt_anom[37],
    '8_17': salt_anom[38],
    '9_17': salt_anom[39],
    '10_17_a': salt_anom[40],
    '10_17_b': salt_anom[41],
    # '11_17': salt_anom[42],   # Something is wrong on this transect
    '4_18': salt_anom[43],
    '5_18': salt_anom[44],
    '6_18': salt_anom[45],
    '8_18': salt_anom[46],
    '9_18_a': salt_anom[47],
    # '9_18_b': salt_anom[48],   # Something is wrong on this transect
    '11_18': salt_anom[49],
    '12_18': salt_anom[50],
    '1_19': salt_anom[51],
    '2_19': salt_anom[52],
    '3_19_a': salt_anom[53],
    '3_19_b': salt_anom[54],
    '4_19_a': salt_anom[55],
    '4_19_b': salt_anom[56],
    '6_19': salt_anom[57],
    '7_19': salt_anom[58],
    '8_19': salt_anom[59],
    '9_19': salt_anom[60],
    '10_19': salt_anom[61],
    '11_19': salt_anom[62],
    '12_19': salt_anom[63],
    '1_20': salt_anom[64],
    '2_20': salt_anom[65],
    '3_20_a': salt_anom[66],
    '3_20_b': salt_anom[67],
    '9_20': salt_anom[68],
    '10_20': salt_anom[69],
    '11_20': salt_anom[70],
    '12_20': salt_anom[71],
    '1_21': salt_anom[72],
    # '2_21': salt_anom[73],   # Something is wrong on this transect
    '11_21': salt_anom[74],
    '12_21': salt_anom[75],
    '1_22': salt_anom[76],
    '2_22': salt_anom[77],
    '3_22': salt_anom[78],
    '4_22': salt_anom[79],
    '5_22': salt_anom[80],
    '6_22': salt_anom[81],
    '8_22': salt_anom[82],
    '9_22': salt_anom[83],
    '10_22': salt_anom[84],
    '11_22': salt_anom[85],
    '12_22': salt_anom[86],
    '1_23': salt_anom[87],
    '2_23': salt_anom[88],
    '3_23_a': salt_anom[89],
    '3_23_b': salt_anom[90],
    '4_23': salt_anom[91],
    '5_23': salt_anom[92],
    '6_23': salt_anom[93],
    '7_23': salt_anom[94],
    '8_23': salt_anom[95],
    '10_23': salt_anom[96],
    '11_23': salt_anom[97],
    '12_23': salt_anom[98],
    '1_24': salt_anom[99],
    '2_24_a': salt_anom[100],
    '2_24_ b': salt_anom[101],
    '3_24': salt_anom[102],
    '4_24': salt_anom[103],
    '5_24': salt_anom[104],
    '6_24': salt_anom[105],
    # '7_24': salt_anom[106],   # Something is wrong on this transect
    # '8_24_a': salt_anom[107],   # Something is wrong on this transect
    # '8_24_b': salt_anom[108],   # Something is wrong on this transect
    '10_24': salt_anom[109],
    '11_24': salt_anom[110],
    '3_25': salt_anom[111],
    '4_25_a': salt_anom[112],
    '4_25_b': salt_anom[113],
    '5_25': salt_anom[114],
    '6_25_a': salt_anom[115],
    '6_25_b': salt_anom[116],
    '7_25': salt_anom[117],
    '8_25_a': salt_anom[118],
    '9_25_a': salt_anom[119],
    '9_25_b': salt_anom[120],
    '10_25_a': salt_anom[121],
    '10_25_b': salt_anom[122],
    '11_25': salt_anom[123],
    '12_25': salt_anom[123], # For cutoff values
    '1_26': salt_anom[123], # For cutoff values
}

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
    'tran_3_25':np.array([datetime(2025,3,19).toordinal()]),
    'tran_4_25_a':np.array([datetime(2025,4,8).toordinal()]),   
    'tran_4_25_b':np.array([datetime(2025,4,27).toordinal()]),   
    'tran_5_25':np.array([datetime(2025,5,17).toordinal()]),   
    'tran_6_25_a':np.array([datetime(2025,6,7).toordinal()]),
    'tran_6_25_b':np.array([datetime(2025,6,28).toordinal()]),
    'tran_7_25':np.array([datetime(2025,7,20).toordinal()]),
    'tran_8_25_a':np.array([datetime(2025,8,9).toordinal()]),
    'tran_9_25_a':np.array([datetime(2025,9,1).toordinal()]),
    'tran_9_25_b':np.array([datetime(2025,9,22).toordinal()]), 
    'tran_10_25_a':np.array([datetime(2025,10,11).toordinal()]),
    'tran_10_25_b':np.array([datetime(2025,10,28).toordinal()]),
    'tran_11_25':np.array([datetime(2025,11,23).toordinal()]),
    'tran_12_25':np.array([datetime(2025,12,15).toordinal()]),  # For cutoff values
    'tran_1_26':np.array([datetime(2026,1,15).toordinal()]),  # For cutoff values

}


combined_temp_data = []

print('Creating a mean depth profile for each transect...')
for transect, array in temp_anoms.items():
    temp_anoms[transect] = np.mean(array, axis=1)   # Creates a profile of the mean values across depth

for transect, array in temp_anoms.items():
    temp_anoms[transect] = xr.DataArray(array)   # Converts the numpy array to an xarray DataArray for the next step
    
print('Adding transect time to the temp anomaly data...')
for (transect, array), (transect_time, time) in zip(temp_anoms.items(), transect_times.items()):
    temp_anoms[transect] = array.expand_dims(time=time)   # Adds the time point from transect_times to the DataArray

for transect, array in temp_anoms.items():
    combined_temp_data.append(array)   # Appends the DataArray to the list: combined_temp_data

print('Concatenating new dataset "combined_temp"...')
combined_temp = xr.concat(combined_temp_data, dim='time')   # Concatenates all of the data together

# Replicating surface values up to 10m above surface to prevent cutoff during filtering
print('Replicating surface values up to 10m above the surface...')
surf_vals = combined_temp[:, 1]

surf_vals2 = xr.DataArray(surf_vals)
surf_vals3 = xr.DataArray(surf_vals)

surf_vals2['depth'] = -5
surf_vals3['depth'] = -10

combined_temp = xr.concat((surf_vals2, combined_temp), dim='depth')
combined_temp = xr.concat((surf_vals3, combined_temp), dim='depth')

# Replace surface values with data at 5 meters depth to rid of NaN's
combined_temp[:,2] = combined_temp[:,3]

print('Gridding the temperature data...') # Generate a regular grid to interpolate the data
xgrid = np.arange(combined_temp['time'].min(), combined_temp['time'].max(), 30) # Every 30 days in time
ygrid = np.arange(-10,1000,5) # Every 5m in depth
temp_Xgrid, temp_Ygrid = np.meshgrid(xgrid, ygrid) # Use meshgrid to create a regular grid of time and depth

time_vals = combined_temp['time'].values
depth_vals = combined_temp['depth'].values

# Create coordinate mesh that matches the shape of combined_temp.values
T, D = np.meshgrid(time_vals, depth_vals, indexing='ij')

# Flatten both the coordinate pairs and the data
points = np.column_stack((T.ravel(), D.ravel()))
values = combined_temp.values.ravel()

# Perform the interpolation on the new regular grid
combined_temp = griddata(
    points=points,
    values=values,
    xi=(temp_Xgrid, temp_Ygrid),
    method='linear'
)

print('Interpolating the temperature data...')
# combined_temp = combined_temp.interp(time=xgrid,depth=ygrid, method='linear') # Interpolate the data over the new grid
# temp_Xgrid, temp_Ygrid = np.meshgrid(combined_temp['time'], combined_temp['depth']) # Use meshgrid to create a regular grid of time and depth

# combined_temp = griddata(points = (combined_temp['time'], combined_temp['depth']),
#                 values = combined_temp.values.flatten(),
#                 xi = (temp_Xgrid, temp_Ygrid),
#                 method = 'linear')

temp = combined_temp # Transpose the temperature data
temp = pd.DataFrame(temp) # Make it a pandas dataframe

print('Applying a 3-month boxcar filter...')
temp_box = temp.T.rolling(window=3, center=True, win_type='boxcar').mean() # Boxcar Filter every 3 transects (90 days)
temp_box = temp_box.T.rolling(window=4, center=True, win_type='boxcar').mean() # Boxcar Filter every 4 x 5m (20m)

# temp_roll = temp.rolling(window=3, center=True, win_type='boxcar').mean() # Rolling boxcar filter every 3 transects (90 days)

fifty_meters = temp_box[12] # Extract fifty-meters values
zero_meters = temp_box[2] # Extract surface values

fifty_meters = xr.DataArray(fifty_meters) # Save to xarray data array
zero_meters = xr.DataArray(zero_meters) # Save to xarray data array
thi_time = time_vals # Save the Trinidad Head Index time as "thi_time"


combined_salt_data = []

print('Creating a mean depth profile for each transect...')
for transect, array in salt_anoms.items():
    salt_anoms[transect] = np.mean(array, axis=1)   # Creates a profile of the mean values across depth

for transect, array in salt_anoms.items():
    salt_anoms[transect] = xr.DataArray(array)   # Converts the numpy array to an xarray DataArray for the next step
    
print('Adding transect time to the salt anomaly data...')
for (transect, array), (transect_time, time) in zip(salt_anoms.items(), transect_times.items()):
    salt_anoms[transect] = array.expand_dims(time=time)   # Adds the time point from transect_times to the DataArray

for transect, array in salt_anoms.items():
    combined_salt_data.append(array)   # Appends the DataArray to the list: combined_salt_data

print('Concatenating new dataset "combined_salt"...')
combined_salt = xr.concat(combined_salt_data, dim='time')   # Concatenates all of the data together

# Replicating surface values up to 10m above surface to prevent cutoff during filtering
print('Replicating surface values up to 10m above the surface...')
surf_vals = combined_salt[:, 1]

surf_vals2 = xr.DataArray(surf_vals)
surf_vals3 = xr.DataArray(surf_vals)

surf_vals2['depth'] = -5
surf_vals3['depth'] = -10

combined_salt = xr.concat((surf_vals2, combined_salt), dim='depth')
combined_salt = xr.concat((surf_vals3, combined_salt), dim='depth')

# Replace surface values with data at 5 meters depth to rid of NaN's
combined_salt[:,2] = combined_salt[:,3]

print('Gridding the salinity data...') # Generate a regular grid to interpolate the data
xgrid = np.arange(combined_salt['time'].min(), combined_salt['time'].max(), 30) # Every 30 days in time
ygrid = np.arange(-10,1000,5) # Every 5m in depth
salt_Xgrid, salt_Ygrid = np.meshgrid(xgrid, ygrid) # Use meshgrid to create a regular grid of time and depth

time_vals = combined_salt['time'].values
depth_vals = combined_salt['depth'].values

# Create coordinate mesh that matches the shape of combined_temp.values
T, D = np.meshgrid(time_vals, depth_vals, indexing='ij')

# Flatten both the coordinate pairs and the data
points = np.column_stack((T.ravel(), D.ravel()))
values = combined_salt.values.ravel()

# Perform the interpolation on the new regular grid
combined_salt = griddata(
    points=points,
    values=values,
    xi=(salt_Xgrid, salt_Ygrid),
    method='linear'
)

salt = combined_salt # Transpose the salterature data
salt = pd.DataFrame(salt) # Make it a pandas dataframe

print('Applying a 3-month boxcar filter...')
salt_box = salt.T.rolling(window=3, center=True, win_type='boxcar').mean() # Boxcar Filter every 3 transects (90 days)
salt_box = salt_box.T.rolling(window=4, center=True, win_type='boxcar').mean() # Boxcar Filter every 4 x 5m (20m)

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
print('Plotting recent s-anom')
fig, (ax2) = plt.subplots(1, 1, figsize=(14,8), dpi=300)

plot2 = ax2.contourf(salt_Xgrid, salt_Ygrid, salt_box, cmap='BrBG_r', norm=divnorm_salt, levels=boundaries_salt)
lines2 = ax2.contour(salt_Xgrid, salt_Ygrid, salt_box, colors='black', norm=divnorm_salt, levels=levels_salt, alpha=0.75)
deployment2_nov_14 = ax2.hlines(y=570, xmin=datetime(2014,12,4).toordinal(), xmax=datetime(2015,3,9).toordinal(), color='k')
deployment2_mar_15 = ax2.hlines(y=570, xmin=datetime(2015,3,9).toordinal(), xmax=datetime(2015,9,17).toordinal(), color='k')
deployment2_sep_15 = ax2.hlines(y=570, xmin=datetime(2015,9,17).toordinal(), xmax=datetime(2016,5,16).toordinal(), color='k')
deployment2_may_16 = ax2.hlines(y=570, xmin=datetime(2016,5,23).toordinal(), xmax=datetime(2016,10,21).toordinal(), color='k')
deployment2_oct_16 = ax2.hlines(y=570, xmin=datetime(2016,10,21).toordinal(), xmax=datetime(2017,6,5).toordinal(), color='k')
deployment2_jun_17 = ax2.hlines(y=570, xmin=datetime(2017,6,5).toordinal(), xmax=datetime(2017,11,6).toordinal(), color='k')
deployment2_apr_18 = ax2.hlines(y=570, xmin=datetime(2018,4,17).toordinal(), xmax=datetime(2018,10,2).toordinal(), color='k')
deployment2_nov_18 = ax2.hlines(y=570, xmin=datetime(2018,11,7).toordinal(), xmax=datetime(2019,4,9).toordinal(), color='k')
deployment2_apr_19 = ax2.hlines(y=570, xmin=datetime(2019,4,9).toordinal(), xmax=datetime(2019,8,19).toordinal(), color='k')
deployment2_sep_19 = ax2.hlines(y=570, xmin=datetime(2019,9,16).toordinal(), xmax=datetime(2020,3,19).toordinal(), color='k')
deployment2_sep_20 = ax2.hlines(y=570, xmin=datetime(2020,9,16).toordinal(), xmax=datetime(2021,2,6).toordinal(), color='k')
deployment2_nov_21 = ax2.hlines(y=570, xmin=datetime(2021,11,12).toordinal(), xmax=datetime(2022,6,16).toordinal(), color='k')
deployment2_jul_22 = ax2.hlines(y=570, xmin=datetime(2022,7,29).toordinal(), xmax=datetime(2023,1,26).toordinal(), color='k')
deployment2_jan_23 = ax2.hlines(y=570, xmin=datetime(2023,1,26).toordinal(), xmax=datetime(2023,8,14).toordinal(), color='k')
deployment2_oct_23 = ax2.hlines(y=570, xmin=datetime(2023,10,13).toordinal(), xmax=datetime(2024,4,12).toordinal(), color='k')
deployment2_apr_24 = ax2.hlines(y=570, xmin=datetime(2024,4,12).toordinal(), xmax=datetime(2024,8,9).toordinal(), color='k')
deployment2_oct_24 = ax2.hlines(y=570, xmin=datetime(2024,10,21).toordinal(), xmax=datetime(2024,12,4).toordinal(), color='k')
deployment2_mar_25 = ax2.hlines(y=570, xmin=datetime(2025,3,21).toordinal(), xmax=salt_Xgrid.max(), color='k')
ax2.clabel(lines2, lines2.levels, inline=True, fontsize=10)
ax2.invert_yaxis()
ax2.set_ylabel('Depth (m)')
# ax2.text(datetime(2022,10,20).toordinal(), 530, 'Salinity Anomaly', fontsize='large')
ax2.set_xlabel('Year')
ax2.set_yticks((0, 200, 400, 600))
ax2.set_xticks((datetime(2015,1,1).toordinal(), datetime(2016,1,1).toordinal(), datetime(2017,1,1).toordinal(), datetime(2018,1,1).toordinal(), datetime(2019,1,1).toordinal(), datetime(2020,1,1).toordinal(), datetime(2021,1,1).toordinal(),
               datetime(2022,1,1).toordinal(), datetime(2023,1,1).toordinal(), datetime(2024,1,1).toordinal(), datetime(2025,1,1).toordinal()))
ax2.set_xticklabels(('2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024', '2025'))
ax2.set_xlim(datetime(2025,3,1).toordinal(), datetime(2026,1,1).toordinal())
ax2.set_ylim(600, 0)
ax2.spines[:].set_linewidth(2)
ax2.tick_params(width=2, top=True, right=True, direction='in')
cbar2 = plt.colorbar(plot2, shrink=0.5, location='right', pad=0.015)
cbar2.outline.set_linewidth(2)
cbar2.set_label(label=r'(PSU)', rotation=0, labelpad=10)
plt.tight_layout()
plt.savefig(f'C:/Users/marqjace/OneDrive - Oregon State University/Desktop/Python/TH-Line_timeseries/figures/t_anom_timeseries_recent_{timestamp}.png')

# Plot the figure: Trinidad Head Averaged Over Inshore 200km (Filtered)
print(f'Plotting t_anom_timeseries_{timestamp}.png...')
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14,8), dpi=300)

plot1 = ax1.contourf(temp_Xgrid, temp_Ygrid, temp_box, cmap='RdYlBu_r', norm=divnorm_temp, levels=boundaries_temp)
lines1 = ax1.contour(temp_Xgrid, temp_Ygrid, temp_box, colors='black', norm=divnorm_temp, levels=levels_temp, alpha=0.75)
deployment1_nov_14 = ax1.hlines(y=570, xmin=datetime(2014,12,4).toordinal(), xmax=datetime(2015,3,9).toordinal(), color='k')
deployment1_mar_15 = ax1.hlines(y=570, xmin=datetime(2015,3,9).toordinal(), xmax=datetime(2015,9,17).toordinal(), color='k')
deployment1_sep_15 = ax1.hlines(y=570, xmin=datetime(2015,9,17).toordinal(), xmax=datetime(2016,5,16).toordinal(), color='k')
deployment1_may_16 = ax1.hlines(y=570, xmin=datetime(2016,5,23).toordinal(), xmax=datetime(2016,10,21).toordinal(), color='k')
deployment1_oct_16 = ax1.hlines(y=570, xmin=datetime(2016,10,21).toordinal(), xmax=datetime(2017,6,5).toordinal(), color='k')
deployment1_jun_17 = ax1.hlines(y=570, xmin=datetime(2017,6,5).toordinal(), xmax=datetime(2017,11,6).toordinal(), color='k')
deployment1_apr_18 = ax1.hlines(y=570, xmin=datetime(2018,4,17).toordinal(), xmax=datetime(2018,10,2).toordinal(), color='k')
deployment1_nov_18 = ax1.hlines(y=570, xmin=datetime(2018,11,7).toordinal(), xmax=datetime(2019,4,9).toordinal(), color='k')
deployment1_apr_19 = ax1.hlines(y=570, xmin=datetime(2019,4,9).toordinal(), xmax=datetime(2019,8,19).toordinal(), color='k')
deployment1_sep_19 = ax1.hlines(y=570, xmin=datetime(2019,9,16).toordinal(), xmax=datetime(2020,3,19).toordinal(), color='k')
deployment1_sep_20 = ax1.hlines(y=570, xmin=datetime(2020,9,16).toordinal(), xmax=datetime(2021,2,6).toordinal(), color='k')
deployment1_nov_21 = ax1.hlines(y=570, xmin=datetime(2021,11,12).toordinal(), xmax=datetime(2022,6,16).toordinal(), color='k')
deployment1_jul_22 = ax1.hlines(y=570, xmin=datetime(2022,7,29).toordinal(), xmax=datetime(2023,1,26).toordinal(), color='k')
deployment1_jan_23 = ax1.hlines(y=570, xmin=datetime(2023,1,26).toordinal(), xmax=datetime(2023,8,14).toordinal(), color='k')
deployment1_oct_23 = ax1.hlines(y=570, xmin=datetime(2023,10,13).toordinal(), xmax=datetime(2024,4,12).toordinal(), color='k')
deployment1_apr_24 = ax1.hlines(y=570, xmin=datetime(2024,4,12).toordinal(), xmax=datetime(2024,8,9).toordinal(), color='k')
deployment1_oct_24 = ax1.hlines(y=570, xmin=datetime(2024,10,21).toordinal(), xmax=datetime(2024,12,4).toordinal(), color='k')
deployment1_mar_25 = ax1.hlines(y=570, xmin=datetime(2025,3,21).toordinal(), xmax=temp_Xgrid.max(), color='k')
ax1.clabel(lines1, lines1.levels, inline=True, fontsize=10)
ax1.invert_yaxis()
ax1.set_ylabel('Depth (m)')
ax1.text(datetime(2022,7,15).toordinal(), 530, 'Temperature Anomaly', fontsize='large')
ax1.set_yticks((0, 200, 400, 600))
ax1.set_xticks((datetime(2015,1,1).toordinal(), datetime(2016,1,1).toordinal(), datetime(2017,1,1).toordinal(), datetime(2018,1,1).toordinal(), datetime(2019,1,1).toordinal(), datetime(2020,1,1).toordinal(), datetime(2021,1,1).toordinal(),
               datetime(2022,1,1).toordinal(), datetime(2023,1,1).toordinal(), datetime(2024,1,1).toordinal(), datetime(2025,1,1).toordinal()))
ax1.set_xticklabels(('2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024', '2025'))
ax1.set_xlim(datetime(2014,12,4).toordinal(), datetime(2026,1,1).toordinal())
ax1.set_ylim(600, 0)
ax1.spines[:].set_linewidth(2)
ax1.tick_params(width=2, top=True, right=True, direction='in')
ax1.set_title('Trinidad Head Averaged Over Inshore 200km (Filtered)', pad=10)
cbar1 = plt.colorbar(plot1, shrink=0.5, location='right', pad=0.015)
cbar1.outline.set_linewidth(2)
cbar1.set_label(label=r'($\degree$C)', rotation=0, labelpad=10)

plot2 = ax2.contourf(salt_Xgrid, salt_Ygrid, salt_box, cmap='BrBG_r', norm=divnorm_salt, levels=boundaries_salt)
lines2 = ax2.contour(salt_Xgrid, salt_Ygrid, salt_box, colors='black', norm=divnorm_salt, levels=levels_salt, alpha=0.75)
deployment2_nov_14 = ax2.hlines(y=570, xmin=datetime(2014,12,4).toordinal(), xmax=datetime(2015,3,9).toordinal(), color='k')
deployment2_mar_15 = ax2.hlines(y=570, xmin=datetime(2015,3,9).toordinal(), xmax=datetime(2015,9,17).toordinal(), color='k')
deployment2_sep_15 = ax2.hlines(y=570, xmin=datetime(2015,9,17).toordinal(), xmax=datetime(2016,5,16).toordinal(), color='k')
deployment2_may_16 = ax2.hlines(y=570, xmin=datetime(2016,5,23).toordinal(), xmax=datetime(2016,10,21).toordinal(), color='k')
deployment2_oct_16 = ax2.hlines(y=570, xmin=datetime(2016,10,21).toordinal(), xmax=datetime(2017,6,5).toordinal(), color='k')
deployment2_jun_17 = ax2.hlines(y=570, xmin=datetime(2017,6,5).toordinal(), xmax=datetime(2017,11,6).toordinal(), color='k')
deployment2_apr_18 = ax2.hlines(y=570, xmin=datetime(2018,4,17).toordinal(), xmax=datetime(2018,10,2).toordinal(), color='k')
deployment2_nov_18 = ax2.hlines(y=570, xmin=datetime(2018,11,7).toordinal(), xmax=datetime(2019,4,9).toordinal(), color='k')
deployment2_apr_19 = ax2.hlines(y=570, xmin=datetime(2019,4,9).toordinal(), xmax=datetime(2019,8,19).toordinal(), color='k')
deployment2_sep_19 = ax2.hlines(y=570, xmin=datetime(2019,9,16).toordinal(), xmax=datetime(2020,3,19).toordinal(), color='k')
deployment2_sep_20 = ax2.hlines(y=570, xmin=datetime(2020,9,16).toordinal(), xmax=datetime(2021,2,6).toordinal(), color='k')
deployment2_nov_21 = ax2.hlines(y=570, xmin=datetime(2021,11,12).toordinal(), xmax=datetime(2022,6,16).toordinal(), color='k')
deployment2_jul_22 = ax2.hlines(y=570, xmin=datetime(2022,7,29).toordinal(), xmax=datetime(2023,1,26).toordinal(), color='k')
deployment2_jan_23 = ax2.hlines(y=570, xmin=datetime(2023,1,26).toordinal(), xmax=datetime(2023,8,14).toordinal(), color='k')
deployment2_oct_23 = ax2.hlines(y=570, xmin=datetime(2023,10,13).toordinal(), xmax=datetime(2024,4,12).toordinal(), color='k')
deployment2_apr_24 = ax2.hlines(y=570, xmin=datetime(2024,4,12).toordinal(), xmax=datetime(2024,8,9).toordinal(), color='k')
deployment2_oct_24 = ax2.hlines(y=570, xmin=datetime(2024,10,21).toordinal(), xmax=datetime(2024,12,4).toordinal(), color='k')
deployment2_mar_25 = ax2.hlines(y=570, xmin=datetime(2025,3,21).toordinal(), xmax=salt_Xgrid.max(), color='k')
ax2.clabel(lines2, lines2.levels, inline=True, fontsize=10)
ax2.invert_yaxis()
ax2.set_ylabel('Depth (m)')
ax2.text(datetime(2022,10,20).toordinal(), 530, 'Salinity Anomaly', fontsize='large')
ax2.set_xlabel('Year')
ax2.set_yticks((0, 200, 400, 600))
ax2.set_xticks((datetime(2015,1,1).toordinal(), datetime(2016,1,1).toordinal(), datetime(2017,1,1).toordinal(), datetime(2018,1,1).toordinal(), datetime(2019,1,1).toordinal(), datetime(2020,1,1).toordinal(), datetime(2021,1,1).toordinal(),
               datetime(2022,1,1).toordinal(), datetime(2023,1,1).toordinal(), datetime(2024,1,1).toordinal(), datetime(2025,1,1).toordinal()))
ax2.set_xticklabels(('2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024', '2025'))
ax2.set_xlim(datetime(2014,12,4).toordinal(), datetime(2026,1,1).toordinal())
ax2.set_ylim(600, 0)
ax2.spines[:].set_linewidth(2)
ax2.tick_params(width=2, top=True, right=True, direction='in')
cbar2 = plt.colorbar(plot2, shrink=0.5, location='right', pad=0.015)
cbar2.outline.set_linewidth(2)
cbar2.set_label(label=r'(PSU)', rotation=0, labelpad=10)
plt.tight_layout()
plt.savefig(f'C:/Users/marqjace/OneDrive - Oregon State University/Desktop/Python/TH-Line_timeseries/figures/t_anom_timeseries_{timestamp}.png')


# Plot the figure: Grid
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14,8), dpi=300)

scat1 = ax1.scatter(temp_Xgrid, temp_Ygrid, s=2)
deployment1_nov_14 = ax1.hlines(y=570, xmin=datetime(2014,12,4).toordinal(), xmax=datetime(2015,3,9).toordinal(), color='k')
deployment1_sep_15 = ax1.hlines(y=570, xmin=datetime(2015,9,17).toordinal(), xmax=datetime(2016,5,16).toordinal(), color='k')
deployment1_may_16 = ax1.hlines(y=570, xmin=datetime(2016,5,23).toordinal(), xmax=datetime(2016,10,21).toordinal(), color='k')
deployment1_oct_16 = ax1.hlines(y=570, xmin=datetime(2016,10,21).toordinal(), xmax=datetime(2017,6,5).toordinal(), color='k')
deployment1_jun_17 = ax1.hlines(y=570, xmin=datetime(2017,6,5).toordinal(), xmax=datetime(2017,11,6).toordinal(), color='k')
deployment1_apr_18 = ax1.hlines(y=570, xmin=datetime(2018,4,17).toordinal(), xmax=datetime(2018,10,2).toordinal(), color='k')
deployment1_nov_18 = ax1.hlines(y=570, xmin=datetime(2018,11,7).toordinal(), xmax=datetime(2019,4,9).toordinal(), color='k')
deployment1_apr_19 = ax1.hlines(y=570, xmin=datetime(2019,4,9).toordinal(), xmax=datetime(2019,8,19).toordinal(), color='k')
deployment1_sep_19 = ax1.hlines(y=570, xmin=datetime(2019,9,16).toordinal(), xmax=datetime(2020,3,19).toordinal(), color='k')
deployment1_sep_20 = ax1.hlines(y=570, xmin=datetime(2020,9,16).toordinal(), xmax=datetime(2021,2,6).toordinal(), color='k')
deployment1_nov_21 = ax1.hlines(y=570, xmin=datetime(2021,11,12).toordinal(), xmax=datetime(2022,6,16).toordinal(), color='k')
deployment1_jul_22 = ax1.hlines(y=570, xmin=datetime(2022,7,29).toordinal(), xmax=datetime(2023,1,26).toordinal(), color='k')
deployment1_jan_23 = ax1.hlines(y=570, xmin=datetime(2023,1,26).toordinal(), xmax=datetime(2023,8,14).toordinal(), color='k')
deployment1_oct_23 = ax1.hlines(y=570, xmin=datetime(2023,10,13).toordinal(), xmax=datetime(2024,4,12).toordinal(), color='k')
deployment1_apr_24 = ax1.hlines(y=570, xmin=datetime(2024,4,12).toordinal(), xmax=datetime(2024,8,9).toordinal(), color='k')
deployment1_oct_24 = ax1.hlines(y=570, xmin=datetime(2024,10,21).toordinal(), xmax=datetime(2024,12,4).toordinal(), color='k')
deployment1_mar_25 = ax1.hlines(y=570, xmin=datetime(2025,3,21).toordinal(), xmax=temp_Xgrid.max(), color='k')
# ax1.clabel(lines1, lines1.levels, inline=True, fontsize=10)
ax1.invert_yaxis()
ax1.set_ylabel('Depth (m)')
ax1.text(datetime(2022,8,1).toordinal(), 530, 'Temperature Anomaly', fontsize='large')
ax1.set_yticks((0, 200, 400, 600))
ax1.set_xticks((datetime(2015,1,1).toordinal(), datetime(2016,1,1).toordinal(), datetime(2017,1,1).toordinal(), datetime(2018,1,1).toordinal(), datetime(2019,1,1).toordinal(), datetime(2020,1,1).toordinal(), datetime(2021,1,1).toordinal(),
               datetime(2022,1,1).toordinal(), datetime(2023,1,1).toordinal(), datetime(2024,1,1).toordinal(), datetime(2025,1,1).toordinal()))
ax1.set_xticklabels(('2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024', '2025'))
ax1.set_xlim(datetime(2014,12,4).toordinal(), datetime(2026,1,1).toordinal())
ax1.set_ylim(600, 0)
ax1.spines[:].set_linewidth(2)
ax1.tick_params(width=2, top=True, right=True, direction='in')
ax1.set_title('Trinidad Head Averaged Over Inshore 200km', pad=10)
cbar1 = plt.colorbar(scat1, shrink=0.5, location='right', pad=0.015)
cbar1.outline.set_linewidth(2)
cbar1.set_label(label=r'($\degree$C)', rotation=0, labelpad=10)

scat2 = ax2.scatter(salt_Xgrid, salt_Ygrid, s=2)
deployment2_nov_14 = ax2.hlines(y=570, xmin=datetime(2014,12,4).toordinal(), xmax=datetime(2015,3,9).toordinal(), color='k')
deployment2_sep_15 = ax2.hlines(y=570, xmin=datetime(2015,9,17).toordinal(), xmax=datetime(2016,5,16).toordinal(), color='k')
deployment2_may_16 = ax2.hlines(y=570, xmin=datetime(2016,5,23).toordinal(), xmax=datetime(2016,10,21).toordinal(), color='k')
deployment2_oct_16 = ax2.hlines(y=570, xmin=datetime(2016,10,21).toordinal(), xmax=datetime(2017,6,5).toordinal(), color='k')
deployment2_jun_17 = ax2.hlines(y=570, xmin=datetime(2017,6,5).toordinal(), xmax=datetime(2017,11,6).toordinal(), color='k')
deployment2_apr_18 = ax2.hlines(y=570, xmin=datetime(2018,4,17).toordinal(), xmax=datetime(2018,10,2).toordinal(), color='k')
deployment2_nov_18 = ax2.hlines(y=570, xmin=datetime(2018,11,7).toordinal(), xmax=datetime(2019,4,9).toordinal(), color='k')
deployment2_apr_19 = ax2.hlines(y=570, xmin=datetime(2019,4,9).toordinal(), xmax=datetime(2019,8,19).toordinal(), color='k')
deployment2_sep_19 = ax2.hlines(y=570, xmin=datetime(2019,9,16).toordinal(), xmax=datetime(2020,3,19).toordinal(), color='k')
deployment2_sep_20 = ax2.hlines(y=570, xmin=datetime(2020,9,16).toordinal(), xmax=datetime(2021,2,6).toordinal(), color='k')
deployment2_nov_21 = ax2.hlines(y=570, xmin=datetime(2021,11,12).toordinal(), xmax=datetime(2022,6,16).toordinal(), color='k')
deployment2_jul_22 = ax2.hlines(y=570, xmin=datetime(2022,7,29).toordinal(), xmax=datetime(2023,1,26).toordinal(), color='k')
deployment2_jan_23 = ax2.hlines(y=570, xmin=datetime(2023,1,26).toordinal(), xmax=datetime(2023,8,14).toordinal(), color='k')
deployment2_oct_23 = ax2.hlines(y=570, xmin=datetime(2023,10,13).toordinal(), xmax=datetime(2024,4,12).toordinal(), color='k')
deployment2_apr_24 = ax2.hlines(y=570, xmin=datetime(2024,4,12).toordinal(), xmax=datetime(2024,8,9).toordinal(), color='k')
deployment2_oct_24 = ax2.hlines(y=570, xmin=datetime(2024,10,21).toordinal(), xmax=datetime(2024,12,4).toordinal(), color='k')
deployment2_mar_25 = ax2.hlines(y=570, xmin=datetime(2025,3,21).toordinal(), xmax=salt_Xgrid.max(), color='k')
# ax2.clabel(lines2, lines2.levels, inline=True, fontsize=10)
ax2.invert_yaxis()
ax2.set_ylabel('Depth (m)')
ax2.text(datetime(2022,11,1).toordinal(), 530, 'Salinity Anomaly', fontsize='large')
ax2.set_xlabel('Year')
ax2.set_yticks((0, 200, 400, 600))
ax2.set_xticks((datetime(2015,1,1).toordinal(), datetime(2016,1,1).toordinal(), datetime(2017,1,1).toordinal(), datetime(2018,1,1).toordinal(), datetime(2019,1,1).toordinal(), datetime(2020,1,1).toordinal(), datetime(2021,1,1).toordinal(),
               datetime(2022,1,1).toordinal(), datetime(2023,1,1).toordinal(), datetime(2024,1,1).toordinal(), datetime(2025,1,1).toordinal()))
ax2.set_xticklabels(('2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024', '2025'))
ax2.set_xlim(datetime(2014,12,4).toordinal(), datetime(2026,1,1).toordinal())
ax2.set_ylim(600, 0)
ax2.spines[:].set_linewidth(2)
ax2.tick_params(width=2, top=True, right=True, direction='in')
# ax2.set_title('Salinity Anomaly', pad=10)
cbar2 = plt.colorbar(scat2, shrink=0.5, location='right', pad=0.015)
cbar2.outline.set_linewidth(2)
cbar2.set_label(label=r'(PSU)', rotation=0, labelpad=10)
plt.tight_layout()
plt.savefig(f'C:/Users/marqjace/OneDrive - Oregon State University/Desktop/Python/TH-Line_timeseries/figures/t_anom_grid_{timestamp}.png')


# Plot the figure: Temperature Anomaly Indices
print(f'Plotting t_anom_indices_MOCI_{timestamp}.png...')
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
ax.set_xlim(datetime(2006,6,1).toordinal(), datetime(2026,1,1).toordinal())
ax.spines[:].set_linewidth(2)
ax.tick_params(width=2, top=True, right=False, direction='in')
ax2.spines[:].set_linewidth(2)
ax2.tick_params(width=2, top=True, right=True, direction='in')
plt.title('Temperature Anomaly Indices', pad=15, fontsize='x-large')
lns = oni_plot + scti_plot + thi_plot + moci_plot
labs = [l.get_label() for l in lns]
ax.legend(lns, labs, loc=2, frameon=False, fontsize='x-large', labelcolor='linecolor')
plt.axvspan(datetime(2006,6,1).toordinal(), datetime(2026,1,1).toordinal(), ymin=0, ymax=0.35, alpha=0.15, color='gray')
plt.tight_layout()
plt.savefig(f'C:/Users/marqjace/OneDrive - Oregon State University/Desktop/Python/TH-Line_timeseries/figures/t_anom_indices_MOCI_{timestamp}.png')


# Plot the figure: Temperature Anomaly Indices
print(f'Plotting t_anom_indices_{timestamp}.png...')
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
# ax2.set_ylabel(r'MOCI Index', fontsize='x-large')
# ax2.set_ylim(-8, 15)
# ax2.set_yticks([-4, 0, 4, 8, 12])
# ax2.set_yticklabels(['-4', '0', '4', '8', '12'])
ax.set_xlabel('Year', fontsize='x-large')
ax.set_xlim(datetime(2006,6,1).toordinal(), datetime(2026,1,1).toordinal())
ax.spines[:].set_linewidth(2)
ax.tick_params(width=2, top=True, right=False, direction='in')
# ax2.spines[:].set_linewidth(2)
# ax2.tick_params(width=2, top=True, right=True, direction='in')
plt.title('Temperature Anomaly Indices', pad=15, fontsize='x-large')
lns = oni_plot + scti_plot + thi_plot
labs = [l.get_label() for l in lns]
ax.legend(lns, labs, loc=2, frameon=False, fontsize='x-large', labelcolor='linecolor')
plt.axvspan(datetime(2006,6,1).toordinal(), datetime(2026,1,1).toordinal(), ymin=0, ymax=0.35, alpha=0.15, color='gray')
plt.tight_layout()
plt.savefig(f"C:/Users/marqjace/OneDrive - Oregon State University/Desktop/Python/TH-Line_timeseries/figures/t_anom_indices_{timestamp}.png")

print("Done!")