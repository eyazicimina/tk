
import uvicorn # Web servisi calistirmak
from fastapi.responses import HTMLResponse # HTML donus yapabilmek icin
import shapely.wkt # Metinsel bir ifadeden nokta veya polygon parse etmek icin
import pandas as pd # Pandas dataframe islemleri icin
import geopandas as gpd # Geopandas i yuklemek icin
import matplotlib.pyplot as plt # Gorsel ciktilar saglamak icin
from fastapi import FastAPI, File, UploadFile # Dosya upload etmek icin
import psycopg2 # Postgresql e baglanmak icin
from fastapi.staticfiles import StaticFiles # Statik dosyalar kullanmak icin (resim gibi)
import folium # Folium haritalarini kullanmak icin
import matplotlib
import ayarlar

# fonksiyon: haritaYukle
# Turkiye haritasini istenilen seviyede yukleyip bize istedigimiz filtereye gore dondurur
# @kademe, object: Hangi seviyede gormek istiyoruz
# @sinir, bool: Sinirlari mi gosterelim?
# @filtre, str: Veri kumesini daraltalim mi?
# @return, plot: Olusturulan harita
# @tamamlandi
# arkazemin = haritaYukle('İlçe', filtre = "(adm1_tr == 'ANKARA')")
def haritaYukle(kademe: object = 1, sinir: bool = True, filtre: str = "") -> matplotlib.pyplot.plot:
    # Kontrol: kademe degiskeni sadece bu 7 degerden birini alabilir.
    assert kademe in [0, 1, 2, 'Türkiye', 'İl', 'Şehir', 'İlçe']
    # Turkiye haritasini yukle
    tr = gpd.read_file(ayarlar.path + ayarlar.dosya_isimleri[kademe])
    if len(filtre) > 0:
        tr = tr.query( filtre )
        assert len(tr) > 0
    # Turkiye haritasini ciz
    # Eger Turkiye seviyesindeyse, Sinira bakmaksizin ciz!
    if kademe in [0, 'Türkiye']:
        return tr.plot()
    else:
        # Eger sadece sinirlari gormek istiyorsak,
        if sinir:
            return tr.boundary.plot()
        else:
            # Eger icleri dolu olarak gormek istiyorsak
            return tr.plot()

# haritaYukle('İl', sinir = False, filtre = "adm1_tr == 'ANKARA'")
arkazemin = haritaYukle('İlçe', filtre = "(adm1_tr == 'ANKARA')") # WHERE .....

plt.show()

