import os
from django.contrib.gis.geoip2 import GeoIP2
from django_countries import countries
from django_countries.fields import Country
from geoip2.errors import AddressNotFoundError

DATASETS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "datasets/geoip2")

def get_request_country(request, default=None):
    countries_dict = dict(countries)
    if default:
        if default in countries_dict:
            default = Country(code=default)
        else:
            raise ValueError("Invalid default country code")

    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")

    g = GeoIP2(path=DATASETS_DIR)
    try:
        country = g.country(ip)
        if country["country_code"] in countries_dict:
            return Country(code=country["country_code"])
        else:
            return default
    except AddressNotFoundError:
        return default
