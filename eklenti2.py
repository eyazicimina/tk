
def isCoordinate(metin: str) -> bool:
  return re.match("^[0-9\,\s\.]+$", metin)
