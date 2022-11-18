import sys
import pandas as pd  # ===> postgre sql
import geopandas     # ===> postgis
from shapely.geometry import Point
import matplotlib.pyplot as plt
import numpy as np

from siniflar import Adres, GENEL_SRID, Nokta
# from siniflar import *
# import siniflar

"""
data = np.array([1,45,67,43,123])
plt.plot(data)
plt.show()
"""
"""
Boylam ve enlemlerden oluşturma (1)
=============================
Şehirleri ve bunların ilgili boylam ve enlemlerini içeren bir ``DataFrame`` düşünelim.
"""

# 1- df = pd.read_csv(".....")
# 2- bos data frame olusturma
df = pd.DataFrame(columns = ['vara', 'varb'])

vara_verileri = [1,2,3]
varb_verileri = ['ahmet', 'mustafa', 'canan']

# Dataframe e teker teker satir ekleme
for i in range(len(vara_verileri)):
    df.loc[ len(df) ] = [ vara_verileri[i], varb_verileri[i] ]
print(df)

# 3:
df = pd.DataFrame(
    {
        'City': ['Buenos Aires', 'Brasilia', 'Santiago', 'Bogota', 'Caracas'],
        'Country': ['Argentina', 'Brazil', 'Chile', 'Colombia', 'Venezuela'],
        'Latitude': [-34.58, -15.78, -33.45, 4.60, 10.48],
        'Longitude': [-58.66, -47.91, -70.66, -74.08, -66.86]
    }
)
# 5x4 matrix, 5x4 data frame

print(df)
print(df.shape)
"""
Bir ``GeoDataFrame``, ``shapely`` bir nesneye ihtiyaç duyar, 
bu nedenle **Boylam** ve **Enlem** öğelerinin bir demeti olarak 
yeni bir **Koordinatlar** sütunu oluştururuz:
"""

# postgre-sql
# select, insert, update, delete, create .....
# offset, order by .....
# big int, integer, double, decimal, varchar = (str)
# GEOMETRY ---> post-gis
#   point (nokta)
#   linestring (dogrultu)
#   polygon (cokgen)

d1 = {
    'Ahmet':  34,
    'Mehmet': 42,
    'Canan':  45,
}

d2 = [
    ('Ahmet', 34),
    ('Mehmet', 42),
    ('Canan', 45)
]

isimler = ['Ahmet', 'Mehmet', 'Canan']
yaslar = [34, 42, 45]

#! BU DEGIL: hepsi = ['Ahmet', 'Mehmet', 'Canan', 34, 42, 45]

print( "ziplenen", zip( isimler, yaslar ) )
print( "ziplenen", list(zip( isimler, yaslar )) )
print( "d2      ", d2 )

print( "ziplenen 2", dict(zip(isimler, yaslar)))
print( "d1        ", d1)

# Zip: Karsilik, ayni sayida !! olan iki listeyi !!, birlestirir (cift)
# Yani, ya bir tuple yapiyor, (list fonksiyonu kullanilirsa)
#       ya da bir dictionary yapior, (dict fonksiyonu kullanilirsa)

print(df)
df['Coordinates'] = list(zip(df.Longitude, df.Latitude))

print( df.Latitude ) # df['Latitude']

print(df.dtypes)
print(df)

# print(dir(Point))
# ['area', 'array_interface', 'array_interface_base', 'boundary', 'bounds', 'buffer', 'centroid', 'contains', 'convex_hull', 'coords', 'covered_by', 'covers', 'crosses', 'ctypes', 'difference', 'disjoint', 'distance', 'empty', 'envelope', 'equals', 'equals_exact', 'geom_type', 'geometryType', 'has_z', 'hausdorff_distance', 'impl', 'interpolate', 'intersection', 'intersects', 'is_closed', 'is_empty', 'is_ring', 'is_simple', 'is_valid', 'length', 'minimum_clearance', 'minimum_rotated_rectangle', 'normalize', 'overlaps', 'project', 'relate', 'relate_pattern', 'representative_point', 'simplify', 'svg', 'symmetric_difference', 'touches', 'type', 'union', 'within', 'wkb', 'wkb_hex', 'wkt', 'x', 'xy', 'y', 'z']

# Ardından demetler (tuples) ``Point`` olarak dönüştürülür:
df['Coordinates'] = df['Coordinates'].apply(Point)



# df['a'] = df['a'].astype(int) # a dedigimiz degisken onceden, FLOAT ti simdi integer

print(df)
a = df.iloc[0]['Coordinates']
print(a)

b = True
print(b)

# Veri yapisi, custom
class Bina:
    adres = None
    yukseklik = None
    m2 = None

mybina = Bina()


# (1) Normal datatype, str (string - metin)
adres = "Esatpasa cad. Akcam sok, No:15, Uskudar, Istanbul"
koordinat = "34.56, 43.34"

# (2) Elastik tanimalama
a = {'Sokak': 'Akcam', 'Cadde': '....'}
koordinat2 = (34.56, 43.34)

# (3) Sinifsal tanimlama

n = Nokta()
n.enlem = 34.56    # veri yazdik
n.boylam = 45.43
n.srid = 0

print(n.enlem) # veri okuma
print(n.boylam)

print( n )  # <__main__.Nokta object>

# Ahmet's car, Ahmet in arabasi (') ==> (.)
# Class = Sablon
a = Adres()
a.Sehir = "Ankara"
a.Ilce = "Polatli"
a.Cadde = "Cumhuriyet"
a.Mahalle = "Avdanlik"
a.Sokak = "Cesme"
a.No = 3

print(a)

sokak = a.Sokak






print(df)
q = df.iloc[4]['Coordinates']
print(q, type(q))
"""
class Point:
    ...

    def __str__(self):
        return f"POINT ({self.x}, {self.y})"
"""

# Artık daha önceden oluşturulan koordinatlar ile
# ``geometry`` ayarını yaparak ``GeoDataFrame``i oluşturulur.
gdf = geopandas.GeoDataFrame(df, geometry='Coordinates')

#pd.read_csv("xxx.csv", parse_dates=['ParselizasyonTarihi'])

print('=============================================================')
print(gdf)
print(gdf.head())

# Koordinatların ülke düzeyinde bir harita üzerinde çizilmesi :

world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))
print(world, type(world))

# We restrict to South America.
bolge = world[world.continent == 'South America']
bolge.to_csv("bolge.csv")
print(bolge.columns)


# ax = world[world.continent == 'South America'].plot(color='white', edgecolor='black')


# df = df[ df['City'] == 'Istanbul' ]
# SQL Where : FILTRELEME


"""

gdf.plot(ax=ax, color='red')

plt.show()


path = "ornekveriTkgm.csv"
"""

"""
df = pd.DataFrame(
    {
        'City': ['Ankara', 'Istanbul'],
        'Country': ['Turkiye', 'Turkiye'],
        'Latitude': [39.925533, 41.015137],
        'Longitude': [32.866287, 28.979530]
    }
)

df['Coordinates'] = list(zip(df.Longitude, df.Latitude))
df['Coordinates'] = df['Coordinates'].apply(Point)
bizim = geopandas.GeoDataFrame(df, geometry='Coordinates')
dunya = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))
#asya = dunya[ dunya.continent == 'Asia' ]
#asya.to_csv("asya.csv")
# background
# ax1 = world[world.continent == 'Asia'].plot(color='lightgray', edgecolor='blue')
ax2 = world[world.name == 'Turkey'].plot(color='lightgray', edgecolor='blue')
# AX = zemin
bizim.plot(ax=ax2, color='yellow', edgecolor = 'red')
plt.show()
"""


"""
df = pd.read_csv("worldcities.csv")
df = df[ df['country'] == 'Turkey' ]
print(df['admin_name'])

lats = {}
lngs = {}

print(df['admin_name'].unique())

for an in df['admin_name'].unique():
    lats[ an ] = df[ df['admin_name'] == an ]['lat'].mean()
    lngs[ an ] = df[ df['admin_name'] == an ]['lng'].mean()

print(lats)
print(lngs)


df = pd.DataFrame(
    {
        'City': list(lats.keys()),
        'lat': list(lats.values()),
        'lng': list(lngs.values())
    }
)
df['Coordinates'] = list(zip(df.lng, df.lat))
df['Coordinates'] = df['Coordinates'].apply(Point)
bizim = geopandas.GeoDataFrame(df, geometry='Coordinates')
dunya = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))
#asya = dunya[ dunya.continent == 'Asia' ]
#asya.to_csv("asya.csv")
# background
# ax1 = world[world.continent == 'Asia'].plot(color='lightgray', edgecolor='blue')
ax2 = world[world.name == 'Turkey'].plot(color='lightgray', edgecolor='blue', column='pop_est')
# ax2 = dunya[dunya.continent == 'Asia'].plot(color='lightgray', edgecolor='blue')
# AX = zemin
bizim.plot(ax=ax2, color='yellow', edgecolor = 'red')
plt.show()
"""



"""
world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))
world = world[(world.pop_est>0) & (world.name!="Antarctica")]

# Bir float degisken kullanarak, renklendirme yapabilmek uzere
world['gdp_per_cap'] = world.gdp_md_est / world.pop_est
print(world['gdp_per_cap'])
# cmap = color map
# legend = Aciklayici gosterge
world.plot(column='gdp_per_cap', cmap='Oranges', legend=True)
plt.show()
"""






df = pd.read_csv("worldcities.csv")
df = df[ df['country'] == 'Turkey' ]
print(df['admin_name'])

lats = {}
lngs = {}
pops = {}

print(df['admin_name'].unique())

for an in df['admin_name'].unique():
    lats[ an ] = df[ df['admin_name'] == an ]['lat'].mean()
    lngs[ an ] = df[ df['admin_name'] == an ]['lng'].mean()
    pops[ an ] = df[ df['admin_name'] == an ]['population'].sum()

print(lats)
print(lngs)

df = pd.DataFrame(
    {
        'City': list(lats.keys()),
        'lat': list(lats.values()),
        'lng': list(lngs.values()),
        'pop': list(pops.values())
    }
)

df['Coordinates'] = list(zip(df.lng, df.lat))
df['Coordinates'] = df['Coordinates'].apply(Point)
bizim = geopandas.GeoDataFrame(df, geometry='Coordinates')
dunya = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))
#asya = dunya[ dunya.continent == 'Asia' ]
#asya.to_csv("asya.csv")
# background
# ax1 = world[world.continent == 'Asia'].plot(color='lightgray', edgecolor='blue')
ax2 = world[world.name == 'Turkey'].plot(color='lightgray', edgecolor='blue')
# ax2 = dunya[dunya.continent == 'Asia'].plot(color='lightgray', edgecolor='blue')
# AX = zemin
bizim[ bizim['pop'] > 500000 ].plot(ax=ax2, color='yellow', edgecolor = 'orange')
bizim[ (bizim['pop'] > 200000) & (bizim['pop'] <= 500000) ].plot(ax=ax2, color='blue', edgecolor = 'green')
bizim[ (bizim['pop'] <= 200000) ].plot(ax=ax2, color='red', edgecolor = 'brown')

# dpi = dot per inch

plt.show()

