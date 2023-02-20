import requests
import sys
import argparse
from functions import request_point, lonlat_distance, find_middle_line


try:
    parser = argparse.ArgumentParser()
    parser.add_argument("--school", nargs="*", type=str)
    parser.add_argument("--home", nargs="*", type=str)
    args = parser.parse_args()
    if not (args.school and args.home):
        raise SystemExit
    distance = lonlat_distance(request_point(", ".join(args.school)),
                               request_point(", ".join(args.home)))
except SystemExit:
    print("Нерпавильные аргументы")
except IndexError:
    print("Такого места нет")
else:
    print(f"Длина: {distance}m")
