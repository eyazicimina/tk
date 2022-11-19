import geopandas as gpd
import folium
import matplotlib.pyplot as plt

path = gpd.datasets.get_path('nybb')
df = gpd.read_file(path)
df.head()

#df.plot(figsize=(6, 6))
#plt.show()
df = df.to_crs(epsg=4326)
m = folium.Map(location=[40.70, -73.94], zoom_start=10, tiles='CartoDB positron')
#! map = folium.Map(location=[4, 10], tiles="Stamen Terrain", zoom_start=3)

df.to_csv("ny.csv")
import random
colors = ['red', 'blue', 'green', 'orange', 'pink', 'navy']
for _, r in df.iterrows():
    # Without simplifying the representation of each borough,
    # the map might not be displayed
    sim_geo = gpd.GeoSeries(r['geometry']).simplify(tolerance=0.001)
    geo_j = sim_geo.to_json()
    geo_j = folium.GeoJson(data=geo_j, style_function=lambda x: {'fillColor': random.choice(colors)})
    #folium.Popup(r['BoroName']).add_to(geo_j)
    geo_j.add_to(m)

print(len(df))

m.save("x.html")