# -*- coding: utf-8 -*-

import arcpy
import zipfile
import os


class Toolbox:
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Toolbox"
        self.alias = "toolbox"

        # List of tool classes associated with this toolbox
        self.tools = [CountyExporter]


class CountyExporter:
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "County Exporter"
        self.description = ""

    def getParameterInfo(self):
        """Define the tool parameters."""
        # First parameter
        full_fc_path = arcpy.Parameter(
            displayName="Highways Feature Class",
            name="Highways_Feature_Class",
            datatype="GPFeatureLayer",
            parameterType="Required",
            direction="Input")

        # Second parameter
        output_folder = arcpy.Parameter(
            displayName="Output Folder",
            name="Output_Folder",
            datatype="DEFolder",
            parameterType="Required",
            direction="Input")


        # Third parameter
        county = arcpy.Parameter(
            displayName="County",
            name="County",
            datatype="GPString",
            parameterType="Required",
            direction="Input")
        
        county.filter.type = "ValueList"

        county.filter.list = []
        # county.parameterDependencies = [full_fc_path]


        params = [full_fc_path, output_folder, county]
        return params

    def isLicensed(self):
        """Set whether the tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        if parameters[0].altered:
            # get the unique values from the NAMELSAD field
            with arcpy.da.SearchCursor(parameters[0].valueAsText, "NAMELSAD") as cursor:
                counties = sorted({row[0] for row in cursor})
                parameters[2].filter.list = counties
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter. This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        
        highways_feature_class = parameters[0].valueAsText
        output_folder = parameters[1].valueAsText
        county = parameters[2].valueAsText

        zip_county_highways(
                highways_feature_class, 
                output_folder,
                county
            )
        return

    def postExecute(self, parameters):
        """This method takes place after outputs are processed and
        added to the display."""
        return

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


