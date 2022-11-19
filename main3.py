import geopandas
import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
from shapely.geometry import Point
import sys
path = "/home/mina5/Downloads/geopandas(2)/geopandas/temel ornekler/Turkey_shapefile/turkey_administrativelevels0_1_2/"
# path = "/home/mina5/Downloads/geopandas(2)/geopandas/temel ornekler/Turkey_shapefile/İl_İlçe_Sınır_Ve_Yerleşim_Verisi/"
# Importing the states ESRI Shapefile of the USA
# Shape dosyasini yukle
tr = gpd.read_file(path + 'tur_polbnda_adm1.shp')

df = pd.read_excel(path + "turkiye-ve-cevresi-cografi-ad-dizini-turkce-xls-111.xls")
df['Coordinates'] = list(zip(df.BOYLAM, df.ENLEM))
df['Coordinates'] = df['Coordinates'].apply(Point)
gdf = geopandas.GeoDataFrame(df, geometry='Coordinates')

print(gdf['TİP'].value_counts().to_dict())

arkazemin = tr.boundary.plot()
# 'YAY': 644
# 'BRJ': 153
# 'MGR': 66

gdf[ gdf['TİP'] == 'YAY'].plot( ax = arkazemin, color = 'green' ) #
gdf[ gdf['TİP'] == 'BRJ'].plot( ax = arkazemin, color = 'red' ) #
gdf[ gdf['TİP'] == 'KALE'].plot( ax = arkazemin, color = 'blue' ) #
plt.show()
#tepeler = df[df['TİP'] == 'TEPE']


#print(dict(df['TİP'].value_counts()))


#tr.plot()
#plt.show()