
GENEL_SRID = 4326

class Adres:
    Sehir = None
    Ilce = None
    Sokak = None
    Cadde = None
    Mahalle = None
    No = None

    def __str__(self):
        return self.Cadde + " caddesi " + self.Sokak + " Sokagi " + \
            self.Mahalle + " Mah., No=" + str(self.No) + ", " + \
               self.Ilce + "/" + self.Sehir

    # Cumhuriyet caddesi Cesme Sokagi Avdanlik Mah., No=3, Polatli/Ankara

def mutlak(sayi):
    if sayi < 0: return -sayi
    return sayi


class Nokta:
    enlem = None
    boylam = None
    srid = GENEL_SRID

    def __str__(self):
        return str(self.enlem) + ", " + str(self.boylam) + ": " + str(self.srid)

