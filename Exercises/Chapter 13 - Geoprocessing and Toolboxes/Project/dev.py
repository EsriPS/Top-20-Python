def zip_county_highways(full_fc_path, output_folder, county):
    
    # remove spaces from county name
    county_no_spaces = county.replace(" ", "_")
    
    # create a file geodatabase
    fgdb = arcpy.management.CreateFileGDB(
        out_folder_path = output_folder,
        out_name = f"{county_no_spaces}_Output"
    )

    # Create a feature class
    output_fc = arcpy.conversion.ExportFeatures(
        in_features = full_fc_path,
        out_features = os.path.join(fgdb[0], 
                                    f"{county_no_spaces}_Highways"),
        where_clause = f"NAMELSAD = '{county}'"
    )
    
    # define a path for the zip file
    zip_file_path = os.path.join(output_folder, f"{county} Highways.zip") 

    # zip the file geodatabase
    with zipfile.ZipFile(zip_file_path, "w") as zipper:
        for root, dirs, files in os.walk(fgdb[0]):
            for file in files:
                fpath = os.path.join(root, file)
                zpath = os.path.relpath(
                            os.path.join(root, file),
                            os.path.join(fgdb[0], '..')
                        )
                zipper.write(
                    fpath,
                    zpath
                )
    
    # delete the file geodatabase
    arcpy.management.Delete(fgdb)
    
    # return the zip file path
    return zip_file_path


import arcpy
import os
import zipfile


# input file geodatabase path
full_fc_path = r"..\Chapter 03 - ArcPy Basics\Chapter 03 Files\Chapter 02 - Working with Maps.gdb\Highways_intersect"

# output folder
output_folder = r".\zipped_outputs"

# which county to export
county = "Alameda County"

if not os.path.exists(output_folder):
    os.mkdir(output_folder)

zip_county_highways(full_fc_path, output_folder, county)




