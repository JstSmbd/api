import requests
import sys
from io import BytesIO
from PIL import Image
from functions import lonlat_distance

search_api_server = "https://search-maps.yandex.ru/v1/"
api_key = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"

try:
    address_ll = requests.get("http://geocode-maps.yandex.ru/1.x/", params={
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": " ".join(sys.argv[1:]),
        "format": "json"}).json()["response"][
        "GeoObjectCollection"]["featureMember"][0]["GeoObject"]["Point"]["pos"].replace(" ", ",")

    search_params = {
        "apikey": api_key,
        "text": "аптека",
        "lang": "ru_RU",
        "ll": address_ll,
        "type": "biz"
    }

    response = requests.get(search_api_server, params=search_params)

    json_response = response.json()

    organization = json_response["features"][0]
    org_name = organization["properties"]["CompanyMetaData"]["name"]
    org_address = organization["properties"]["CompanyMetaData"]["address"]
    point = organization["geometry"]["coordinates"]
    org_point = "{0},{1}".format(point[0], point[1])
    org_distance = round(lonlat_distance(map(float, address_ll.split(',')),
                                         map(float, org_point.split(','))), 2)
    map_params = {
        "l": "map",
        "pt": "{0},pm2bm~{1},pm2am".format(org_point, address_ll)
    }

    map_api_server = "http://static-maps.yandex.ru/1.x/"
    response = requests.get(map_api_server, params=map_params)
    Image.open(BytesIO(response.content)).show()
    print(f"Название: {org_name}\n"
          f"Адрес: {org_address}\n"
          f"Время работы: {organization['properties']['CompanyMetaData']['Hours']['text']}\n"
          f"Расстояние: {org_distance}m")
except (KeyError, IndexError):
    print("bad parameters")