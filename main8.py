
import sys
import geopandas
import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
from shapely.geometry import Point, Polygon
import shapely.wkt  # herhangi bir text formatindan, point, linestring veya polygona cevirmek icin
# ST_GeomFromText( 'POLYGON ((3 4), (......)' ) =========> (pyton) shapely.wkt.loads() # load string

path = "/home/mina5/Downloads/geopandas(2)/geopandas/temel ornekler/Turkey_shapefile/turkey_administrativelevels0_1_2/"
tr = gpd.read_file(path + 'tur_polbnda_adm1.shp')
tr = gpd.read_file(path + 'tur_polbna_adm2.shp')
# 32.59 40.75

# Kayit ediyoruz
tr.to_csv("tr.csv")

# Ornek parseller olusturuyoruz
parsel1 = [ [26.45, 36.42], [27.45, 36.42], [27.45, 37.42], [26.45, 37.42], [26.45, 36.42] ]
parsel2 = [ [36.45, 36.42], [37.45, 36.42], [37.45, 37.42], [36.45, 37.42], [36.45, 36.42] ]
parsel3 = [ [32.59, 40.75], [32.59, 40.85], [32.69, 40.85], [32.69, 40.85], [32.59, 40.75] ]
yeni_mahalle = [ [32.840599, 39.938874], [32.838738, 39.93684], [32.837799,39.935813], [32.837575, 39.935495], [32.840599, 39.938874]]

p = "POLYGON((32.7863540048828 39.97255988329443,32.88680318554689 39.95473822350395,32.87762443945314 39.93054784650609,32.88014702148436 39.89863024935207,32.79140965917969 39.85222693384191,32.672459894531265 39.83585281008209,32.63430274609376 39.83085287888003,32.597190243164064 39.84202307882488,32.595691015624986 39.867684333535145,32.61182134375002 39.91485362169062,32.66303878515628 39.95766192354099,32.7863540048828 39.97255988329443))"
p = shapely.wkt.loads( p )

p2 = "POLYGON((32.70365977015192 39.98715551150938,32.70692133631403 39.99333690573029,32.73215555872614 39.99136418111636,32.73061060633356 39.981894309854866,32.71155619349177 39.977290426057365,32.70365977015192 39.98715551150938))"
p2 = shapely.wkt.loads( p2 )

p3 = "POLYGON((32.726834056040595 39.97360709568655,32.71996760096247 39.98728703635963,32.728550669810126 40.002279209336635,32.77421259607966 39.99780820390815,32.76906275477106 39.97255467911879,32.726834056040595 39.97360709568655))"
p3 = shapely.wkt.loads( p3 )

# Ornek polygonlar olusturuyoruz
polygon_geom1 = Polygon( parsel1 )
polygon_geom2 = Polygon( parsel2 )
polygon_geom3 = Polygon( parsel3 )
polygon_yenimahalle = Polygon( yeni_mahalle )

# crs = coordinate reference system
# 4326
# 2 satirli, geo pandas dataframe olusturuk!
# polygon_geom3, polygon_yenimahalle, p,
polygon = gpd.GeoDataFrame( geometry=[  p2, p3 ] )


# YENIMAHALLE
# adm2_en

arkazemin = tr[ (tr['adm1'] == 'TUR006') & (tr['adm2_en'] == 'YENIMAHALLE') ].boundary.plot()
polygon.plot(ax = arkazemin, color = 'red', alpha=0.25) # alpha = 1.0 %100 ayni renkte, transparent olmadan!


plt.show()



# ===============
# Buradan sonrasi folium
# ===============
import folium
polygon.crs = "EPSG:4326"
m = folium.Map([28.726834056040595, 44.97360709568655], zoom_start=5, tiles="OpenStreetMap")
q = folium.GeoJson(polygon, style_function=lambda x: {'fillColor': 'orange', 'color': 'purple'})
q.add_to(m)
m.save("OpenStreetMap" + ".html")
"""
# the map might not be displayed
sim_geo = gpd.GeoSeries(r['geometry']).simplify(tolerance=0.001)
geo_j = sim_geo.to_json()
geo_j = folium.GeoJson(data=geo_j, style_function=lambda x: {'fillColor': random.choice(colors)})
# folium.Popup(r['BoroName']).add_to(geo_j)
geo_j.add_to(m)
"""