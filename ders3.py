
#: Imports
import sys
from OSMPythonTools.api import Api
from OSMPythonTools.nominatim import Nominatim

nominatim = Nominatim()
api = Api()

def özellikÇıkar( nesne: object, hariç = [] ) -> dict: 
    çıktı = {}

    return çıktı

def sorgula( girdi, ekstra = 10 ):
    if type(girdi) is int:
        sonuc = api.query(f"way/{girdi}")
        return özellikÇıkar( sonuc )

    if type(girdi) is str:
        sonuc = nominatim.query(girdi, wkt=True)
        return özellikÇıkar( sonuc )

    if type(girdi) is tuple:
        sonuc = nominatim.query(girdi[0], girdi[1], reverse=True, zoom= ekstra)
        return özellikÇıkar( sonuc )

    raise Exception("Bilinmeyen format")
