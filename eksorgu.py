from OSMPythonTools.overpass import overpassQueryBuilder
query = overpassQueryBuilder(area=nyc, elementType='node', selector='"highway"="bus_stop"', out='body')
