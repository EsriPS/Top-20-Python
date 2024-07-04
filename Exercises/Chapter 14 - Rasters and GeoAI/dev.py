from arcgis.gis import GIS
import arcgis
import datetime
import time
import arcpy

gis = GIS("Pro")


# Access the service

naip_item = gis.content.get("3f8d2d3828f24c00ae279db4af26d566")

naip_item



naip_lyr = naip_item.layers[0]
naip_lyr # NaturalColor



for fn in naip_lyr.properties.rasterFunctionInfos:
    print(fn['name'] + ": " + fn['description'] + "\n")


    # Convert a target date (e.g., June 17, 2021) to a unix timestamp
# we know NAIP was collected on 6/17/2021 over this area by manual inspection of the dataset
filter_date_dt = datetime.datetime(2021, 6, 17)

filter_date_unix = int(time.mktime(filter_date_dt.timetuple()) * 1000)
filter_date_unix



dc_bounds_item = gis.content.get("40e234c129144e4ebc97f813f6985fa9")
dc_bounds_lyr = dc_bounds_item.layers[0]



df_dc_bounds = dc_bounds_lyr.query(as_df=True)

envelope = arcgis.geometry.Envelope((df_dc_bounds.spatial.bbox))


df = naip_lyr.query(
    "AcquisitionDate IS NOT NULL",
    geometry_filter = arcgis.geometry.filters.intersects(
        geometry=envelope, 
        sr=envelope.spatial_reference),
    as_df=True,
    # return_geometry=False
    )
df

import pandas as pd

df.AcquisitionDate.apply(lambda x: int(time.mktime(pd.to_datetime(x, unit='ms').timetuple())*1000))

unique_dates = sorted(list(set([f.attributes['AcquisitionDate'] for f in fset.features])))

# create a list of datetime objects in utc
dates_dt = [datetime.datetime.fromtimestamp(d/1000) for d in unique_dates]




wkid = dc_bounds_lyr.properties.extent['spatialReference']['wkid']
wkid

xmax = dc_bounds_lyr.properties.extent['xmax']
xmin = dc_bounds_lyr.properties.extent['xmin']
ymax = dc_bounds_lyr.properties.extent['ymax']
ymin = dc_bounds_lyr.properties.extent['ymin']


dc_bounds_flayer = arcpy.MakeFeatureLayer_management(dc_bounds_lyr.url, "dc_bounds")
desc = arcpy.Describe(dc_bounds_flayer) 
spref = desc.spatialReference
metersPerUnit = spref.metersPerUnit
data_type = desc.dataType 


# Calculate height and width of output image
naip_res = 1 # NAIP resolution in 1 meter

w = int((xmax - xmin) * metersPerUnit / naip_res)
h = int((ymax - ymin) * metersPerUnit / naip_res)



naip_lyr.export_image(
    bbox=arcgis.geometry.Envelope(dc_bounds_lyr.properties.extent),
    time = 1437548400000,
    export_format = "tiff",
    rendering_rule = {'rasterFunction': "NaturalColor"},
    size=[w, h],
    f = "image",
    save_folder = r".",
    save_file = rf"NaipT1est__{w}_{h}.tif",
    image_sr = wkid,
    bbox_sr = wkid,
    no_data = 0,
    )


# summarize the counts of pixels for each class and do some math













# Get metadata from the AOI layer to pass to the export function

wkid = dc_bounds_lyr.properties.extent['spatialReference']['wkid']
wkid


xmax = dc_bounds_lyr.properties.extent['xmax']
xmin = dc_bounds_lyr.properties.extent['xmin']
ymax = dc_bounds_lyr.properties.extent['ymax']
ymin = dc_bounds_lyr.properties.extent['ymin']



dc_bounds_flayer = arcpy.MakeFeatureLayer_management(dc_bounds_lyr.url, "dc_bounds")
desc = arcpy.Describe(dc_bounds_flayer) 
spref = desc.spatialReference
metersPerUnit = spref.metersPerUnit
data_type = desc.dataType 



# Calculate height and width of output image
naip_res = 1 # NAIP resolution in 1 meter

w = int((xmax - xmin) * metersPerUnit / naip_res)
h = int((ymax - ymin) * metersPerUnit / naip_res)



rendering = "NaturalColor" # export only RGB bands


# extract a NAIP image with a Time and Geometry filter
rgb_bands = naip_lyr.export_image(
                  bbox=arcgis.geometry.Envelope(dc_bounds_lyr.properties.extent),
                  time = filter_date_unix,
                  export_format = "tiff",
                  rendering_rule = {'rasterFunction': rendering},
                  size=[w, h],
                  f = "image",
                  save_folder = r".",
                  save_file = f"NaipTest_{filter_date_unix}_{rendering}_{w}_{h}.tif",
                  image_sr = wkid,
                  bbox_sr = wkid,
                  no_data = 0,
                 )



xmin = -121.497028
xmax = -121.445101
ymin = 37.689793
ymax = 37.722999
sr = 4326

envelope = arcgis.geometry.Polygon({
    "xmin":xmin,
     "ymin": ymin, 
     "xmax": xmax, 
     "ymax": ymax,
     "spatialReference":sr})

fset = naip_lyr.query(
    "AcquisitionDate IS NOT NULL",
    geometry_filter = arcgis.geometry.filters.intersects(
        geometry={"x":xmin, "y":ymin, "spatialReference":sr}, 
        sr=sr))

dates = sorted([f.attributes['AcquisitionDate'] for f in fset.features])

#get datetime objects for dates
dates_dt = [datetime.datetime.fromtimestamp(d/1000) for d in dates]

wkid = 3857

extent = arcgis.geometry.Polygon(fset.features[0].geometry).extent
xmin = extent[0]
ymin = extent[1]
xmax = extent[2]
ymax = extent[3]
envelope = arcgis.geometry.Envelope(
    {

    "xmin":extent[0],
     "ymin": extent[1], 
     "xmax": extent[2], 
     "ymax": extent[3],
     "spatialReference":wkid})


unique_dates = list(set([f.attributes['AcquisitionDate'] for f in fset.features]))


# Calculate height and width of output image
naip_res = 1 # NAIP resolution in 1 meter

metersPerUnit = arcpy.SpatialReference(wkid).metersPerUnit

w = int((xmax - xmin) * metersPerUnit / naip_res)
h = int((ymax - ymin) * metersPerUnit / naip_res)


ud = unique_dates[-3]
naip_lyr.export_image(
    bbox=envelope,
    time = ud,
    export_format = "tiff",
    rendering_rule = {'rasterFunction': rendering},
    size=[w, h],
    f = "image",
    save_folder = r".",
    save_file = rf"C:\Users\dav11274\Desktop\github\Top-20-Python\Exercises\Chapter 14 - Rasters and GeoAI\NaipT1est_{ud}_{rendering}_{w}_{h}.tif",
    image_sr = wkid,
    bbox_sr = wkid,
    no_data = 0,
    )


# timestamp for now
filter_date_dt = datetime.datetime.now()

#timestamp for one month ago
filter_date_dt = datetime.datetime.now() - datetime.timedelta(days=30)

filter_date_unix = int(time.mktime(filter_date_dt.timetuple()) * 1000)