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

# package imports
import arcpy
import os
import zipfile
import multiprocessing
from concurrent.futures import ProcessPoolExecutor, as_completed

#=============================== INPUTS ===================================
# input file geodatabase path
input_fgdb = r"..\Chapter 03 - ArcPy Basics\Chapter 03 Files\Chapter 02 - Working with Maps.gdb"

# input feature class name
input_fc_name = "Highways_intersect"

# output folder
output_folder = r".\zipped_outputs"
#==========================================================================

if __name__ == '__main__':
    # get the full feature class path
    full_fc_path = os.path.join(
        input_fgdb, input_fc_name
    )

    # get the county for each feature
    counties = [r[0] for r in arcpy.da.SearchCursor(full_fc_path, ['NAMELSAD'])]

    # narrow the counties down to unique counties
    counties = list(set(counties))
    counties.sort()

    # create the output folder
    if not os.path.exists(output_folder):
        os.mkdir(output_folder)

    # get your cpu count for multiprocessing
    process_count = multiprocessing.cpu_count()

    
    # set up the process pool executor
    with ProcessPoolExecutor(max_workers=process_count) as executor:
        
        # set up a list to contain all the future objects
        futures_list = []
        
        # submit each job to the executor
        for county in counties:
            futures_list.append(executor.submit(zip_county_highways, full_fc_path, output_folder, county))

        # iterate through the futures to see when they're completed
        for future in as_completed(futures_list):
            print(future.result())