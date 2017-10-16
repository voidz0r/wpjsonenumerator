#!/usr/bin/python3

import requests
import argparse
from colors import *
from tabulate import tabulate
import sys

parser = argparse.ArgumentParser(description="Enumerate wp-json API")
parser.add_argument("url", help="The URL to scan")
parser.add_argument("--dangerous-methods", help="Specify a comma-separated list of dangerous methods", default=("PUT", "DELETE", "PATCH", "POST"))
args = parser.parse_args()

url = args.url
dangerous_methods = args.dangerous_methods
    

if not url:
    parser.print_help()
    sys.exit(0)


if "/wp-json/" not in url:
    url += "/wp-json/"

try:
    response = requests.get(url).json()
except Exception as e:
    print("Something went wrong while trying to access to %s, maybe a JSON error" % (url))
    print(e)
    sys.exit(0)
routes = []

for route, value in response['routes'].items():
    methods = []
    for method in value.get("methods"):
        if method in dangerous_methods:
            methods.append(color(method, "red"))
        else:
            methods.append(color(method, "green"))
    routes.append([color(route, "yellow"), ", ".join(methods)])

routes = sorted(routes, key=lambda route: route[0])

print(tabulate(routes, headers=["URL", "Available Methods"]))
