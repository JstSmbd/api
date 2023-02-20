import requests
import sys
from io import BytesIO
from PIL import Image, UnidentifiedImageError
from functions import request_point, lonlat_distance, find_middle_line

coords = [request_point("Санкт-Петербург, Петергоф"), [30.044691, 59.912339],
          [30.265166, 59.917148], [30.275479, 59.929408], [30.282346, 59.932818],
          request_point("Санкт-Петербург, Эрмитажная пристань"), [30.308389, 59.946044],
          [30.285011, 59.949008], [30.264646, 59.956940], [30.196755, 59.966286],
          request_point("Санкт-Петербург, Петергоф")]

if len(coords) > 1:
    distances = []
    for i, coord in enumerate(coords[:-1]):
        distances.append(lonlat_distance(coord, coords[i + 1]))
    i, procent = find_middle_line(sum(distances) / 2, distances)
    point1, point2 = coords[i], coords[i + 1]
    answers = f"{point1[0] - (point1[0] - point2[0]) * procent}," \
              f"{point1[1] - (point1[1] - point2[1]) * procent}"
elif len(coords) == 1:
    answers = f"{coords[0][0]},{coords[0][1]}"
    distances = [0]
else:
    print(f"Длина: 0m")
    sys.exit()

response = requests.get("http://static-maps.yandex.ru/1.x/", params={
    "l": "map",
    "pl": ",".join([f"{coord[0]},{coord[1]}" for coord in coords]) if len(coords) > 1 else "",
    "pt": f"{answers},pm2rdm"
})

print(f"Длина: {sum(distances)}m")

Image.open(BytesIO(response.content)).show()
