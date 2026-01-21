# Template for Opening & Merging Individual Dives
# Created by Jace Marquardt on 12/02/2025

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
        # 'salinity_corrected',
        # 'aanderaa4831_dissolved_oxygen',
        # 'fet_Ik',
        # 'fet_pumptime_b',
        # 'aanderaa4330_dissolved_oxygen',
        # 'sbe43_dissolved_oxygen'
    ]

    # Load Data into Dictionary
    ds_dict = gt.load.seaglider_basestation_netCDFs(
        filenames, names,
        return_merged=False,
        keep_global_attrs=False,
    )

    # Print Keys
    print(ds_dict.keys())

    # Rename Variables
    ctd_data_point = ds_dict['sg_data_point']

    if 'salinity_corrected' in ctd_data_point:
        dat = ctd_data_point.rename({
            'salinity': 'salt_raw',
            'temperature': 'temp_raw',
            'ctd_pressure': 'pressure',
            'ctd_depth': 'depth',
            'ctd_time': 'time_raw',
            # 'salinity_corrected': 'salt_corrected',
            # 'aanderaa4831_dissolved_oxygen': 'oxygen',
            # 'aanderaa4330_dissolved_oxygen': 'oxygen',
            # 'sbe43_dissolved_oxygen': 'oxygen'
        })
    else:
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
    dat.close()

    # dat = ds_dict['fet_data_point']
    # dat.to_netcdf(output_filename)
    # dat.close()

# Example usage
filenames = r'C:/Users/marqjace/TH_line/deployments/nov_2025/transect3/p686*.nc'
output_filename = r'C:/Users/marqjace/TH_line/deployments/nov_2025/transect3/1_26_merged.nc'
merge_seaglider_data(filenames, output_filename)
