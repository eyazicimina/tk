
#: Imports
import sys
from OSMPythonTools.api import Api

#: Create the api
api = Api()
way = api.query('way/680549716')

#: Print the available tags
print( "TAGS", way.tags() )
print( "GEOM", way.geometry() )
print( "ARID", way.areaId() )
print( "TYID", way.typeId() )
print( "TIDS", way.typeIdShort() )
print( "TYPE", way.type() )
print( "ID  ", way.id() )
print( "LAT ", way.lat() )
print( "LON ", way.lon() )
print( "VISB", way.visible() )
print( "MEMS", way.members() )
print( "XML ", way.toXML() )
print( "CLON", way.centerLon() )
print( "CLAT", way.centerLat() )
print( "HIST", way.history())

for n in way.nodes():
    print( "NODE", n.tags(), n.lat(), n.lon() )

print("=========================================================")

from OSMPythonTools.nominatim import Nominatim
nominatim = Nominatim()
location = nominatim.query('Cumhuriyet, Üsküdar', wkt=True)
areaId = location.areaId()
displayName = location.displayName()
address = location.address()
type = location.type()
print("NAME", displayName)
print("ARID", areaId)
print("ADRS", address)
print("TYPE", type)
print("WKT ", location.wkt()) 

print("=========================================================")

from OSMPythonTools.nominatim import Nominatim
nominatim = Nominatim()
location = nominatim.query(49.4093582, 8.694724, reverse=True, zoom=10)
print("NAME", location.displayName())
print("ADRS", location.address())
print("JSON", location.toJSON())
