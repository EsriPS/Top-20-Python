
# import pandas
# import requests
# import json
# import datetime



# url = "https://data.sfgov.org/resource/vw6y-z8j6.json"
# fields = "$select=service_request_id,requested_datetime,status_notes,lat,long,neighborhoods_sffind_boundaries,source,supervisor_district,media_url,point"
# where = "$where=status_description='Open' and requested_datetime > '2024-01-20T00:00:00.000000'"
# limit = "$limit=1000"
# order = "$order=requested_datetime DESC"


# response = requests.get(url+"?"+fields+"&"+where#+"&"+limit+"&"+order
#                         )

# json_response = json.loads(response.text)

# print(len(json_response))

# df = pandas.DataFrame(json_response)





# import datetime

# # Get the current date and time
# now = datetime.datetime.now()

# # Subtract one day from the current date
# yesterday = now - datetime.timedelta(days=1)

# # Set the time to midnight
# midnight = datetime.time()

# # Combine the date and time
# timestamp = datetime.datetime.combine(yesterday, midnight)

# # Convert the timestamp to a floating point number
# floating_timestamp = timestamp.strftime('%Y-%m-%dT%H:%M:%S.%f') 

# # Print the floating timestamp
# print(floating_timestamp)


# from arcgis.geometry import Geometry, Point, Polygon, Polyline

# def __geomToStringArray(geometries, returnType="str"):
#     """function to convert the geomtries to strings"""
#     listGeoms = []
#     for g in geometries:

#         if not isinstance(g, Geometry):
#             g = Geometry(g)
#         if isinstance(g, Point):
#             listGeoms.append(g)
#         elif isinstance(g, Polygon):
#             listGeoms.append(g)
#         elif isinstance(g, Polyline):
#             listGeoms.append({"paths": g["paths"]})
#     if returnType == "str":
#         return json.dumps(listGeoms)
#     elif returnType == "list":
#         return listGeoms
#     else:
#         return json.dumps(listGeoms)
    

import arcgis
gis = arcgis.gis.GIS()
geoms = [arcgis.geometry.Point({'x':15.877,'y':14.917,'spatialReference':{'wkid':4326}}),
    arcgis.geometry.Point({'x':15.859,'y':14.909,'spatialReference':{'wkid':4326}}),
    arcgis.geometry.Point({'x':15.957,'y':15.412,'spatialReference':{'wkid':4326}})]
arcgis.geometry.buffer(geoms,in_sr=4326,distances=[500,500,500],buffer_sr=3857,unit='esriSRUnit_Foot')