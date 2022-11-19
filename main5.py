import sys
import geopandas
import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
from shapely.geometry import Point, Polygon
import shapely.wkt  # herhangi bir text formatindan, point, linestring veya polygona cevirmek icin

df = pd.read_csv("mypolygons.csv", sep=";" )
print(df.dtypes)
print(df)

# Turkiye bolgesel verileri oku (2. seviyeden okuma yap)
path = "/home/mina5/Downloads/geopandas(2)/geopandas/temel ornekler/Turkey_shapefile/turkey_administrativelevels0_1_2/"
# tr = gpd.read_file(path + 'tur_polbnda_adm1.shp')
tr = gpd.read_file(path + 'tur_polbna_adm2.shp')
# Sadece Ankarayi ve komsu olan 3 daha sehri goster
komsular = ['TUR006'] #, 'TUR071', 'TUR042', 'TUR018']
alt1 = tr[ tr['adm1'].isin(komsular) ]

# Sadece sinirlari plot edelim
alt1 = alt1.boundary.plot()
# koordinatlari, metinsel formattan, nokta formatina (polygon formatina) cevir
df['coordinates'] = df['coordinates'].apply(lambda value: shapely.wkt.loads(value))

obj = df.iloc[0]['coordinates']
print(obj, type(obj))


# yenidata = gpd.GeoDataFrame( df,  geometry=[  p2, p3 ] )
gdf = geopandas.GeoDataFrame(df, geometry='coordinates')


gdf[ gdf['parselID'] == 1 ].plot(ax = alt1, color = 'blue', alpha=0.30, edgecolor='black') # alpha = 1.0 %100 ayni renkte, transparent olmadan!
gdf[ gdf['parselID'] == 2 ].plot(ax = alt1, color = 'red', alpha=0.30, edgecolor='black') # alpha = 1.0 %100 ayni renkte, transparent olmadan!



# plt.show()


p1 = Point((34.45, 45.56)) # shapely.wkt.loads("POINT(34.45 45.56)")
p2 = Point((34.55, 45.66))
print(p1, type(p1))
print(p2, type(p2))

print( p1.distance(p2) )
print( p2.distance(p1) )
# POSTGIS, ST_Distance( p1, p2 )
print( Point.distance( p1, p2 ) )



# ========================
# Bir polygon olusturalim
# Array of Array (List of List) (listeler listesi)
# [ [26.45, 36.42], [27.45, 36.42], [27.45, 37.42], [26.45, 37.42], [26.45, 36.42] ]
noktalar1 = [ [26.45, 36.42], [27.45, 36.42], [27.45, 37.42], [26.45, 37.42], [26.45, 36.42] ]
P1 = Polygon( noktalar1 )

noktalar2 = [ [36.45, 36.42], [37.45, 36.42], [37.45, 37.42], [36.45, 37.42], [36.45, 36.42] ]
P2 = Polygon( noktalar2 )

noktalar3 = [ [32.840599, 39.938874], [32.838738, 39.93684], [32.837799,39.935813], [32.837575, 39.935495], [32.840599, 39.938874]]
P3 = Polygon( noktalar3 )

print(P1, type(P1))
print(P2, type(P2))
print(P3, type(P3))

print( P1.area, P2.area, P3.area )

print( P1.intersects( P2 ) )
print( P1.intersects( P3 ) )
print( P2.intersects( P3 ) )

# ST_Intersects == Polygon.instersects

print( Polygon.intersects( P1, P2 ) )

print( Polygon.intersection(P1, P2))



