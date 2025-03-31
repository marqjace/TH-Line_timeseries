import numpy as np
import xarray as xr
from pathlib import Path
from scipy.interpolate import griddata

# Set grid dimensions: (36 points from -126.625 to -124.375)
    #                    x (200 points from 0 to 1000m) 
    #                    = one point every 5km lon and every 5m depth
xn, yn = 36, 200
xmin, xmax = -126.625, -124.375
ymin, ymax = 0, 1000

# Dictionaries to store the interpolated data arrays
temperature_data = {}
salinity_data = {}

def standardize_dimension(ds):
    """
    Standardize the dimension names of a dataset. 
    Ex: SG266 uses 'ctd_data_point' instead of 'sg_data_point'.
    """
    if 'ctd_data_point' in ds.dims:
        ds = ds.rename({'ctd_data_point': 'sg_data_point'})
    return ds

def process_transect(filepath, transect_name):
    """Process a single transect file."""
    ds = xr.open_dataset(filepath, decode_times=False)
    ds = standardize_dimension(ds)

    # Check the shapes and content of longitude and depth
    if 'longitude' in ds.variables and 'depth' in ds.variables:
        # Perform interpolation
        try:
            # Extract the data points
            points = np.array([ds['longitude'].values, ds['depth'].values]).T
            temp_values = ds['temp_raw'].values
            salt_values = ds['salt_raw'].values

            # Create the grid
            grid_lon, grid_depth = np.meshgrid(np.linspace(xmin, xmax, xn), np.linspace(ymin, ymax, yn))
            grid_points = np.array([grid_lon.flatten(), grid_depth.flatten()]).T
            
            # Interpolate the data
            temp_interp = griddata(points, temp_values, grid_points, method='linear')
            temp_interp = temp_interp.reshape((yn, xn))

            salt_interp = griddata(points, salt_values, grid_points, method='linear')
            salt_interp = salt_interp.reshape((yn, xn))
            
            # Create an xarray DataArray for the interpolated data
            temp_interp_da = xr.DataArray(temp_interp, coords={'depth': np.linspace(ymin, ymax, yn), 'longitude': np.linspace(xmin, xmax, xn)}, dims=['depth', 'longitude'])
            salt_interp_da = xr.DataArray(salt_interp, coords={'depth': np.linspace(ymin, ymax, yn), 'longitude': np.linspace(xmin, xmax, xn)}, dims=['depth', 'longitude'])
            
            # Save the interpolated data arrays in the dictionaries
            temperature_data[transect_name] = temp_interp_da
            salinity_data[transect_name] = salt_interp_da
            
            return {'temperature': temp_interp_da, 'salinity': salt_interp_da}
        
        except Exception as e:
            print(f"Error during interpolation: {e}")
            return None
    else:
        print("Longitude or Depth variables are not available.")
        return None

def batch_process(filepaths):
    """Process multiple transect files and return a dictionary of results."""
    results = {}
    for i, filepath in enumerate(filepaths, start=1):
        print(f"Processing {Path(filepath).name} ({i}/{len(filepaths)})...")
        transect_name = Path(filepath).stem.replace('_merged', '')
        results[transect_name] = process_transect(filepath, transect_name)
    print("Processing complete.")
    return results

# transects = batch_process(filepaths)

# # Example of accessing individual transects and their data
# for transect_name, data_dict in transects.items():
#     if data_dict is not None:
#         print(f"Transect: {transect_name}")
#         temperature_data = data_dict['temperature']
#         salinity_data = data_dict['salinity']
        
#         # Print some information about the data
#         print(f"Temperature DataArray: {temperature_data}")
#         print(f"Salinity DataArray: {salinity_data}")
        
#         # Access specific values or perform operations on the data
#         print(f"Temperature values: {temperature_data.values}")
#         print(f"Salinity values: {salinity_data.values}")
#     else:
#         print(f"Transect: {transect_name} has no data.")