import requests
import sys
from io import BytesIO
from PIL import Image, UnidentifiedImageError
from functions import lonlat_distance

try:
    address_ll = requests.get("http://geocode-maps.yandex.ru/1.x/", params={
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": " ".join(sys.argv[1:]),
        "format": "json"}).json()["response"][
        "GeoObjectCollection"]["featureMember"][0]["GeoObject"]["Point"]["pos"].replace(" ", ",")

    response = requests.get("http://geocode-maps.yandex.ru/1.x/", params={
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "kind": "district",
        "geocode": address_ll,
        "format": "json"
    }).json()["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"][
        "metaDataProperty"]["GeocoderMetaData"]["Address"]["Components"]

    district = " или ".join([kind["name"] for kind in response
                             if kind["kind"] == "district" and "район" in kind["name"].lower()])
    print(district if district else "нет района")
except (IndexError, KeyError):
    print("bad parameters")
