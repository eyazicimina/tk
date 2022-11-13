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


# uvicorn.run(app, host="0.0.0.0", port=8000)
import random
for _ in range(100):
    id = random.randint(1, 100000)
    alan = random.random() * 1000
    no = random.randint(1, 100)
    ilid = random.randint(1, 81)
    print(f"INSERT INTO parsel(id, alan, no, ilid) VALUES ({id}, {alan}, {no}, {ilid});")

a = "selam\nnaber"
a = """selam
naber"""


import psycopg2
conn = psycopg2.connect("dbname=emre user=postgres password=123")
cur = conn.cursor()
cur.execute("""
SELECT * 
FROM cd.bookings 
LIMIT 3
""")
sonuclar = cur.fetchall()
for s in sonuclar:
    print(s)

cur.execute("""
SELECT * 
FROM cd.members 
LIMIT 3
""")
sonuclar = cur.fetchall()
for s in sonuclar:
    print(s)






cur.execute("""
SELECT * 
FROM cd.bookings 
LIMIT 3
""")
sonuclar = cur.fetchall()

#: Kaç tane sonuç geldi
print(len(sonuclar))

#: Cursor ile birlikte gelen kolonların ismi nedir?
print(type(cur.description), cur.description)


def getir( sorgu: str, dataFrameeCevir: bool = False ) -> dict:
    cur.execute(sorgu)
    sonuclar = cur.fetchall()
    columns = [c[0] for c in cur.description]
    return {"sonuçlar": sonuclar, "kolonlar": columns, "adet": len(sonuclar)}

r1 = getir("SELECT * FROM cd.bookings LIMIT 10;")
r2 = getir("SELECT * FROM cd.facilities LIMIT 10;")
r3 = getir("SELECT * FROM cd.members LIMIT 10;")
print(r1)
print(r2["kolonlar"])
print(r3["adet"])

print(r1["sonuçlar"][0])

print(r1["sonuçlar"][0][2])




s = 'POINT(120 100)'
print(s)
s = s.replace("POINT(", "").replace(")", "")
print(s)
s = s.split(" ")
print(s)
s = [float(i) for i in s]
print(s)
s = tuple(s)
print(s)

print(getir("SELECT name, geom FROM geometries LIMIT 1;")["sonuçlar"])



import random
def noktaÜret() -> str:
    b = 26 + random.random() * 19 # 26 ile 45 arası
    e = 36 + random.random() * 6  # 36 ile 42
    return f"POINT({b} {e})"



for _ in range(1000):
    r = noktaÜret()
    cur.execute(f"INSERT INTO geometries VALUES ('Point', '{r}');")


def doğrultuÜret() -> str:
    def koordinatÜret() -> str:
        b = 26 + random.random() * 19  # 26 ile 45 arası
        e = 36 + random.random() * 6  # 36 ile 42
        return f"{b} {e}"

    k1 = koordinatÜret()
    k2 = koordinatÜret()
    k3 = koordinatÜret()
    k4 = koordinatÜret()
    return f"LINESTRING({k1}, {k2}, {k3}, {k4})"


for _ in range(random.randint(100, 1000)):
    r = doğrultuÜret()
    cur.execute(f"INSERT INTO geometries VALUES ('LineString', '{r}');")




def çokgenÜret() -> str:
    def koordinatÜret() -> str:
        b = 26 + random.random() * 19  # 26 ile 45 arası
        e = 36 + random.random() * 6  # 36 ile 42
        return f"{b} {e}"

    poly = []
    for _ in range(random.randint(3, 20)):
        poly.append( koordinatÜret() )

    poly.append(poly[0])
    return "POLYGON((" + ",".join(poly) + "))"



for _ in range(random.randint(500, 2000)):
    p = çokgenÜret()
    s = f"INSERT INTO geometries VALUES ('Polygon', '{p}');"
    cur.execute(s)
## INSERT INTO geometries VALUES ('Polygon', 'POLYGON((0 0, 1 0, 1 1, 0 1, 0 0))');


conn.commit()
