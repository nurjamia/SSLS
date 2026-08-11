
from urllib.parse import unquote
class UrlReplace:
    def __init__(self):
        UrlText = "https://docs.google.com/viewer?url=http%3A%2F%2Fwww.vldb.org%2Fpvldb%2Fvol6%2Fp913-papadopoulos.pdf"
        CleanUrlText = str(unquote(unquote(UrlText)))
        print(CleanUrlText.replace("https://docs.google.com/viewer?url=",""))
obj = UrlReplace()



