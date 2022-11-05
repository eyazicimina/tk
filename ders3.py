#: Imports
import sys
from OSMPythonTools.overpass import overpassQueryBuilder
from OSMPythonTools.api import Api
from OSMPythonTools.nominatim import Nominatim
from OSMPythonTools.overpass import Overpass

overpass = Overpass()
nominatim = Nominatim()
api = Api()

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


print( sorgula(473223865) )
print( sorgula("Cumhuriyet, Üsküdar") )
print( sorgula(( 49.4093582, 8.694724 )) )
print( sorgula(( "Cumhuriyet, Üsküdar", '"highway"="bus_stop"' )) )


