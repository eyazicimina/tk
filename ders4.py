import uvicorn
from fastapi import FastAPI
app = FastAPI()

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
        return özellikÇıkar( sonuc, ["fromId", "tag", "toXML", "nodes", "timestamp"] )
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



from fastapi.responses import HTMLResponse

@app.get("/", response_class=HTMLResponse)
async def root():
    return "<form action='sorgula' method='get'><input type='text' name='sorgu' id='sorgu'></form>"
    #return sorgula(473223865)

@app.get("/sorgula")
async def xdsfgdsfgfsd(sorgu):
    if isNumeric(sorgu):
        return sorgula(int(sorgu))
    elif isCoordinate(sorgu):
        return sorgula(tuple([float(k) for k in sorgu.split(" ")]))
    else:
        return sorgula(sorgu)

import re
def isNumeric(metin: str) -> bool:
    return re.match("^[0-9]+$", metin)

def isCoordinate(metin: str) -> bool:
  return re.match("^[0-9\,\s\.]+$", metin)


uvicorn.run(app, host="0.0.0.0", port=8000)
