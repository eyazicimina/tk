#: Kütüphaneleri import etme
import sys
from OSMPythonTools.overpass import overpassQueryBuilder
from OSMPythonTools.api import Api
from OSMPythonTools.nominatim import Nominatim
from OSMPythonTools.overpass import Overpass

#: Api'leri başlatma
overpass = Overpass()
nominatim = Nominatim()
api = Api()

#
def özellikÇıkar( nesne: object, hariç: list = [] ) -> dict:
    info = {}
    for a in dir( nesne ):
        if a[0] != "_" and a not in hariç:
            method = getattr( nesne, a )
            info[a] = method()
    return info

def sorgula( girdi, ekstra = 10 ):
    if type(girdi) is int:
        sonuc = api.query(f"way/{girdi}")
        return özellikÇıkar( sonuc, ["fromId", "tag", "toXML"] )
    if type(girdi) is str:
        sonuc = nominatim.query(girdi, wkt=True)
        return özellikÇıkar( sonuc )
    if type(girdi) is tuple:
        if type(girdi[0]) is float:
            sonuc = nominatim.query(girdi[0], girdi[1], reverse=True, zoom= ekstra)
            return özellikÇıkar( sonuc )
        if type(girdi[0]) is str:
            loc = nominatim.query( girdi[0] )
            query = overpassQueryBuilder(area=loc, elementType='node', selector=girdi[1], out='body')
            sonuc = overpass.query(query)
            return özellikÇıkar( sonuc, ["timestamp_area_base"] )
    raise Exception("Bilinmeyen format")

print( "1", sorgula(473223865) )
print( "2", sorgula("Cumhuriyet, Üsküdar") )
print( "3", sorgula(( 49.4093582, 8.694724 )) )
print( "4", sorgula(( "Cumhuriyet, Üsküdar", '"highway"="bus_stop"' )) )


s1 = sorgula(473223865)
s2 = sorgula("Cumhuriyet, Üsküdar")
s3 = sorgula(( 49.4093582, 8.694724 ))
s4 = sorgula(( "Cumhuriyet, Üsküdar", '"highway"="bus_stop"' ))

s1 = list(s1.keys())
s2 = list(s2.keys())
s3 = list(s3.keys())
s4 = list(s4.keys())

birleşmiş = s1 + s2 + s3 + s4
birleşmiş = sorted(birleşmiş)
yegane = set(birleşmiş)

print(len(yegane))

import collections
frequency = dict(collections.Counter(birleşmiş))
print(frequency)

for item in frequency:
    if frequency[item] == 2:
        print(item)


import pandas as pd
df = pd.DataFrame(columns = list(yegane))



df.loc[len(df)] = {s:1 for s in s1}
df.loc[len(df)] = {s:1 for s in s2}
df.loc[len(df)] = {s:1 for s in s3}
df.loc[len(df)] = {s:1 for s in s4}
print(df)

# df.to_csv("şablon.csv", sep=";")


# polygon içindeki...
# iki nokta arasında

# kaydet
# oku
# networkx
# dönüştür (xml, json, polygon, KML, GML, SHP, OSM)
# parse (polygon, json, dict ....)






temelSorgu = pd.DataFrame(columns =
                          ["temelSorguId", "cacheTimestamp", "cacheVersion", "queryString", "other"])
alan = pd.DataFrame(columns =
                    ["alanId", "temelSorguId", "id", "areaId", "typeIdShort", "type", "typeId"])
adres = pd.DataFrame(columns =
                     ["adresId", "alanId", "address", "displayName", "isReverse", "wkt"])
node = pd.DataFrame(columns =
                    ["nodeId", "alanId", "countNodes", "generator", "nodes", "version",
                     "valid", "copyright"])

