







number = 8
number % 2 == 0



# set a number
number = 8

# check if the number is even
if number % 2 == 0:

    # print a message only if the number is even
    print('this is even')

# print a message only if the number is odd
else:
    print('this is odd')



list_of_numbers = [1,2,3,4,5,6,7,9,7,10]

for number in list_of_numbers:
    print(number)


for number in list_of_numbers:
    if number % 2 == 0:
        print(number, 'is even')
    else:
        print(number, 'is odd')



for number in list_of_numbers:
    if number % 2 == 0:
        print(number, 'is even')
    else:
        print(number, 'is odd')
        double_number = number * 2
        print(double_number, 'is even')




import arcpy
import json

fc = r"C:\Users\dav11274\Desktop\github\Top-20-Python\Exercises\Chapter 03 - ArcPy Basics\Chapter 03 Files\Chapter 02 - Working with Maps.gdb\highways_intersect"


fset = arcpy.FeatureSet(fc)


json_string = arcpy.FeatureSet(fc).JSON
json_fc = json.loads(json_string)


for key in json_fc.keys():
    print(key, type(json_fc[key]))




import pandas
import requests
import json
import datetime


url = "https://data.sfgov.org/resource/wg3w-h783.json"

now = datetime.datetime.now()
start_date = now - datetime.timedelta(days=7)
midnight = datetime.time()

# Combine the date and time
start_day_midnight = datetime.datetime.combine(start_date, midnight)
formatted_start_day = start_day_midnight.strftime('%Y-%m-%dT%H:%M:%S.%f') 
formatted_start_day


resp = requests.get(url, params={'$where': f"incident_date > '{formatted_start_day}'"})

with open('data.json', 'w') as f:
    f.write(resp.text)