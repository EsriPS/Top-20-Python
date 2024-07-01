







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




# import arcpy
# import json

# fc = r"C:\Users\dav11274\Desktop\github\Top-20-Python\Exercises\Chapter 03 - ArcPy Basics\Chapter 03 Files\Chapter 02 - Working with Maps.gdb\highways_intersect"


# fset = arcpy.FeatureSet(fc)


# json_string = arcpy.FeatureSet(fc).JSON
# json_fc = json.loads(json_string)


# for key in json_fc.keys():
#     print(key, type(json_fc[key]))




# import pandas
# import requests
# import json
# import datetime


# url = "https://data.sfgov.org/resource/wg3w-h783.json"

# now = datetime.datetime.now()
# start_date = now - datetime.timedelta(days=7)
# midnight = datetime.time()

# # Combine the date and time
# start_day_midnight = datetime.datetime.combine(start_date, midnight)
# formatted_start_day = start_day_midnight.strftime('%Y-%m-%dT%H:%M:%S.%f') 
# formatted_start_day


# resp = requests.get(url, params={'$where': f"incident_date > '{formatted_start_day}'"})

# with open('data.json', 'w') as f:
#     f.write(resp.text)


import json

with open('data.geojson') as f:
    data = json.load(f)


type(data)


type(data[0]['point']['coordinates'])


for f in data:
    f['incident_category']


import requests
import json

resp = requests.get('https://data.sfgov.org/resource/vw6y-z8j6.geojson?$query=SELECT%0A%20%20%60service_request_id%60%2C%0A%20%20%60requested_datetime%60%2C%0A%20%20%60closed_date%60%2C%0A%20%20%60updated_datetime%60%2C%0A%20%20%60status_description%60%2C%0A%20%20%60status_notes%60%2C%0A%20%20%60agency_responsible%60%2C%0A%20%20%60service_name%60%2C%0A%20%20%60service_subtype%60%2C%0A%20%20%60service_details%60%2C%0A%20%20%60address%60%2C%0A%20%20%60street%60%2C%0A%20%20%60supervisor_district%60%2C%0A%20%20%60neighborhoods_sffind_boundaries%60%2C%0A%20%20%60police_district%60%2C%0A%20%20%60lat%60%2C%0A%20%20%60long%60%2C%0A%20%20%60point%60%2C%0A%20%20%60point_geom%60%2C%0A%20%20%60source%60%2C%0A%20%20%60media_url%60%2C%0A%20%20%60bos_2012%60%2C%0A%20%20%60data_as_of%60%2C%0A%20%20%60data_loaded_at%60%2C%0A%20%20%60%3A%40computed_region_6qbp_sg9q%60%2C%0A%20%20%60%3A%40computed_region_qgnn_b9vv%60%2C%0A%20%20%60%3A%40computed_region_26cr_cadq%60%2C%0A%20%20%60%3A%40computed_region_ajp5_b2md%60%2C%0A%20%20%60%3A%40computed_region_rxqg_mtj9%60%2C%0A%20%20%60%3A%40computed_region_yftq_j783%60%2C%0A%20%20%60%3A%40computed_region_jx4q_fizf%60%2C%0A%20%20%60%3A%40computed_region_bh8s_q3mv%60%2C%0A%20%20%60%3A%40computed_region_p5aj_wyqh%60%2C%0A%20%20%60%3A%40computed_region_fyvs_ahh9%60%2C%0A%20%20%60%3A%40computed_region_f58d_8dbm%60%2C%0A%20%20%60%3A%40computed_region_9dfj_4gjx%60%2C%0A%20%20%60%3A%40computed_region_vtsz_7cme%60%2C%0A%20%20%60%3A%40computed_region_n4xg_c4py%60%2C%0A%20%20%60%3A%40computed_region_sruu_94in%60%2C%0A%20%20%60%3A%40computed_region_4isq_27mq%60%2C%0A%20%20%60%3A%40computed_region_viu7_rrfi%60%2C%0A%20%20%60%3A%40computed_region_fcz8_est8%60%2C%0A%20%20%60%3A%40computed_region_pigm_ib2e%60%2C%0A%20%20%60%3A%40computed_region_9jxd_iqea%60%2C%0A%20%20%60%3A%40computed_region_6ezc_tdp2%60%2C%0A%20%20%60%3A%40computed_region_6pnf_4xz7%60%2C%0A%20%20%60%3A%40computed_region_h4ep_8xdi%60%2C%0A%20%20%60%3A%40computed_region_nqbw_i6c3%60%2C%0A%20%20%60%3A%40computed_region_2dwj_jsy4%60%2C%0A%20%20%60%3A%40computed_region_y6ts_4iup%60%2C%0A%20%20%60%3A%40computed_region_jwn9_ihcz%60')

jdict = resp.json()

with open('data.geojson', 'w') as f:
    f.write(json.dumps(jdict))

# convert the url-encoded query string to a dictionary
url ="""https://data.sfgov.org/resource/vw6y-z8j6.json?$query=SELECT%0A%20%20%60service_request_id%60%2C%0A%20%20%60requested_datetime%60%2C%0A%20%20%60closed_date%60%2C%0A%20%20%60updated_datetime%60%2C%0A%20%20%60status_description%60%2C%0A%20%20%60status_notes%60%2C%0A%20%20%60agency_responsible%60%2C%0A%20%20%60service_name%60%2C%0A%20%20%60service_subtype%60%2C%0A%20%20%60service_details%60%2C%0A%20%20%60address%60%2C%0A%20%20%60street%60%2C%0A%20%20%60supervisor_district%60%2C%0A%20%20%60neighborhoods_sffind_boundaries%60%2C%0A%20%20%60police_district%60%2C%0A%20%20%60lat%60%2C%0A%20%20%60long%60%2C%0A%20%20%60point%60%2C%0A%20%20%60point_geom%60%2C%0A%20%20%60source%60%2C%0A%20%20%60media_url%60%2C%0A%20%20%60bos_2012%60%2C%0A%20%20%60data_as_of%60%2C%0A%20%20%60data_loaded_at%60%2C%0A%20%20%60%3A%40computed_region_6qbp_sg9q%60%2C%0A%20%20%60%3A%40computed_region_qgnn_b9vv%60%2C%0A%20%20%60%3A%40computed_region_26cr_cadq%60%2C%0A%20%20%60%3A%40computed_region_ajp5_b2md%60%2C%0A%20%20%60%3A%40computed_region_rxqg_mtj9%60%2C%0A%20%20%60%3A%40computed_region_yftq_j783%60%2C%0A%20%20%60%3A%40computed_region_jx4q_fizf%60%2C%0A%20%20%60%3A%40computed_region_bh8s_q3mv%60%2C%0A%20%20%60%3A%40computed_region_p5aj_wyqh%60%2C%0A%20%20%60%3A%40computed_region_fyvs_ahh9%60%2C%0A%20%20%60%3A%40computed_region_f58d_8dbm%60%2C%0A%20%20%60%3A%40computed_region_9dfj_4gjx%60%2C%0A%20%20%60%3A%40computed_region_vtsz_7cme%60%2C%0A%20%20%60%3A%40computed_region_n4xg_c4py%60%2C%0A%20%20%60%3A%40computed_region_sruu_94in%60%2C%0A%20%20%60%3A%40computed_region_4isq_27mq%60%2C%0A%20%20%60%3A%40computed_region_viu7_rrfi%60%2C%0A%20%20%60%3A%40computed_region_fcz8_est8%60%2C%0A%20%20%60%3A%40computed_region_pigm_ib2e%60%2C%0A%20%20%60%3A%40computed_region_9jxd_iqea%60%2C%0A%20%20%60%3A%40computed_region_6ezc_tdp2%60%2C%0A%20%20%60%3A%40computed_region_6pnf_4xz7%60%2C%0A%20%20%60%3A%40computed_region_h4ep_8xdi%60%2C%0A%20%20%60%3A%40computed_region_nqbw_i6c3%60%2C%0A%20%20%60%3A%40computed_region_2dwj_jsy4%60%2C%0A%20%20%60%3A%40computed_region_y6ts_4iup%60%2C%0A%20%20%60%3A%40computed_region_jwn9_ihcz%60"""

from urllib.parse import unquote

print(unquote(url))



url ="""https://data.sfgov.org/resource/vw6y-z8j6.geojson?$query=SELECT
  `service_request_id`,
  `requested_datetime`,
  `closed_date`,
  `updated_datetime`,
  `status_description`,
  `status_notes`,
  `agency_responsible`,
  `service_name`,
  `service_subtype`,
  `service_details`,
  `address`,
  `street`,
  `supervisor_district`,
  `neighborhoods_sffind_boundaries`,
  `police_district`,
  `lat`,
  `long`,
  `point`,
  `point_geom`,
  `source`,
  `media_url`,
  `bos_2012`,
  `data_as_of`,
  `data_loaded_at`
  WHERE `requested_datetime` > '2023-01-01T00:00:00.000' AND `requested_datetime` < '2024-01-01T00:00:00.000' AND lat > 0
  LIMIT 10000"""



resp = requests.get(url)
jdict = resp.json()


with open('data.geojson', 'w') as f:
    f.write(json.dumps(jdict))

dates = [pd.to_datetime(f['properties']['requested_datetime']) for f in jdict['features']]

import pandas as pd















# create a list
list_1 = [1, 2, 3, 5, 7, 8]

# get the first item in the list
list_1[0]

# get the last item in the list
list_1[-1]

# get the first 3 items in the list
list_1[0:3]


# copy a list
list_2 = list_1[0:-1]

# pop the last item from the list
list_2.pop(2)

list_2.append("a new value")

# print the original list
print(list_1)

print(list_2)

# create a dictionary
dict_1 = {
    'key1': 'value1',
    'key2': 'value2',
    'key3': 'value3'
}

# print the dictionary keys
print(dict_1.keys())

# print the dictionary values
print(dict_1.values())

# print the 
dict_1['key1']


dict_1['key1'] = 'updates!'
dict_1['key1']


dict_1['a new key'] = 'a new value'

dict_1['and a list'] = list_2


dict_2 = {
    'key3': 'new value3',
    'key4': 'value4',
    'key5': 'value5'
}

# combine two dictionaries
dict_1.update(dict_2)


# load some unknown data
import json

with open('data.geojson') as f:
    data = json.load(f)

# check the type of the data
type(data)

# check the keys of the data
data.keys()

# check the value of hte "type" key
data['type']

# check the type of the "features" key
type(data['features'])

# check the type of the first item in the "features" key
type(data['features'][0])

# check the keys of the first item in the "features" key
data['features'][0].keys()

# check the keys of the "properties" key in the first item in the "features" key
data['features'][0]['properties'].keys()

# check the value of the "service_name" key in the "properties" key in the first item in the "features" key
data['features'][0]['properties']['service_name']


data['features'][0]


first_feature = data['features'][0]

first_feature['properties']['service_name'] = 'new value'

features = data['features']

# reset the dictionary - just in case
sn_count_dict = {}

# iterate through each feature
for feature in features:
    
    # get the service name
    service_name = feature['properties']['service_name']
    
    # test to see if the service_name is in the dictionary
    if service_name in sn_count_dict:
        # add to the number if it's already in there
        sn_count_dict[service_name] = sn_count_dict[service_name] + 1
    else:
        # add a new key to the dictionary if not already there
        sn_count_dict[service_name] =  1

# sort the dictionary by value
sorted_sn_count_dict = {k: v for k, v in sorted(sn_count_dict.items(), key=lambda item: item[1], reverse=True)}