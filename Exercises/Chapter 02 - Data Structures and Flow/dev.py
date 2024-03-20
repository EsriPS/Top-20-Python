







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

fc = r"C:\Users\dav11274\Desktop\github\Top-20-Python\Exercises\Chapter 02 - ArcPy Basics\Chapter 02 Files\Chapter 02 - Working with Maps.gdb\highways_intersect"


fset = arcpy.FeatureSet(fc)


json_string = arcpy.FeatureSet(fc).JSON
json_fc = json.loads(json_string)


for key in json_fc.keys():
    print(key, type(json_fc[key]))



import arcgis
df = arcgis.features.GeoAccessor.from_featureclass(fc)


geom = df.SHAPE[0]