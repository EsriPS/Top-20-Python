import arcpy


fc = r"C:\Users\dav11274\Desktop\github\Top-20-Python\Exercises\Chapter 02 - ArcPy Basics\Chapter 02 Files\Chapter 02 - Working with Maps.gdb\Highways_intersect"

arcpy.Exists(fc)

arcpy.management.GetCount(fc)[0]


fields = arcpy.ListFields(fc)

for field in fields:
    print(field.name, field.type)

all_hwys = []




# note the context manager
with arcpy.da.SearchCursor(fc, ['HWY_NUM']) as cursor:
    for row in cursor:
        all_hwys.append(row[0])


len(all_hwys)

len(list(set(all_hwys)))

for hwa in list(set(all_hwys)):
    try:
        int(hwa)
    except:
        print(hwa)

arcpy.management.AddField(fc, 'HWY_NUM_CLEAN', 'TEXT', field_length=10)


with arcpy.da.UpdateCursor(fc, ['HWY_NUM', 'HWY_NUM_CLEAN']) as cursor:
    for row in cursor:
        try:
            row[1] = int(row[0].strip())
        except Exception as e:
            print(row[0], e)

        cursor.updateRow(row)














import arcpy

# Load the project
# project_path = r"C:\Users\dav11274\Desktop\github\Workshop_Beginner_3\Beginner_Week_3.aprx"
project_path = r".\Chapter 02 Files\Chapter 02 - Working with Maps.aprx"
project = arcpy.mp.ArcGISProject(project_path)

layout = project.listLayouts()[0]

for element in layout.listElements():
    print(element.name)

title = [e for e in layout.listElements() if e.name == 'Text'][0]
map_frame = [e for e in layout.listElements() if e.name == 'Map Frame'][0]



for layer in map_frame.map.listLayers():
    if layer.name in ['Highways_Intersect','Counties']:
        print(layer.name, layer.isBroken)



for layer in map_frame.map.listLayers():
    if layer.name in ['Highways_Intersect','Counties']:
        layer_conn_props = layer.connectionProperties
        layer_conn_props['connection_info']['database'] = project.databases[0]['databasePath']
        layer.updateConnectionProperties(
            layer.connectionProperties, layer_conn_props
        )
        print(layer.name, layer.dataSource, layer.isBroken)

project.save()



county = 'Contra Costa County'

for layer in map_frame.map.listLayers():
    if layer.name in ['Highways_Intersect','Counties']:
        layer.definitionQuery = f"NAMELSAD = '{county}'"
        county_extent = map_frame.getLayerExtent(layer, True)

# roads_layer.definitionQuery = "NAMELSAD = '{}'".format(county)
title.text = county

# zoom the map frame to the extent of the selected county
map_frame.camera.setExtent(county_extent)

layout.exportToPDF('./{}.pdf'.format(county))

# get hte layer in a map frame called 'Counties'
# for layer in layout.mapSeries.mapFrame.map.listLayers():
#     if layer.name == 'Counties':
#         counties_layer = layer



# # # Get the layout with a map series
# # for layout in layouts:
# #     if not layout.mapSeries is None:
# #         print(layout.mapSeries.enabled)

# # layout

# # check for broken layers (layers with no source)


# # reset the source for broken layers

# for layer in layout.mapSeries.mapFrame.map.listLayers():
#     if layer.name in ['Highways_Intersect','Counties']:
#         layer_conn_props = layer.connectionProperties
#         layer_conn_props['connection_info']['database'] = project.databases[0]['databasePath']
#         layer.updateConnectionProperties(
#             layer.connectionProperties, layer_conn_props
#         )
#         print(layer.name, layer.dataSource, layer.isBroken)
        
# project.save()


# print(layout.listElements())
# title = layout.listElements()[0]






# ms = layout.mapSeries

# ms.currentPageNumber

# county = 'Alameda County'
# ms.currentPageNumber =  ms.getPageNumberFromName(county)

# for layer in layout.mapSeries.mapFrame.map.listLayers():
#     if layer.name == 'Highways_Intersect':
#         roads_layer = layer

# roads_layer.definitionQuery = "NAMELSAD = '{}'".format(county)
# title.text = county


# ms.exportToPDF('./{}.pdf'.format(county), 'CURRENT')






# break the layers
import arcpy
import os

# Load the project
# project_path = r"C:\Users\dav11274\Desktop\github\Workshop_Beginner_3\Beginner_Week_3.aprx"
project_path = r".\Chapter 02 Files\Chapter 02 - Working with Maps.aprx"
project = arcpy.mp.ArcGISProject(project_path)

layout = project.listLayouts()[0]

for element in layout.listElements():
    print(element.name)

title = [e for e in layout.listElements() if e.name == 'Text'][0]
map_frame = [e for e in layout.listElements() if e.name == 'Map Frame'][0]


temp_gdb = r"C:\Top20Python\Chapter_2_rename.gdb"
# rename the database
os.rename(temp_gdb, r"C:\Top20Python\Chapter_2.gdb")

for layer in map_frame.map.listLayers():
    if layer.name in ['Highways_Intersect','Counties']:
        layer_conn_props = layer.connectionProperties
        layer_conn_props['connection_info']['database'] = r'C:\Top20Python\Chapter_2.gdb'
        # layer.updateConnectionProperties(
        #     'c:\\Desktop\\GIS_STUFF\\Workshops\\Workshop_Beginner_3\\Week_2_Data.gdb',
        #     r"C:\Users\dav11274\Desktop\github\Workshop_Beginner_3\Week_2_Data.gdb")
        layer.updateConnectionProperties(
            layer.connectionProperties, layer_conn_props
        )
        print(layer.name, layer.dataSource, layer.isBroken)
        
project.save()

del(project)

os.rename( r"C:\Top20Python\Chapter_2.gdb", temp_gdb)


