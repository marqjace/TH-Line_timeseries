# Template for Opening & Merging Individual Dives
# Created by Jace Marquardt on 02/06/2025

# Imports
import glidertools as gt

def merge_seaglider_data(filenames, output_filename):
    # Load Variables
    gt.load.seaglider_show_variables(filenames)

    # Define Variables
    names = [
        'ctd_depth',
        'ctd_time',
        'ctd_pressure',
        'salinity',
        'temperature',
        # 'aanderaa4831_dissolved_oxygen',
        # 'aanderaa4330_dissolved_oxygen',
        # 'sbe43_dissolved_oxygen'
    ]

    # Load Data into Dictionary
    ds_dict = gt.load.seaglider_basestation_netCDFs(
        filenames, names,
        return_merged=True,
        keep_global_attrs=False
    )

    # Print Keys
    print(ds_dict.keys())

    # Rename Variables
    ctd_data_point = ds_dict['ctd_data_point']

    dat = ctd_data_point.rename({
        'salinity': 'salt_raw',
        'temperature': 'temp_raw',
        'ctd_pressure': 'pressure',
        'ctd_depth': 'depth',
        'ctd_time': 'time_raw',
        # 'aanderaa4831_dissolved_oxygen': 'oxygen',
        # 'aanderaa4330_dissolved_oxygen': 'oxygen',
        # 'sbe43_dissolved_oxygen': 'oxygen'
    })

    print(dat)

    # Save Merged File to NetCDF
    dat.to_netcdf(output_filename)

# Example usage
filenames = 'C:/Users/marqjace/TH_line/deployments/mar_2025/transect2/p266*.nc'
output_filename = 'C:/Users/marqjace/TH_line/deployments/mar_2025/transect2/4_25_merged.nc'
merge_seaglider_data(filenames, output_filename)
