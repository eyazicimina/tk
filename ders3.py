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

# Auto Identity = Auto Increment
son_idler = { "temelSorgu": 0, "alan": 0, "adres": 0,"node": 0}

def idver( tablo: str ) -> int:
    sonid = son_idler[ tablo ] + 1
    son_idler[tablo] = sonid
    return sonid

sorgular = [
    473223865,
    "Cumhuriyet, Üsküdar",
    ( 49.4093582, 8.694724 ),
    ( "Cumhuriyet, Üsküdar", '"highway"="bus_stop"' )
]


#: Her bir sorgu için
for sorgu in sorgular:
    #: Sorgulama işlemi yap
    sonuc = sorgula( sorgu )
    #: Her bir sorguda, mutlaka temel sorgu vardır!
    #: Temel sorgu için yeni bir id üret!
    temelSorguId = idver("temelSorgu")
    yeni_kayıt = {
        "temelSorguId": temelSorguId,
        "cacheTimestamp": sonuc["cacheTimestamp"],
        "cacheVersion": sonuc["cacheVersion"],
        "queryString": sonuc["queryString"]
    }
    #: Temel sorgu tablosuna ekle
    temelSorgu.loc[ len(temelSorgu) ] = yeni_kayıt
    #: Alan tablosuna ekleme yap
    alanId = idver("alan")
    yeni_kayıt2 = {}
    #: Temel bağlantı kolonlarını dolduralım
    yeni_kayıt2["alanId"] = alanId
    yeni_kayıt2["temelSorguId"] = temelSorguId

    # ["id", "areaId", "typeIdShort", "type", "typeId"]




    # print("!", sonuc)
    # ["alanId", "temelSorguId", "id", "areaId", "typeIdShort", "type", "typeId"]

"""
! {'apiVersion': '0.6', 'areaId': 2873223865, 'attribution': 'http://www.openstreetmap.org/copyright', 'cacheTimestamp': '2022-11-04T15:23:49.505200', 'cacheVersion': '1.0', 'centerLat': None, 'centerLon': None, 'changeset': '114040647', 'copyright': 'OpenStreetMap and contributors', 'countMembers': 0, 'countNodes': 23, 'generator': 'CGImap 0.8.8 (4108215 spike-07.openstreetmap.org)', 'geometry': {"coordinates": [[[32.83615, 39.850298], [32.836171, 39.849481], [32.836307, 39.849416], [32.836359, 39.84935], [32.836362, 39.849255], [32.83639, 39.848428], [32.836553, 39.848366], [32.836633, 39.848319], [32.836713, 39.848262], [32.836757, 39.848224], [32.83679, 39.848171], [32.836818, 39.848119], [32.837018, 39.848244], [32.837211, 39.848487], [32.837306, 39.848487], [32.837307, 39.848535], [32.837321, 39.84859], [32.83759, 39.849091], [32.837274, 39.849246], [32.837366, 39.849785], [32.837458, 39.85013], [32.83698, 39.850331], [32.83615, 39.850298]]], "type": "Polygon"}, 'history': None, 'id': 473223865, 'isValid': True, 'lat': None, 'license': 'http://opendatacommons.org/licenses/odbl/1-0/', 'lon': None, 'members': [], 'nodes': [<OSMPythonTools.api.ApiResult object at 0x0000015B5DDE6B60>, <OSMPythonTools.api.ApiResult object at 0x0000015B5DDE6E30>, <OSMPythonTools.api.ApiResult object at 0x0000015B5DDE7040>, <OSMPythonTools.api.ApiResult object at 0x0000015B5DDE7250>, <OSMPythonTools.api.ApiResult object at 0x0000015B5DDE7460>, <OSMPythonTools.api.ApiResult object at 0x0000015B5DDE7670>, <OSMPythonTools.api.ApiResult object at 0x0000015B5DDE7880>, <OSMPythonTools.api.ApiResult object at 0x0000015B5DDE7A90>, <OSMPythonTools.api.ApiResult object at 0x0000015B5DDE7CA0>, <OSMPythonTools.api.ApiResult object at 0x0000015B5DDE7EB0>, <OSMPythonTools.api.ApiResult object at 0x0000015B5DDE7F70>, <OSMPythonTools.api.ApiResult object at 0x0000015B5DDE7F40>, <OSMPythonTools.api.ApiResult object at 0x0000015B5DE20520>, <OSMPythonTools.api.ApiResult object at 0x0000015B5DE20730>, <OSMPythonTools.api.ApiResult object at 0x0000015B5DE20940>, <OSMPythonTools.api.ApiResult object at 0x0000015B5DE20B50>, <OSMPythonTools.api.ApiResult object at 0x0000015B5DE20D60>, <OSMPythonTools.api.ApiResult object at 0x0000015B5DE20F70>, <OSMPythonTools.api.ApiResult object at 0x0000015B5DE21180>, <OSMPythonTools.api.ApiResult object at 0x0000015B5DE21390>, <OSMPythonTools.api.ApiResult object at 0x0000015B5DE215A0>, <OSMPythonTools.api.ApiResult object at 0x0000015B5DE217B0>, <OSMPythonTools.api.ApiResult object at 0x0000015B5DE219C0>], 'queryString': 'way/473223865', 'tags': {'barrier': 'fence', 'landuse': 'residential', 'name': 'TBMM Eski Lojmanları Sitesi'}, 'timestamp': datetime.datetime(2021, 11, 20, 21, 1, 48, tzinfo=tzutc()), 'type': 'way', 'typeId': 'way/473223865', 'typeIdShort': 'w473223865', 'uid': '14474713', 'user': 'pinkyPrii', 'userid': '14474713', 'version': 8, 'visible': 'true'}
! {'address': None, 'areaId': 3603866327, 'cacheTimestamp': '2022-11-05T10:23:28.504432', 'cacheVersion': '1.0', 'displayName': 'Cumhuriyet Mahallesi, Üsküdar, İstanbul, Marmara Bölgesi, 34697, Türkiye', 'id': 3866327, 'isReverse': False, 'queryString': 'Cumhuriyet, Üsküdar', 'toJSON': [{'place_id': 298278074, 'licence': 'Data © OpenStreetMap contributors, ODbL 1.0. https://osm.org/copyright', 'osm_type': 'relation', 'osm_id': 3866327, 'boundingbox': ['41.0056665', '41.015203', '29.0726392', '29.0894421'], 'lat': '41.0108797', 'lon': '29.0807595', 'display_name': 'Cumhuriyet Mahallesi, Üsküdar, İstanbul, Marmara Bölgesi, 34697, Türkiye', 'class': 'boundary', 'type': 'administrative', 'importance': 0.45585065784831785, 'icon': 'https://nominatim.openstreetmap.org/ui/mapicons/poi_boundary_administrative.p.20.png', 'geotext': 'POLYGON((29.0726392 41.0056665,29.0738694 41.005781,29.07535 41.005969,29.076774 41.0063719,29.0775729 41.0066838,29.0785461 41.0070638,29.0814741 41.0082072,29.08346 41.0088827,29.0851591 41.0092204,29.0870841 41.0094598,29.0888092 41.0094893,29.0890691 41.0094836,29.0894421 41.0094753,29.0893821 41.0100059,29.0893227 41.0102341,29.0892849 41.0103792,29.0892807 41.0104834,29.0892748 41.0106322,29.0892579 41.0109075,29.0893658 41.0110954,29.0893737 41.0112263,29.0893546 41.0113694,29.0892576 41.0115952,29.0891316 41.0119404,29.0886524 41.0119708,29.0881341 41.0119357,29.0876894 41.0136003,29.087473 41.0140839,29.0873369 41.0143716,29.0870082 41.0150678,29.085803 41.0147199,29.0852201 41.0145594,29.0834767 41.0141223,29.0820926 41.0139442,29.0815401 41.0140332,29.081068 41.0144946,29.0808213 41.0147092,29.0798235 41.0150006,29.0791154 41.015203,29.0784019 41.014863,29.0772378 41.0143854,29.0775865 41.0137499,29.076701 41.0137941,29.0753174 41.0138632,29.0750211 41.0116305,29.0748212 41.0111856,29.0746415 41.0108253,29.074569 41.0103517,29.0745181 41.0100906,29.0744081 41.0096089,29.0742579 41.0092324,29.0740567 41.0087082,29.0736946 41.0080787,29.0734237 41.0076294,29.0730777 41.0069615,29.0729275 41.0066194,29.0728497 41.0063036,29.0727049 41.0058604,29.0726392 41.0056665))'}], 'type': 'relation', 'typeId': 'relation/3866327', 'typeIdShort': 'r3866327', 'wkt': 'POLYGON((29.0726392 41.0056665,29.0738694 41.005781,29.07535 41.005969,29.076774 41.0063719,29.0775729 41.0066838,29.0785461 41.0070638,29.0814741 41.0082072,29.08346 41.0088827,29.0851591 41.0092204,29.0870841 41.0094598,29.0888092 41.0094893,29.0890691 41.0094836,29.0894421 41.0094753,29.0893821 41.0100059,29.0893227 41.0102341,29.0892849 41.0103792,29.0892807 41.0104834,29.0892748 41.0106322,29.0892579 41.0109075,29.0893658 41.0110954,29.0893737 41.0112263,29.0893546 41.0113694,29.0892576 41.0115952,29.0891316 41.0119404,29.0886524 41.0119708,29.0881341 41.0119357,29.0876894 41.0136003,29.087473 41.0140839,29.0873369 41.0143716,29.0870082 41.0150678,29.085803 41.0147199,29.0852201 41.0145594,29.0834767 41.0141223,29.0820926 41.0139442,29.0815401 41.0140332,29.081068 41.0144946,29.0808213 41.0147092,29.0798235 41.0150006,29.0791154 41.015203,29.0784019 41.014863,29.0772378 41.0143854,29.0775865 41.0137499,29.076701 41.0137941,29.0753174 41.0138632,29.0750211 41.0116305,29.0748212 41.0111856,29.0746415 41.0108253,29.074569 41.0103517,29.0745181 41.0100906,29.0744081 41.0096089,29.0742579 41.0092324,29.0740567 41.0087082,29.0736946 41.0080787,29.0734237 41.0076294,29.0730777 41.0069615,29.0729275 41.0066194,29.0728497 41.0063036,29.0727049 41.0058604,29.0726392 41.0056665))'}
! {'address': {'city': 'Heidelberg', 'state': 'Baden-Württemberg', 'ISO3166-2-lvl4': 'DE-BW', 'country': 'Deutschland', 'country_code': 'de'}, 'areaId': 3600285864, 'cacheTimestamp': '2022-11-05T11:42:06.557488', 'cacheVersion': '1.0', 'displayName': 'Heidelberg, Baden-Württemberg, Deutschland', 'id': 285864, 'isReverse': True, 'queryString': [49.4093582, 8.694724], 'toJSON': [{'place_id': 298086493, 'licence': 'Data © OpenStreetMap contributors, ODbL 1.0. https://osm.org/copyright', 'osm_type': 'relation', 'osm_id': 285864, 'lat': '49.4093582', 'lon': '8.694724', 'display_name': 'Heidelberg, Baden-Württemberg, Deutschland', 'address': {'city': 'Heidelberg', 'state': 'Baden-Württemberg', 'ISO3166-2-lvl4': 'DE-BW', 'country': 'Deutschland', 'country_code': 'de'}, 'boundingbox': ['49.3520029', '49.4596927', '8.5731788', '8.7940496']}], 'type': 'relation', 'typeId': 'relation/285864', 'typeIdShort': 'r285864', 'wkt': None}
! {'areas': [], 'cacheTimestamp': '2022-11-05T12:05:16.223676', 'cacheVersion': '1.0', 'copyright': 'The data included in this document is from www.openstreetmap.org. The data is made available under ODbL.', 'countAreas': 0, 'countElements': 20, 'countNodes': 20, 'countRelations': 0, 'countWays': 0, 'elements': [<OSMPythonTools.element.Element object at 0x0000015B5DDE6A10>, <OSMPythonTools.element.Element object at 0x0000015B5DDE7CA0>, <OSMPythonTools.element.Element object at 0x0000015B5DDE7A90>, <OSMPythonTools.element.Element object at 0x0000015B5DDE4250>, <OSMPythonTools.element.Element object at 0x0000015B5DDE6B00>, <OSMPythonTools.element.Element object at 0x0000015B5DDE7040>, <OSMPythonTools.element.Element object at 0x0000015B5DDE56C0>, <OSMPythonTools.element.Element object at 0x0000015B5DE20F70>, <OSMPythonTools.element.Element object at 0x0000015B5DE21A20>, <OSMPythonTools.element.Element object at 0x0000015B5DE21DE0>, <OSMPythonTools.element.Element object at 0x0000015B5DE22050>, <OSMPythonTools.element.Element object at 0x0000015B5DE21CF0>, <OSMPythonTools.element.Element object at 0x0000015B5DE217B0>, <OSMPythonTools.element.Element object at 0x0000015B5DE20520>, <OSMPythonTools.element.Element object at 0x0000015B5DE21BD0>, <OSMPythonTools.element.Element object at 0x0000015B5DE21EA0>, <OSMPythonTools.element.Element object at 0x0000015B5DE21F60>, <OSMPythonTools.element.Element object at 0x0000015B5DE21D80>, <OSMPythonTools.element.Element object at 0x0000015B5DE21390>, <OSMPythonTools.element.Element object at 0x0000015B5DE20730>], 'generator': 'Overpass API 0.7.59 e21c39fe', 'isValid': True, 'nodes': [<OSMPythonTools.element.Element object at 0x0000015B5DDE6A10>, <OSMPythonTools.element.Element object at 0x0000015B5DDE7CA0>, <OSMPythonTools.element.Element object at 0x0000015B5DDE7A90>, <OSMPythonTools.element.Element object at 0x0000015B5DDE4250>, <OSMPythonTools.element.Element object at 0x0000015B5DDE6B00>, <OSMPythonTools.element.Element object at 0x0000015B5DDE7040>, <OSMPythonTools.element.Element object at 0x0000015B5DDE56C0>, <OSMPythonTools.element.Element object at 0x0000015B5DE20F70>, <OSMPythonTools.element.Element object at 0x0000015B5DE21A20>, <OSMPythonTools.element.Element object at 0x0000015B5DE21DE0>, <OSMPythonTools.element.Element object at 0x0000015B5DE22050>, <OSMPythonTools.element.Element object at 0x0000015B5DE21CF0>, <OSMPythonTools.element.Element object at 0x0000015B5DE217B0>, <OSMPythonTools.element.Element object at 0x0000015B5DE20520>, <OSMPythonTools.element.Element object at 0x0000015B5DE21BD0>, <OSMPythonTools.element.Element object at 0x0000015B5DE21EA0>, <OSMPythonTools.element.Element object at 0x0000015B5DE21F60>, <OSMPythonTools.element.Element object at 0x0000015B5DE21D80>, <OSMPythonTools.element.Element object at 0x0000015B5DE21390>, <OSMPythonTools.element.Element object at 0x0000015B5DE20730>], 'queryString': '[timeout:25][out:json];area(3603866327)->.searchArea;(node["highway"="bus_stop"](area.searchArea);); out body;', 'relations': [], 'remark': None, 'timestamp_osm_base': datetime.datetime(2022, 11, 5, 9, 2, 44, tzinfo=tzutc()), 'toJSON': {'version': 0.6, 'generator': 'Overpass API 0.7.59 e21c39fe', 'osm3s': {'timestamp_osm_base': '2022-11-05T09:02:44Z', 'timestamp_areas_base': '2022-11-05T08:44:26Z', 'copyright': 'The data included in this document is from www.openstreetmap.org. The data is made available under ODbL.'}, 'elements': [{'type': 'node', 'id': 927955126, 'lat': 41.0105176, 'lon': 29.0838191, 'tags': {'bus': 'yes', 'highway': 'bus_stop', 'public_transport': 'platform'}}, {'type': 'node', 'id': 927955128, 'lat': 41.0118129, 'lon': 29.0880248, 'tags': {'bus': 'yes', 'highway': 'bus_stop', 'name': 'Açan Sokak', 'public_transport': 'platform'}}, {'type': 'node', 'id': 4486289891, 'lat': 41.0106672, 'lon': 29.08703, 'tags': {'bus': 'yes', 'highway': 'bus_stop', 'name': 'Üçyol', 'public_transport': 'platform'}}, {'type': 'node', 'id': 5239669821, 'lat': 41.0137177, 'lon': 29.0753145, 'tags': {'bus': 'yes', 'highway': 'bus_stop', 'name': 'Çeşme', 'public_transport': 'platform'}}, {'type': 'node', 'id': 7132896793, 'lat': 41.0119592, 'lon': 29.0880413, 'tags': {'bus': 'yes', 'highway': 'bus_stop', 'name': 'Açan Sokak', 'public_transport': 'platform'}}, {'type': 'node', 'id': 7132896810, 'lat': 41.0107082, 'lon': 29.0872894, 'tags': {'bus': 'yes', 'highway': 'bus_stop', 'name': 'Üçyol', 'public_transport': 'platform'}}, {'type': 'node', 'id': 7132896836, 'lat': 41.0146126, 'lon': 29.0856502, 'tags': {'bus': 'yes', 'highway': 'bus_stop', 'name': 'Dörtyol', 'public_transport': 'platform'}}, {'type': 'node', 'id': 7138816397, 'lat': 41.014198, 'lon': 29.0812956, 'tags': {'bus': 'yes', 'highway': 'bus_stop', 'name': 'Cumhuriyet Mahallesi Muhtarlığı', 'public_transport': 'platform'}}, {'type': 'node', 'id': 7138854975, 'lat': 41.0127702, 'lon': 29.0822821, 'tags': {'bus': 'yes', 'highway': 'bus_stop', 'name': 'Özanakent', 'public_transport': 'platform'}}, {'type': 'node', 'id': 7138854976, 'lat': 41.0127089, 'lon': 29.0824285, 'tags': {'bus': 'yes', 'highway': 'bus_stop', 'name': 'Özanakent', 'public_transport': 'platform'}}, {'type': 'node', 'id': 7138854983, 'lat': 41.0091346, 'lon': 29.0800034, 'tags': {'bus': 'yes', 'highway': 'bus_stop', 'name': 'Şehit Recep Büyük', 'public_transport': 'platform'}}, {'type': 'node', 'id': 7138854984, 'lat': 41.0091184, 'lon': 29.0801536, 'tags': {'bus': 'yes', 'highway': 'bus_stop', 'name': 'Şehit Recep Büyük', 'public_transport': 'platform'}}, {'type': 'node', 'id': 7138855286, 'lat': 41.0103895, 'lon': 29.0791987, 'tags': {'bus': 'yes', 'highway': 'bus_stop', 'name': 'Karlıdere Caddesi', 'public_transport': 'platform'}}, {'type': 'node', 'id': 7138855287, 'lat': 41.0104077, 'lon': 29.0793073, 'tags': {'bus': 'yes', 'highway': 'bus_stop', 'name': 'Karlıdere Caddesi', 'public_transport': 'platform'}}, {'type': 'node', 'id': 7138855296, 'lat': 41.0071632, 'lon': 29.0776645, 'tags': {'bus': 'yes', 'highway': 'bus_stop', 'name': 'Deniz Sokak', 'public_transport': 'platform'}}, {'type': 'node', 'id': 7138855297, 'lat': 41.0072199, 'lon': 29.0781527, 'tags': {'bus': 'yes', 'highway': 'bus_stop', 'name': 'Deniz Sokak', 'public_transport': 'platform'}}, {'type': 'node', 'id': 7138855300, 'lat': 41.0105838, 'lon': 29.0747141, 'tags': {'bus': 'yes', 'highway': 'bus_stop', 'name': 'Kırklar', 'public_transport': 'platform'}}, {'type': 'node', 'id': 7138862587, 'lat': 41.0077486, 'lon': 29.0736317, 'tags': {'bench': 'no', 'bus': 'yes', 'highway': 'bus_stop', 'name': 'Devlet Su İşleri', 'public_transport': 'platform', 'shelter': 'yes'}}, {'type': 'node', 'id': 7138862589, 'lat': 41.0063833, 'lon': 29.0750894, 'tags': {'bus': 'yes', 'highway': 'bus_stop', 'name': 'Baraj Yolu Sokak', 'public_transport': 'platform'}}, {'type': 'node', 'id': 7138862590, 'lat': 41.006325, 'lon': 29.0752541, 'tags': {'bus': 'yes', 'highway': 'bus_stop', 'name': 'Baraj Yolu Sokak', 'public_transport': 'platform'}}]}, 'version': 0.6, 'ways': []}


temelSorgu = pd.DataFrame(columns =
                          ["temelSorguId", "cacheTimestamp", "cacheVersion", "queryString", "other"])
alan = pd.DataFrame(columns =
                    ["alanId", "temelSorguId", "id", "areaId", "typeIdShort", "type", "typeId"])
adres = pd.DataFrame(columns =
                     ["adresId", "alanId", "address", "displayName", "isReverse", "wkt"])
node = pd.DataFrame(columns =
                    ["nodeId", "alanId", "countNodes", "generator", "nodes", "version",
                     "valid", "copyright"])
"""


