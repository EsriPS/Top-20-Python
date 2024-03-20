


import arcgis
gis = arcgis.GIS("home")

item_2020_census_housing = gis.content.get('81d9e89b8b574a649ff6e14f61c8494f')

lyr_counties = item_2020_census_housing.layers[2]

df_california = lyr_counties.query(
    where="STATE = 'California'",
    as_df=True
)



field_aliases = {f['name']: f['alias'] 
              for f in lyr_counties.properties.fields}


df_california = df_california.rename(columns=field_aliases)

df_california['Name'].plot()

df_california.plot(
    kind='bar', 
    x='Name', 
    y='Total Housing Units',
)

df_california.plot(
    kind='bar', 
    x='Name', 
    y='Total Housing Units',
    figsize=(15, 5),
)

df_california = df_california.sort_values(
    'Total Housing Units', 
    ascending=False
    )


df_california.plot(
    kind='bar', 
    x='Name', 
    y='Total Housing Units',
    figsize=(15, 5),
)


df_california.plot(
    kind='hist', 
    y='Total Housing Units',
    legend=False,
)


df_california[df_california.Name != 'Los Angeles County'].plot(
    kind='scatter',
    x='Total Housing Units',
    y='Total Population',
)



import arcpy

# url = r"https://services1.arcgis.com/hLJbHVT9ZrDIzK0I/arcgis/rest/services/CrimesChiTheft/FeatureServer/0"
# bar = arcpy.charts.Bar(x="BEAT", aggregation="count", title="Chicago Thefts by Beat", dataSource=url)
# bar.exportToSVG('bar.svg', width=800, height=500)


# flyr_counties = arcpy.management.MakeFeatureLayer(
#     lyr_counties.url,
#     "california counties",
#     "STATE = 'California'"
# )




import seaborn as sns
sns.set_style('whitegrid')


ax = sns.barplot(x=df_california['Name'][0:10], 
                 y=df_california['Total Housing Units'][0:10],
                 palette='viridis')
ax.set_xticklabels(df_california['Name'][0:10],rotation=90)

sns.scatterplot(x='Total Housing Units', y='Total Population', data=df_california)


sns.catplot?



import plotly.express as px

fig = px.bar(df_california, x='Name', y='Total Housing Units')
fig.show()


import pyarrow as pa

pa_table=  pa.Table.from_pandas(df_california[["Total Housing Units", "Name"]])

arcpy.charts.Pie(
    categoryField="Name",
    numberFields = ["Total Housing Units"],
    title="Total Housing Units by County",
    dataSource= pa_table
)


arcpy.charts.Bar(
    x="Name",
    y = ["Total Housing Units"],
    title="Total Housing Units by County",
    dataSource= pa_table,
    miniChartsPerRow=4
)

arcpy.charts.QQPlot(x="p_matter", dataTransformationType="squareRoot",
                            title="Comparison of Particular Matter and Normal Distribution",
                            dataSource="air_quality")