
from arcgis.gis import GIS
import arcgis
import datetime
import time
import arcpy
import pandas as pd

gis = GIS("pro")


# Access the service

naip_item = gis.content.get("3f8d2d3828f24c00ae279db4af26d566")
naip_lyr = naip_item.layers[0]


model_item = gis.content.get("a10f46a8071a4318bcc085dae26d7ee4") # naip
model_local = model_item.download(save_path = r".", file_name = model_item.name) 

name = 'acquisition_date_test'
in_extent = (-13530675.228816083, 4545237.670432766, -13528866.137925146, 4547533.238415405) # this one is good
# in_extent = (-13531724.345844738, 4545036.586488164, -13528757.599476013, 4550120.3308824245) # this doesn't work
# in_extent = (-13531729.73726924, 4545151.197054078, -13528776.701236999, 4548344.528062875)
xmin, ymin, xmax, ymax = in_extent


extent = {'xmin': xmin,
  'ymin': ymin,
  'xmax': xmax,
  'ymax': ymax,
  'spatialReference': {'wkid': 3857}}

envelope = arcgis.geometry.Envelope(extent)    

df = naip_lyr.query(
    "AcquisitionDate IS NOT NULL",
    geometry_filter = arcgis.geometry.filters.intersects(
        geometry=envelope, 
        sr=envelope.spatial_reference),
    as_df=True,
    # return_geometry=False
    )


df['query_date'] = df.AcquisitionDate.apply(lambda  x: int(time.mktime(pd.to_datetime(x, unit='ms').timetuple())*1000))

df['agol_date'] = df.AcquisitionDate.apply(lambda  x: pd.to_datetime(x, unit='ms'))

# Convert a target date (e.g., June 17, 2021) to a unix timestamp
# we know NAIP was collected on 6/17/2021 over this area by manual inspection of the dataset
filter_date_dt = datetime.datetime(2022, 5, 17)
filter_date_unix = int(time.mktime(filter_date_dt.timetuple()) * 1000)
filter_date_unix


# Calculate height and width of output image
naip_res = 1 # NAIP resolution in 1 meter
metersPerUnit = 1



w = int((xmax - xmin) * metersPerUnit / naip_res)
h = int((ymax - ymin) * metersPerUnit / naip_res)

for filter_date_unix in df.AcquisitionDate.values:

    datestring = datetime.datetime.fromtimestamp(filter_date_unix/1000).strftime('%Y-%m-%d')

    natural_color = naip_lyr.export_image(
        bbox=envelope, 
        bbox_sr=3857, 
        image_sr=3857, 
        size=[w,h], 
        export_format='tiff',
        time=filter_date_unix,
        rendering_rule = {'rasterFunction': "NaturalColor"},
        f = "image",
        save_folder = r".",
        save_file = rf"{name}_{datestring}.tif",
        )
