
import re
def isNumeric(metin: str) -> bool:
  return re.match("^[0-9]+$", metin)
