def extract_to_df(url):
    '''
    TODO - write docstring
    '''

    # Request data from the API
    response = requests.get(url)

    # Convert the response to JSON
    response_text = response.text

    # Convert JSON to a Python data types (lists/dictionaries)
    results_list = json.loads(response_text)

    # Convert the Python lists/dictionaries to a Pandas DataFrame
    df = pandas.DataFrame(results_list)

    # Return the DataFrame
    return df


import pandas
import requests
import json
import datetime
import arcgis


now = datetime.datetime.now()
yesterday = now - datetime.timedelta(days=1)

# Set the time to midnight
midnight = datetime.time()

# Combine the date and time
yesterday_midnight = datetime.datetime.combine(yesterday, midnight)
formatted_yesterday = yesterday_midnight.strftime('%Y-%m-%dT%H:%M:%S.%f') 
where = f"$where=status_description='Open' and requested_datetime > '{formatted_yesterday}'"

field_list = [
    'service_request_id',
    'requested_datetime',
    'closed_date',
    'status_notes',
    'lat',
    'long',
    'neighborhoods_sffind_boundaries',
    'source',
    'supervisor_district',
    'media_url',
    'point'
]

fields = "$select=" + ",".join(field_list)

url = "https://data.sfgov.org/resource/vw6y-z8j6.json"
full_url = url+"?"+fields+"&"+where


df = extract_to_df(full_url)


# import arcpy
# import arcgis

# with arcpy.EnvManager(workspace=r"C:\Users\dav11274\Desktop\github\Top-20-Python\Exercises\Chapter 06\Tutorial_06_02.gdb"):
#     print(arcpy.ListFeatureClasses())




df_neighborhood = df.groupby("neighborhoods_sffind_boundaries").agg(
    {
        "service_request_id": "count"
    }
)


sedf_neighborhoods = pandas.DataFrame.spatial.from_featureclass(
    "../Chapter 06/Tutorial_06_02.gdb/SF_Find_Neighborhoods"
)



sedf_merge = sedf_neighborhoods.merge(
    df_neighborhood, 
    how = 'inner', 
    left_on = 'name', 
    right_on = 'neighborhoods_sffind_boundaries'
)

sedf_merge.rename(
    columns = {"service_request_id": "count"},
)