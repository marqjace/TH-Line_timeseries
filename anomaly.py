# Function to calculate the temperature anomaly
# Created by Jace Marquardt
# Last updated 04-12-2025

import numpy as np

def temperature_anomaly(transect_dict, woa_dict):
    """Creates a list of temperature anomaly transects using the transects data and WOA data."""
    
    temp_anomaly = []

    for key, value in transect_dict.items():
        # Split by underscore and take the first part
        month_number = key.split('_')[0]

        for key2, value2 in woa_dict.items():
            if month_number == key2:
                anomaly = np.subtract(value, value2)
                temp_anomaly.append(anomaly)
    
    return temp_anomaly

def salinity_anomaly(transect_dict, woa_dict):
    """Creates a list of salinity anomaly transects using the transects data and WOA data."""
    
    salt_anomaly = []

    for key, value in transect_dict.items():
        # Split by underscore and take the first part
        month_number = key.split('_')[0]

        for key2, value2 in woa_dict.items():
            if month_number == key2:
                anomaly = np.subtract(value, value2)
                salt_anomaly.append(anomaly)
    
    return salt_anomaly