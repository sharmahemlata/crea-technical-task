# https://help.marine.copernicus.eu/en/articles/5029956-how-to-convert-netcdf-to-geotiff#h_088eb0feb8

import xarray as xr
import cdsapi
import rioxarray
import warnings
import argparse
import datetime

from matplotlib import pyplot as plt

warnings.filterwarnings("ignore")


def get_o3_mass_mixing_geotiff(day, month, year):
    c = cdsapi.Client()
    c.retrieve(
        'reanalysis-era5-pressure-levels',
        {
            'product_type': 'reanalysis',
            'format': 'netcdf',
            'variable': 'ozone_mass_mixing_ratio',
            'pressure_level': '850',
            'year': year,
            'month': month,
            'day': day,
            'time': [
                '00:00', '01:00', '02:00',
                '03:00', '04:00', '05:00',
                '06:00', '07:00', '08:00',
                '09:00', '10:00', '11:00',
                '12:00', '13:00', '14:00',
                '15:00', '16:00', '17:00',
                '18:00', '19:00', '20:00',
                '21:00', '22:00', '23:00',
            ],
        },
        'download.nc')

    nc_file = xr.open_dataset('download.nc')
    nc_file = nc_file.resample(time='1D').mean()

    bT = nc_file['o3']
    bT = bT.rio.set_spatial_dims(x_dim='longitude', y_dim='latitude')
    bT.rio.write_crs("epsg:4326", inplace=True)
    bT.rio.to_raster(r"out.tiff")

    bT.plot()
    plt.savefig("out.png")


parser = argparse.ArgumentParser(description='Build global raster (geotiff) of average Ozone mass mixing ratio at 850hPa of any given day')
parser.add_argument('date', metavar='d', type=lambda s: datetime.datetime.strptime(s, '%d/%m/%Y'),
                    help='Date in format dd/mm/yyyy')
args = parser.parse_args()

get_o3_mass_mixing_geotiff(
                           str(args.date.day),
                           str(args.date.month), 
                           str(args.date.year)
                           )
