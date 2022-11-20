
# Import etme islemleri
import matplotlib.colors as mcolors

# Turkce karakterlerin karsiliklari
Turkce_Karakter = {
    "Ş": "s", "Ü": "u", "Ç": "c", "Ğ": "g",
    "Ö": "o", "İ": "i", "I": "i", "ı": "i",
    "ğ": "g", "ç": "c", "ş": "s", "ö": "o",
    "ü": "u",
}

# Parsel tipleri duzenleme
Duzeltmeler = {
    'betonarme isyeri': 'isyeri beton',
    'is yeri-beton-': 'isyeri beton',
    'is yeri - beton': 'isyeri beton'
}

# Matplotlib in destekledigi tum renkleri yazdik liste olarak!
renkler = list({name for name in mcolors.CSS4_COLORS if f'xkcd:{name}' in mcolors.XKCD_COLORS})

# Path degiskenini ayarla
path = "/home/mina5/Downloads/geopandas(2)/geopandas/temel ornekler/Turkey_shapefile/turkey_administrativelevels0_1_2/"

# Dosya isimleri
dosya_isimleri = {
    0: 'tur_linebnda_adm0.shp',
    1: 'tur_polbnda_adm1.shp',
    2: 'tur_polbna_adm2.shp',
    'Türkiye': 'tur_linebnda_adm0.shp',
    'İl': 'tur_polbnda_adm1.shp',
    'Şehir': 'tur_polbnda_adm1.shp',
    'İlçe': 'tur_polbna_adm2.shp'
}
