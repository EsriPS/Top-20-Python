from arcgis.gis import GIS
from arcgis.features import analysis
from pathlib import Path
import arcpy
import shutil


my_gis_org = GIS(
    url="https://www.arcgis.com",  # or your Portal URL
    profile="my_profile",
)


source_fgdb_path = Path(
    r"C:\Users\gis_pro\Documents\ArcGIS\Projects\MyProject\MyProject.gdb"
)


arcpy.management.Compact(str(source_fgdb_path))


# The name of the folder to place the File Geodatabase in
fgdb_folder_name = source_fgdb_path.stem
# The location of the folder to place the File Geodatabase in
fgdb_folder_location = source_fgdb_path.parent
# The path to the folder to place the File Geodatabase in
fgdb_folder_path = fgdb_folder_location.joinpath(fgdb_folder_name)
# The path of our copied File Geodatabase
fgdb_path = fgdb_folder_path.joinpath(source_fgdb_path.name)


# Copy the File Geodatabase to the new location
shutil.copytree(source_fgdb_path, fgdb_path)
# Zip the File Geodatabase
zipped_fgdb = shutil.make_archive(
    base_name=fgdb_folder_path,  # The name of the archive, not including the file extension
    format="zip",  # The archive format
    root_dir=fgdb_folder_path,  # The directory to archive
)


fgdb_item_properties = {
    "type": "File Geodatabase",  # The type of item this will be
    "title": "Philadelphia Parking Tickets by Neighborhood",  # The title of the item
    "description": "Parking tickets issued in Philadelphia by neighborhood",  # The description of the item
    "tags": "Philadelphia, Parking, Tickets, Neighborhood",  # Tags for the item
}


my_fgdb_item = my_gis_org.content.add(
    item_properties=fgdb_item_properties,  # The properties of the item
    data=zipped_fgdb,  # The path to the zipped file geodatabase
)


my_fgdb_item = my_gis_org.content.get("cb0765ce42bc41dfb9e0bc62ae3ce4c0")


fgdb_publish_parameters = {
    "name": "Philadelphia Parking Tickets by Neighborhood",  # The name of the service
}


my_hosted_feature_service_item = my_fgdb_item.publish(
    publish_parameters=fgdb_publish_parameters
)


[layer.properties["name"] for layer in my_hosted_feature_service_item.layers]


parking_tickets_by_neighborhood_layer = my_hosted_feature_service_item.layers[0]


enriched_layer = analysis.enrich_layer(
    input_layer=parking_tickets_by_neighborhood_layer,  # FeatureLayer object to be enriched
    analysis_variables=[
        "crime.CRMCYPROC"
    ],  # Analysis variables to enrich the input layer with
    output_name="Philadelphia Parking Tickets by Neighborhood Enriched with Property Crime",  # The name of the output layer
)
