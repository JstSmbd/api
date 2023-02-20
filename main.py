import requests
import sys
import argparse
from functions import request_point, lonlat_distance, find_middle_line


try:
    parser = argparse.ArgumentParser()
    parser.add_argument("place", nargs="*", type=str)
    args = parser.parse_args()
    l = lonlat_distance(request_point(", ".join(args.place)),
                        request_point("Москва, Останкинская телебашня")) / 1000
    print(f"{(l / 3.6 - 525 ** 0.5) ** 2}m")
except (KeyError, IndexError) as ex:
    print("Неправильные аргументы")