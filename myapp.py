
# Kutuphane yuklemeleri
from fastapi import FastAPI # Web servis olusturmak icin
import uvicorn # Web servisi calistirmak
from fastapi.responses import HTMLResponse # HTML donus yapabilmek icin
import shapely.wkt # Metinsel bir ifadeden nokta veya polygon parse etmek icin
import pandas as pd # Pandas dataframe islemleri icin
import geopandas as gpd # Geopandas i yuklemek icin
import matplotlib.pyplot as plt # Gorsel ciktilar saglamak icin
from fastapi import FastAPI, File, UploadFile # Dosya upload etmek icin

import psycopg2
conn = psycopg2.connect("dbname=emre user=postgres password=postgres")
cur = conn.cursor()

# Bir tane fast api nesnesi olustur
app = FastAPI()
from fastapi.staticfiles import StaticFiles
app.mount("/static", StaticFiles(directory="static"), name="static")

# Anasayfa
@app.get("/", response_class=HTMLResponse)
async def function_root():
    # Anasayfayi, "anasayfa.html" den yukle, goster
    return str(open("anasayfa.html", 'r', encoding='utf-8').read())

# Eger bir "metinsel" koordinat veya polygon girildiyse
@app.get("/text", response_class=HTMLResponse)
async def function_text(geostring, asmap = None, astable = None):
    # 3 gosterme secenegini oku
    asmap = True if asmap == 'on' else False
    astable = True if astable == 'on' else False
    # Gelen koordinat veya polygonu oku, cevir
    p = shapely.wkt.loads(geostring)

    # Sonucu bir tablo olarak gormek istiyorsak
    if astable:
        df = pd.DataFrame(columns = ['geom'])
        df.loc[len(df)] = [ p ]
        return df.to_html()

    # Sonucu bir harita olarak gormek istiyorsak
    if asmap:
        path = "/home/mina5/Downloads/geopandas(2)/geopandas/temel ornekler/Turkey_shapefile/turkey_administrativelevels0_1_2/"
        tr = gpd.read_file(path + 'tur_polbnda_adm1.shp')
        df = pd.DataFrame(columns=['geom'])
        df.loc[len(df)] = [p]
        geop = gpd.GeoDataFrame(df, geometry='geom')
        geop.plot(ax = tr.boundary.plot(), color='red')
        plt.savefig('static/images/ resim.png', dpi=300)
        return "<img src='static/images/resim.png'>"
    return 'bos'


# Eger bir "dosya" girildiyse
@app.post("/file", response_class=HTMLResponse)
async def function_file(file: UploadFile, fileasmap = None, fileastable = None, fileasgraphic = None):

    # 3 gosterme secenegini oku
    fileasmap = True if fileasmap == 'on' else False
    fileastable = True if fileastable == 'on' else False
    fileasgraphic = True if fileasgraphic == 'on' else False

    import shutil
    from pathlib import Path
    from tempfile import NamedTemporaryFile
    from typing import Callable

    try:
        suffix = Path(file.filename).suffix
        with NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            shutil.copyfileobj(file.file, tmp)
            tmp_path = Path(tmp.name)
    finally:
        file.file.close()

    df = pd.read_csv(tmp_path, sep=';')

    fileasmap = True
    if fileastable:
        return df.to_html()
    if fileasmap:
        path = "/home/mina5/Downloads/geopandas(2)/geopandas/temel ornekler/Turkey_shapefile/turkey_administrativelevels0_1_2/"
        tr = gpd.read_file(path + 'tur_polbnda_adm1.shp')

        df['coordinates'] = df['coordinates'].apply(lambda value: shapely.wkt.loads(value))

        geop = gpd.GeoDataFrame(df, geometry='coordinates')
        geop.plot(ax = tr.boundary.plot(), color='red')
        plt.savefig('static/images/resim2.png', dpi=300)
        return "<img src='static/images/resim2.png'>"


    return 'bos'

# Eger bir "metinsel" koordinat veya polygon girildiyse
@app.get("/sql", response_class=HTMLResponse)
async def function_sql(sqlstatement: str, asmap = None, astable = None):
    # 3 gosterme secenegini oku
    asmap = True if asmap == 'on' else False
    astable = True if astable == 'on' else False
    # Gelen koordinat veya polygonu oku, cevir

    cur.execute(sqlstatement)
    sonuclar = cur.fetchall()
    for s in sonuclar:
        print(s)

    return ''

    # Sonucu bir tablo olarak gormek istiyorsak
    if astable:
        df = pd.DataFrame(columns = ['geom'])
        df.loc[len(df)] = [ p ]
        return df.to_html()

    # Sonucu bir harita olarak gormek istiyorsak
    if asmap:
        path = "/home/mina5/Downloads/geopandas(2)/geopandas/temel ornekler/Turkey_shapefile/turkey_administrativelevels0_1_2/"
        tr = gpd.read_file(path + 'tur_polbnda_adm1.shp')
        df = pd.DataFrame(columns=['geom'])
        df.loc[len(df)] = [p]
        geop = gpd.GeoDataFrame(df, geometry='geom')
        geop.plot(ax = tr.boundary.plot(), color='red')
        plt.savefig('static/images/ resim.png', dpi=300)
        return "<img src='static/images/resim.png'>"
    return 'bos'



uvicorn.run(app, host="0.0.0.0", port=5000)


# dpi save higher resolution
# image display static path html
