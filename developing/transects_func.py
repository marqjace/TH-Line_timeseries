import os
import numpy as np
import xarray as xr
import pandas as pd
from scipy.interpolate import griddata

def make_transect_grid(xmin=-126.625, xmax=-124.375, ymin=0, ymax=1000, xn=36, yn=200):
    x = np.linspace(xmin, xmax, xn)
    y = np.linspace(ymin, ymax, yn)

    return np.meshgrid(x, y)

def interp_to_grid(lon, depth, values, Xgrid, Ygrid):
    return griddata(
        points=(lon.values, depth.values),
        values=values.values,
        xi=(Xgrid, Ygrid),
        method="linear"
    )

def transect(filepath, Xgrid, Ygrid):
    ds = xr.open_dataset(filepath, drop_variables=['compass_timeouts_times_truck'])

    time = ds.time_raw
    mean_time = time.mean().values
    mean_time_pd = pd.to_datetime(mean_time)
    lon = ds.longitude
    depth = ds.depth

    out = {
        "lon": lon,
        "depth": depth,
        "time": time,
        "temp_interp": interp_to_grid(lon, depth, ds.temp_raw, Xgrid, Ygrid),
        "salt_interp": interp_to_grid(lon, depth, ds.salt_raw, Xgrid, Ygrid),
        "mean_time": mean_time_pd,
    }

    if "salt_corrected" in ds:
        out["salt_corrected_interp"] = interp_to_grid(
            lon, depth, ds.salt_corrected, Xgrid, Ygrid
        )

    return out

def process_transects(filepaths):
    Xgrid, Ygrid = make_transect_grid()

    results = {}
    for i, fp in enumerate(filepaths, start=1):
        # Extract the base filename without extension
        base = os.path.basename(fp)          # '10_25_b_merged.nc'
        name = base.split('_merged')[0]      # '10_25_b'
        
        print(f"Processing {i}/{len(filepaths)} {name}...")
        results[name] = transect(fp, Xgrid, Ygrid)

    # Convenience dictionaries
    temps = {
        k: {
            "temp": v["temp_interp"],
            "mean_time": v["mean_time"],
        }
        for k, v in results.items()
    }
    salts = {
    k: {
        "salt": v["salt_corrected_interp"] if "salt_corrected_interp" in v else v["salt_interp"],
        "mean_time": v["mean_time"],
    }
    for k, v in results.items()
    }

    print(f"Processing complete.\n")
    return results, temps, salts

# def timeseries_grid(time_min, time_max, temp_anom, depth):
#     xgrid = np.arange(time_min, time_max, np.timedelta64(30, 'D')) # Every 30 days in time
#     ygrid = np.arange(0,1000,5) # Every 5m in depth
    
#     Xgrid, Ygrid = np.meshgrid(xgrid, ygrid)

#     return griddata(
#         points=(temp_anom.values, depth.values),
#         values=values.values,
#         xi=(Xgrid, Ygrid),
#         method="linear"
#     )



