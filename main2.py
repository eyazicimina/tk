
import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
from shapely.geometry import Point
import sys
path = "/home/mina5/Downloads/geopandas(2)/geopandas/temel ornekler/"
# Importing the states ESRI Shapefile of the USA
# Shape dosyasini yukle
us_states = gpd.read_file(path + 'us_states.shp')
# us_states.plot()
# plt.show()


#: US airports datasini yukle
airports_data = pd.read_csv(path + 'us_airports.csv')
geometry = [Point(xy) for xy in zip(airports_data['LONGITUDE'], airports_data['LATITUDE'])]
airports_us = gpd.GeoDataFrame(airports_data, geometry = geometry, crs = us_states.crs)
airports_us = airports_us[['AIRPORT', 'geometry']]


# fig, ax = plt.subplots(figsize = (8,8))
ax = us_states.plot(color = 'blue', edgecolor = 'black')
airports_us.plot(ax=ax, markersize = 2, color = 'red')

plt.show()

# Spatial Join

#! airports_us = gpd.sjoin(airports_us, us_states, how  = 'inner', op = 'intersects')

