import arcpy


file_gdb = r"C:\Users\dav11274\Desktop\github\Top-20-Python\Exercises\Chapter 12 - Interacting with Databases\indoors_test.gdb"

arcpy.env.workspace = file_gdb


arcpy.ListFeatureClasses()

arcpy.ListTables()

arcpy.ListDatasets()

for dataset in arcpy.ListDatasets():
    print(dataset)
    for fc in arcpy.ListFeatureClasses(feature_dataset=dataset):
        print(f"  {fc}")
for fc in arcpy.ListFeatureClasses():
    print(fc)
for table in arcpy.ListTables():
    print(table)



for root, dirs, files in arcpy.da.Walk(file_gdb):
    for dir in dirs:
        print(dir)
    for file in files:
        print(file)









import arcpy
import sqlite3
import pandas as pd
import os
import csv
import arcgis

sl_db = arcpy.management.CreateSQLiteDatabase(
    r"C:\Users\dav11274\Desktop\github\Top-20-Python\Exercises\Chapter 12 - Interacting with Databases\data",
    "ST_GEOMETRY"
)

fc_counties = arcpy.conversion.ExportFeatures(
    r"C:\Users\dav11274\Desktop\github\Top-20-Python\Exercises\Chapter 03 - ArcPy Basics\Chapter 03 Files\Chapter 02 - Working with Maps.gdb\Counties",
    os.path.join(sl_db[0], "Counties")
)


for root, dirs, files in arcpy.da.Walk(sl_db):
    for dir in dirs:
        print(dir)
    for file in files:
        print(file)




sl_conn = sqlite3.connect(sl_db[0])

sl_cursor = sl_conn.cursor()

sl_cursor.execute("select * from sqlite_master ")

results = sl_cursor.fetchall()

pd.DataFrame(results)






pd.read_sql("select * from Counties", sl_conn)








# import arcgis
# item_blocks = arcgis.GIS().content.get('d1105f1e65a743cc84fc12c034625fc7')

# import csv

# df_blocks = item_blocks.layers[0].query(r"GEOID LIKE '06%'",
#                             as_df=True,
#                 return_geometry=False)

# # ensure that GEOID is a string as a csv
# df_blocks['GEOID'] = df_blocks['GEOID'].astype(str)
# df_blocks[['GEOID','P0010001','H0010001']]\
# .rename(columns={'P0010001':'Population','H0010001':'Housing_Units'})\
# .to_csv(r"C:\Users\dav11274\Desktop\github\Top-20-Python\Exercises\Chapter 12 - Interacting with Databases\block_groups.csv", index=False,
#         )


csv_path = r"C:\Users\dav11274\Desktop\github\Top-20-Python\Exercises\Chapter 12 - Interacting with Databases\block_groups.csv"

# copy the csv into the sqlite database without the header
# sl_cursor.execute("CREATE TABLE BlockGroups2 (GEOID TEXT, Population INTEGER, Housing_Units INTEGER)")
# with open(csv_path, 'r') as f:
#     reader = csv.reader(f)
#     next(reader)  # Skip the header
#     sl_cursor.executemany("INSERT INTO BlockGroups2 (GEOID, Population, Housing_Units) VALUES (?, ?, ?)", reader)

df_block_groups = pd.read_csv(
    r"C:\Users\dav11274\Desktop\github\Top-20-Python\Exercises\Chapter 12 - Interacting with Databases\block_groups.csv"
    )

df_block_groups['county_geoid'] = df_block_groups['GEOID'].astype(str).str[:4].str.zfill(5)
df_block_groups.to_sql("BlockGroups", sl_conn, if_exists='replace', index=False)



sql = """
SELECT
    county_geoid,
    SUM(Population) as county_population,
    SUM(Housing_Units) as county_housing_units
FROM
    BlockGroups
GROUP BY
    county_geoid

"""
pd.read_sql(sql, sl_conn)






sql = """
CREATE VIEW CountyStats AS
SELECT
    county_geoid,
    SUM(Population) as county_population,
    SUM(Housing_Units) as county_housing_units
FROM
    BlockGroups
GROUP BY
    county_geoid

"""
sl_cursor.execute(sql)


pd.read_sql("select * from CountyStats", sl_conn)


sql_join = """
CREATE VIEW CountyStatsSpatial2 AS
SELECT
    fc.OBJECTID,
    fc.name,
    tbl.county_population,
    tbl.county_housing_units,
    fc.shape
FROM
    Counties fc
    JOIN
        CountyStats tbl
    ON
        fc.geoid = tbl.county_geoid
"""

sl_cursor.execute(sql_join)
# del(sl_cursor)

pd.read_sql("select * from CountyStatsSpatial2", sl_conn)

pd.DataFrame.spatial.from_featureclass(
    os.path.join(sl_db[0],"main.CountyStatsSpatial2")
)




# from sqlalchemy import Column
# from sqlalchemy import ForeignKey
# from sqlalchemy import Integer
# from sqlalchemy import String
# from sqlalchemy.orm import declarative_base
# from sqlalchemy.orm import relationship

# Base = declarative_base()

# class User(Base):
#     __tablename__ = "user_account"
#     id = Column(Integer, primary_key=True)
#     name = Column(String(30))
#     fullname = Column(String)
#     addresses = relationship(
#         "Address", back_populates="user", cascade="all, delete-orphan"
#     )
#     def __repr__(self):
#         return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"

# class Address(Base):
#     __tablename__ = "address"
#     id = Column(Integer, primary_key=True)
#     email_address = Column(String, nullable=False)
#     user_id = Column(Integer, ForeignKey("user_account.id"), nullable=False)
#     user = relationship("User", back_populates="addresses")
#     def __repr__(self):
#         return f"Address(id={self.id!r}, email_address={self.email_address!r})"