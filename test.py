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

    # Save Merged File to NetCDF
    ds_dict.to_netcdf(output_filename)
    ds_dict.close()

# Example usage
filenames = r'C:\Users\marqjace\seaglider\sg686\TH_Line_11Nov25\p686*.nc'
output_filename = r'C:\Users\marqjace\seaglider\sg686\TH_Line_11Nov25\sg686_merged.nc'
merge_seaglider_data(filenames, output_filename)
