import requests
import json
import pandas
import time



url = "https://data.sfgov.org/resource/vw6y-z8j6.json"
fields = "$select=service_request_id,requested_datetime,status_notes,lat,long,neighborhoods_sffind_boundaries,source,supervisor_district,media_url,point"
where = "$where=status_description='Open' and requested_datetime > '2024-01-20T00:00:00.000000'"
limit = "$limit=1000"
order = "$order=requested_datetime DESC"


response = requests.get(url+"?"+fields+"&"+where+"&"+limit+"&"+order)

json_response = json.loads(response.text)

print(len(json_response))

df = pandas.DataFrame(json_response)





import datetime

# Get the current date and time
now = datetime.datetime.now()

# Subtract one day from the current date
yesterday = now - datetime.timedelta(days=1)

# Set the time to midnight
midnight = datetime.time()

# Combine the date and time
timestamp = datetime.datetime.combine(yesterday, midnight)

# Convert the timestamp to a floating point number
floating_timestamp = timestamp.strftime('%Y-%m-%dT%H:%M:%S.%f') 

# Print the floating timestamp
print(floating_timestamp)
