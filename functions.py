import math
import requests
from random import uniform


def find_bbox(toponym):
    lw = toponym["boundedBy"]["Envelope"]["lowerCorner"]
    up = toponym["boundedBy"]["Envelope"]["upperCorner"]
    return f"{lw.replace(' ', ',')}~{up.replace(' ', ',')}"


def request_point(find):
    answer = requests.get("http://geocode-maps.yandex.ru/1.x/", params={
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": find,
        "format": "json"
    }).json()["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
    return list(map(float, answer["Point"]["pos"].split()))


def find_middle_line(metres, distances, i=0):
    if metres - distances[i] <= 0:
        return i, metres / distances[i]
    else:
        return find_middle_line(metres - distances[i], distances, i + 1)


def lonlat_distance(a, b):

    degree_to_meters_factor = 111 * 1000
    a_lon, a_lat = a
    b_lon, b_lat = b

    radians_lattitude = math.radians((a_lat + b_lat) / 2.)
    lat_lon_factor = math.cos(radians_lattitude)

    dx = abs(a_lon - b_lon) * degree_to_meters_factor * lat_lon_factor
    dy = abs(a_lat - b_lat) * degree_to_meters_factor

    distance = math.sqrt(dx * dx + dy * dy)

    return distance


def get_coords(geocode, bbox=False):
    answer = requests.get("http://geocode-maps.yandex.ru/1.x/", params={
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": geocode,
        "format": "json"}).json()["response"][
        "GeoObjectCollection"]["featureMember"][0]["GeoObject"]
    return find_bbox(answer) if bbox else answer["Point"]["pos"].replace(" ", ",")


def get_map(params):
    return requests.get("http://static-maps.yandex.ru/1.x/", params=params)


def get_bbox_part(bbox, type):
    list_bbox = [list(map(float, (list_bbox := bbox.split("~"))[0].split(","))),
                 list(map(float, list_bbox[1].split(",")))]
    sizes = [abs(list_bbox[0][0] - list_bbox[1][0]), abs(list_bbox[0][1] - list_bbox[1][1])]
    if type == "map":
        pr = uniform(0.005 / sizes[0], 0.032 / sizes[0])
    else:
        pr = uniform(0.005 / sizes[0], 1)
    next_sizes = [size * pr for size in sizes]
    lw_corner = [list_bbox[0][0] + uniform(0, sizes[0] - next_sizes[0]),
                 list_bbox[0][1] + uniform(0, sizes[1] - next_sizes[1])]
    return f"{lw_corner[0]},{lw_corner[1]}~" \
           f"{lw_corner[0] + next_sizes[0]}," \
           f"{lw_corner[1] + next_sizes[1]}"
