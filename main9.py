
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
import re
import random
from shapely.geometry import Point, Polygon

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

# fonksiyon: geometriCizdir
# Dataframe icinde verilen tum geometriler (nokta veya polygon), arka zemin
# ustune cizdirilir.
# @arkazemin, matplotlib.pyplot.plot: Arka harita
# @dataFrame, pd.DataFrame: Cizdirilmek istenen geometrilerin oldugu dataframe
# @geometriKolonu, str: Dataframe icinde hangi kolonun geometri oldugunu soyluyor
# @renk, str: Cizdirilme rengi
# @doygunluk, float: 0 ile 1 arasinda, ilgili cizimlerin o renkte ne kadar doygun olacagini gosterir
# @filtre, str: Veri kumesini daraltalim mi?
# @return, plot: Olusturulan harita
# @tamamlandi
def geometriCizdir(
        arkazemin: matplotlib.pyplot.plot,
        dataFrame: pd.DataFrame,
        geometriKolonu: str = 'geom',
        renk: str = 'red',
        doygunluk: float = 0.5,
        filtre: str = ""
    ):
    assert arkazemin != None
    assert len(dataFrame) > 0
    assert doygunluk > 0.0 and doygunluk <= 1.0
    assert renk in ayarlar.renkler
    # Dataframe in ilk satirini alalim !, sonrasinda geometri kolonu degeri eger bir "METIN" ise
    if type(dataFrame.iloc[0][geometriKolonu]) is str:
        # Dataframe icindeki "POINT" veya "POLYGON" ifadesini, PARSE edelim
        dataFrame[geometriKolonu] = dataFrame[geometriKolonu].apply(lambda value: shapely.wkt.loads(value))
    # Filtrele
    if len(filtre) > 0:
        dataFrame = dataFrame.query( filtre )
    # Bir geo pandas dataframe i olusturalim
    geop = gpd.GeoDataFrame(dataFrame, geometry= geometriKolonu )
    # Istenilen renkte ve arkazemin ustune ilgili geometrileri cizdirelim
    return geop.plot(ax = arkazemin, color=renk, alpha=doygunluk, edgecolor='black')

# fonksiyon: duzelt
# Girilen tapucinsaciklama sini duzeltir
# @metin, str: Girilecek olan tapucinsaciklama
# @return, str: Temizlenmis hali
# @tamamlandi
def duzelt(metin: str) -> str:
    # Her ne olursa olsun metne cevir
    # NOT: Bazen, bir metinsel kolonda 3 5 gibi ifadeler olabilir, bunlar ootmatik olarak "float" olarak algilanir
    # Bu nedenle, metin temizleme islemlerinde mutlaka str fonksiyonuna almak gerekir
    metin = str(metin)
    # Icindeki Turkce karakterleri cevir, (ingilizceye)
    for t in ayarlar.Turkce_Karakter: metin = metin.replace( t, ayarlar.Turkce_Karakter[t] )
    # Kucuk harflere cevir
    metin = metin.lower()
    # Bas ve sondaki bosluklari temizle
    metin = metin.strip()
    # Tire
    metin = re.sub(r"\s+", " ", metin)
    metin = re.sub(r"\-+", "-", metin)
    metin = metin.replace(" -", "-")
    metin = metin.replace("- ", "-")
    # Duzenlemeler
    if metin in ayarlar.Duzeltmeler:
        metin = ayarlar.Duzeltmeler[metin]
    # Dondurme islemi
    return metin

# fonksiyon: kesisenBul
# Kesisen alanlari bulur
# @cizimler, pd.DataFrame: Cizimlerin (polygon) oldugu dataframe
# @esik_degeri, float: Hangi esigin ustundeyse listele...
# @return, list: Liste olarak, kesisen ve kesisim alanlari esik degeri ustunde olan yerler
# @tamamlandi
def kesisenBul( cizimler: pd.DataFrame, esik_degeri: float = 0.0001 ) -> list:
    # Bir donus degiskeni atamasi yap
    sonuclar = []
    # Her bir ikili icin
    for i in range(len(cizimler)):
        # Ilk satiri oku
        rowi = cizimler.iloc[i]['geom']
        for j in range(len(cizimler)):
            # N x N === PERMUTASYON
            # (N 2) = N . (N-1) / 2 === KOMBINASYON
            if i > j:
                # Ikinci satiri oku
                rowj = cizimler.iloc[j]['geom']

                # Komsu olanlar, yan yana olanlar, sinirlari birbirine degenler dahi "INTERSECTS" olur
                # Iki tane birbirinden uzak ve degmeyen polygon, "INTERSECTS" olmaz!
                # Eger intersects ediyorsa
                if Polygon.intersects( rowi, rowj ):  #! ST_Intersects
                    # Kesisim bolgesini al(! NOT: bu da bir polygon olur)
                    intersection = Polygon.intersection( rowi, rowj ) # ! ST_Intersection
                    # Eger kesisen bir alan var ise!!
                    if intersection.area > esik_degeri:
                        # sonuc listesine ekle
                        sonuclar.append(  (i, j, intersection.area ) )
                        print( i, j, intersection.area )
    return sonuclar







"""
On calisma
tum_isimler = cizimler['tapucinsaciklama'].unique()
tum_isimler_temizlenmis = [duzelt(i) for i in tum_isimler]
tum_isimler_temizlenmis = sorted(tum_isimler_temizlenmis)
print(len(tum_isimler_temizlenmis))
print(len(list(set(tum_isimler_temizlenmis))))
"""

#! arkazemin = haritaYukle('İlçe', filtre = "(adm1_tr == 'ANKARA')")
arkazemin = haritaYukle('İlçe', filtre = "(adm2_tr == 'ÇANKAYA')")
cizimler = pd.read_csv("/home/mina5/PycharmProjects/ornekveriTkgm.csv", encoding='Windows-1254')
cizimler['tapucinsaciklama'] = cizimler['tapucinsaciklama'].apply(lambda value: duzelt(value))

# geometriCizdir( arkazemin, cizimler, filtre = "(mahallead == 'ÖVEÇLER')" )

bastan5tane = list(cizimler['tapucinsaciklama'].value_counts().to_dict().keys())[0:5]

"""
for b in bastan5tane:
    geometriCizdir( arkazemin, cizimler,
                    filtre = "(tapucinsaciklama == '" + b + "')",
                    renk = random.choice(ayarlar.renkler) )
    
"""
# plt.show()

# Kesisen alanlari bul !
# print(kesisenBul(cizimler))
print(cizimler)
"""
geom = cizimler.iloc[0]['geom']
print("Merkez", geom.centroid, type(geom.centroid)) # ST_Centroid
print("Alan", geom.area, type(geom.area)) # ST_Area

nokta = geom.centroid
print( geom.contains(nokta) ) #! ST_Contains


for i in range( len( cizimler )):
    geom = cizimler.iloc[i]['geom']
    nokta = geom.centroid
    if not geom.contains(nokta):
        print("Merkez, kendi icinde degil!", nokta, geom, i)
"""

cizimler['geom'] = cizimler['geom'].apply(lambda value: shapely.wkt.loads(value))
cizimler['duzgun'] = cizimler.apply( lambda row: row['geom'].contains( row['geom'].centroid ), axis=1 )


geometriCizdir( arkazemin, cizimler[ cizimler['duzgun'] == False ] )
plt.show()
