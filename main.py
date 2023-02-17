import requests
import sys
from io import BytesIO
from PIL import Image, UnidentifiedImageError
from functions import lonlat_distance

search_api_server = "https://search-maps.yandex.ru/v1/"
api_key = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"

try:
    address_ll = requests.get("http://geocode-maps.yandex.ru/1.x/", params={
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": " ".join(sys.argv[1:]),
        "format": "json"}).json()["response"][
        "GeoObjectCollection"]["featureMember"][0]["GeoObject"]["Point"]["pos"].replace(" ", ",")

    json_response = requests.get(search_api_server, params={
        "apikey": api_key,
        "text": "аптека",
        "lang": "ru_RU",
        "ll": address_ll,
        "type": "biz",
        "results": 10
    }).json()

    points = []
    color = ""
    for i, org in enumerate(json_response["features"], start=1):
        if "круглосуточно" in org["properties"]["CompanyMetaData"]["Hours"]["text"]:
            color = "gn"
        elif org["properties"]["CompanyMetaData"]["Hours"]["text"]:
            color = "bl"
        else:
            color = "gr"
        points.append(f'{",".join(map(str, org["geometry"]["coordinates"]))},pm2{color}m{i}')
    map_params = {
        "l": "map",
        "pt": "~".join(points)
    }

    map_api_server = "http://static-maps.yandex.ru/1.x/"
    response = requests.get(map_api_server, params=map_params)
    Image.open(BytesIO(response.content)).show()
except (IndexError, KeyError):
    print("bad parameters")
except UnidentifiedImageError:
    print("no pharmacies nearby")