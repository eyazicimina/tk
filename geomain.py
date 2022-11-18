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




#ax = world[world.continent == 'South America'].plot(color='white', edgecolor='black')
#gdf.plot(ax=ax, color='red')
#plt.show()

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
"""
bizim[ bizim['pop'] > 500000 ].plot(ax=ax2, color='yellow', markersize=150, edgecolor = 'orange')
bizim[ (bizim['pop'] > 200000) & (bizim['pop'] <= 500000) ].plot(ax=ax2, markersize=300, marker = 'D', color='blue', edgecolor = 'green')
bizim[ (bizim['pop'] <= 200000) ].plot(ax=ax2, marker = 'P', markersize=45, color='red', edgecolor = 'brown')
"""
# AYARLAR
renk_sayisi = 2
# SABIT
colors = ['red', 'green', 'blue', 'yellow', 'brown', 'gray', 'hotpink', 'darkviolet', 'darkorange', 'navy']




populasyonlar = sorted(list(bizim['pop'].unique()))

df['popsirasi'] = df['pop'].apply(lambda value: populasyonlar.index(value) )

maximum = bizim['popsirasi'].max()
minimum = bizim['popsirasi'].min()
poprange = maximum - minimum
limit = poprange / renk_sayisi

for i in range(renk_sayisi):
    p1 = bizim['popsirasi'].min() + i * limit
    p2 = bizim['popsirasi'].min() + (i+1) * limit
    sub = bizim[ (bizim['popsirasi'] > p1) & (bizim['popsirasi'] <= p2) ]
    sub.plot(ax=ax2, color=colors[i])

# plt.show()


world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))
print(world)

# Boundary, sadece dis cerceveyi cizer

world.geometry.boundary.plot(figsize=(20,16))
# plt.show()

# post_gis ST_GeometryType()
"""
SELECT ST_GeometryType(geom), COUNT(*)
FROM tablo
GROUP BY geom
"""

print(world.geometry.geom_type.value_counts())

print(dir(world.geometry))
"""
['T', '_AXIS_LEN', '_AXIS_ORDERS', '_AXIS_TO_AXIS_NUMBER', '_HANDLED_TYPES', 
'abs', 'add', 'add_prefix', 'add_suffix', 'affine_transform', 'agg', 'aggregate', 'align', 'all', 'any', 'append', 'apply', 'area', 'argmax', 'argmin', 'argsort', 'array', 'asfreq', 'asof', 'astype', 'at', 'at_time', 'attrs', 'autocorr', 'axes', 'backfill', 'between', 'between_time', 'bfill', 'bool', 'boundary', 'bounds', 'buffer', 'cascaded_union', 'centroid', 'clip', 'clip_by_rect', 'combine', 'combine_first', 'compare', 'contains', 'convert_dtypes', 'convex_hull', 'copy', 'corr', 'count', 'cov', 'covered_by', 'covers', 'crosses', 'crs', 'cummax', 'cummin', 'cumprod', 'cumsum', 'cx', 'describe', 'diff', 'difference', 'disjoint', 'distance', 'div', 'divide', 'divmod', 'dot', 'drop', 'drop_duplicates', 'droplevel', 'dropna', 'dtype', 'dtypes', 'duplicated', 'empty', 'envelope', 'eq', 'equals', 'estimate_utm_crs', 'ewm', 'expanding', 'explode', 'explore', 'exterior', 'factorize', 'ffill', 'fillna', 'filter', 'first', 'first_valid_index', 'flags', 'floordiv', 'from_file', 'from_wkb', 'from_wkt', 'from_xy', 'ge', 'geom_almost_equals', 'geom_equals', 'geom_equals_exact', 
'geom_type', 'geometry', 'get', 'groupby', 'gt', 'has_sindex', 'has_z', 'hasnans', 
'head', 'hist', 'iat', 'idxmax', 'idxmin', 'iloc', 'index', 'infer_objects', 'info', 'interiors', 
'interpolate', 'intersection', 'intersects', 'is_empty', 'is_monotonic', 'is_monotonic_decreasing',
'is_monotonic_increasing', 'is_ring', 'is_simple', 'is_unique', 'is_valid', 'isin', 'isna', 
'isnull', 'item', 'items', 'iteritems', 'keys', 'kurt', 'kurtosis', 'last', 'last_valid_index', 
'le', 'length', 'loc', 'lt', 'mad', 'make_valid', 'map', 'mask', 'max', 'mean', 'median', 
'memory_usage', 'min', 'mod', 'mode', 'mul', 'multiply', 'name', 'nbytes', 'ndim', 'ne', 
'nlargest', 'normalize', 'notna', 'notnull', 'nsmallest', 'nunique', 'overlaps', 'pad', 
'pct_change', 'pipe', 'plot', 'pop', 'pow', 'prod', 'product', 'project', 'quantile',
'radd', 'rank', 'ravel', 'rdiv', 'rdivmod', 'reindex', 'reindex_like', 'relate', 
'rename', 'rename_axis', 'reorder_levels', 'repeat', 'replace', 'representative_point',
'resample', 'reset_index', 'rfloordiv', 'rmod', 'rmul', 'rolling', 'rotate', 'round', 
'rpow', 'rsub', 'rtruediv', 'sample', 'scale', 'searchsorted', 'select', 'sem', 'set_axis',
'set_crs', 'set_flags', 'shape', 'shift', 'simplify', 'sindex', 'size', 'skew', 'slice_shift', 
'sort_index', 'sort_values', 'squeeze', 'std', 'sub', 'subtract', 'sum', 'swapaxes', 'swaplevel',
'symmetric_difference', 'tail', 'take', 'to_clipboard', 'to_crs', 'to_csv', 'to_dict', 'to_excel', 
'to_file', 'to_frame', 'to_hdf', 'to_json', 'to_latex', 'to_list', 'to_markdown', 'to_numpy', 
'to_period', 'to_pickle', 'to_sql', 'to_string', 'to_timestamp', 'to_wkb', 'to_wkt', 'to_xarray',
'total_bounds', 'touches', 'transform', 'translate', 'transpose', 'truediv', 'truncate', 'type', 
'tz_convert', 'tz_localize', 'unary_union', 'union', 'unique', 'unstack', 'update', 'value_counts', 
'values', 'var', 'view', 'where', 'within', 'x', 'xs', 'y', 'z']
"""


"""
WKT formatından oluşturma (2)
===============
WKT formatında koordinatlara sahip bir ``DataFrame``
"""




import pandas as pd  # ===> postgre sql
import geopandas     # ===> postgis
from shapely.geometry import Point
import matplotlib.pyplot as plt
import numpy as np

df = pd.DataFrame(
    {'City': ['Buenos Aires', 'Brasilia', 'Santiago', 'Bogota', 'Caracas'],
     'Country': ['Argentina', 'Brazil', 'Chile', 'Colombia', 'Venezuela'],
     'Coordinates': ['POINT(-34.58 -58.66)', 'POINT(-15.78 -47.91)',
                     'POINT(-33.45 -70.66)', 'POINT(4.60 -74.08)',
                     'POINT(10.48 -66.86)']})

from shapely import wkt
df['Coordinates'] = df['Coordinates'].apply(wkt.loads)
gdf = geopandas.GeoDataFrame(df, geometry='Coordinates')
world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))
ax = world[world.continent == 'South America'].plot(color='white', edgecolor='black')
gdf.plot(ax=ax)
plt.show()


