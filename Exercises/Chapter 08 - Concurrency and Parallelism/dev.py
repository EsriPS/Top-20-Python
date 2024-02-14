

import multiprocessing
import time
import os

# print(multiprocessing.cpu_count())

# create a manager object to manage the output?
# manager = multiprocessing.Manager()
# merged_results = manager.list()
# process_list = []



def gp_logic(start, end):
    # merged_results.append((start, end))
    try:
        print(f'GP logic for {start} to {end} complete')
        time.sleep(10)
        # with open(os.path.join(r'C:\Users\dav11274\Desktop\github\Top-20-Python\Exercises\Chapter 08 - Concurrency and Parallelism',
        #                     f'output_{start}_{end}.txt'), 'w') as f:
        #     f.write(f'GP logic for {start} to {end} complete')
    except Exception as e:
        return -1
    # return (start, end)



process_count = 10


# if __name__ == '__main__':

from concurrent.futures import ProcessPoolExecutor, as_completed

with ProcessPoolExecutor(max_workers=process_count, mp_context=multiprocessing.get_context('fork')) as executor:
    futures_list = []
    for i in range(0,5):
        futures_list.append(executor.submit(gp_logic, i, i))

    print(len(futures_list))
    for future in as_completed(futures_list):
        print(future.result())



# while start < end:
#     for i in range(process_count):
#         loop_end = start + chunk_size
#         p = multiprocessing.Process(target=gp_logic, args=(start, loop_end))
#         p.start()
#         process_list.append(p)
#         # gp_logic(start, loop_end, merged_results)
#         print(f'GP logic for {start} to {loop_end} complete')
#         start = start + chunk_size



# for process in process_list:
#     # needed to ensure the tool doesn't finish until the last chunk is complete.
#     process.join()











# import arcgis

# gis = arcgis.GIS('home')

# item_structures = gis.content.get('0ec8512ad21e4bb987d7e848d14e7e24')
# lyr_structures = item_structures.layers[0]


# item_wildfires = gis.content.get('3f7b0c76a05a4f6995f9759cd41c0215')
# lyr_wildfires = item_wildfires.layers[1]

# fset_wildfires = lyr_wildfires.query(where='1=1', 
#                                      return_geometry=True, 
#                                      out_fields='*')

# def query_structures_by_wildfire(wildfire_feature,
#                                  structures_layer):
    
#     try:
#         # Get the wildfire geometry and name
#         wildfire_geom = wildfire_feature.geometry
#         wildfire_name = wildfire_feature.attributes['FIRE_NAME']

#         # Create a spatial filter to find structures that intersect the wildfire
#         wildfire_filter = arcgis.geometry.filters.intersects(
#             wildfire_geom, sr = wildfire_geom['spatialReference']
#         )

#         # Query the structures layer for structures that intersect the wildfire
#         structures = structures_layer.query(
#             geometry_filter = wildfire_filter,
#             return_count_only=True
#         )

#         # Return the wildfire name and the number of structures
#         return {
#             'Wildfire': wildfire_name,
#             'Structures': structures
#             }
    
#     # If an error occurs, return the wildfire name and None for the structures
#     except Exception as e:

#         # print the error so we know which wildfire failed
#         print(wildfire_name, e)

#         return {
#             'Wildfire': wildfire_name,
#             'Structures': None
#             }


# # query all the wildfires
# fset_wildfires = lyr_wildfires.query(
#     where = "1=1"
# )

# # start a timer for the total time
# total_start = time.time()

# # iterate through the first 100 wildfires
# for wildfire in fset_wildfires.features:
    
#     # timer for individual features
#     loop_start = time.perf_counter()
    
#     # run the query for each wildfire
#     results = query_structures_by_wildfire(
#                             wildfire_feature = wildfire,
#                             structures_layer = lyr_structures
#                         )
    
#     # close out the timer
#     loop_end = time.perf_counter()
    
#     print(results, loop_end - loop_start)
    
# # close out the timer for total time
# total_end = time.time()
# print(total_end - total_start)


# mt_start = time.time()
# result_dicts = []

# import concurrent

# # Use a ThreadPoolExecutor to query structures for each wildfire
# with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:

#     # Create a list to store the future objects
#     exec_results = []

#     # Iterate through each wildfire feature
#     for wildfire in fset_wildfires.features:

#         # Submit a query task for each wildfire
#         exec_result = executor.submit(query_structures_by_wildfire,
#                                       wildfire_feature = wildfire,
#                                       structures_layer = lyr_structures)

#         # Append the future object to the list
#         exec_results.append(exec_result)

#     # Iterate through the future objects as they complete
#     for r in concurrent.futures.as_completed(exec_results):

#         # Append the result to the list of results
#         result_dicts.append(r.result())

# mt_end = time.time()
# print(mt_end - mt_start)