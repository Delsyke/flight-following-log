import json
import datetime


def get_c208_eet(dep, dest):
    with open('timings.json') as f:
        timings = json.load(f)

    try:
        eet = timings["C208"][dep.upper()][dest.upper()]
    except KeyError:
        eet = timings["C208"][dest.upper()][dep.upper()]
    
    return eet


def get_dhc8_eet(dep, dest):
    with open('dhc8 timings.json') as f:
        timings = json.load(f)

    try:
        eet = timings["DHC8"][dep.upper()][dest.upper()]
    except KeyError:
        eet = timings["DHC8"][dest.upper()][dep.upper()]
    
    return eet



def get_eta(departure_time, eet):
    hr, mnt = eet.split(':')
    trip_time = datetime.timedelta(hours=int(hr), minutes=int(mnt))

    if isinstance(departure_time, str):
        dep_time = datetime.datetime.strptime(departure_time, '%H:%M')
        eta = dep_time + trip_time
    elif isinstance(departure_time, datetime.datetime):
        eta = departure_time + trip_time

    return eta



# print(get_dhc8_eet('HKNW', 'Htkj'))
# print(get_c208_eet('HKNW', 'Htkj'))
# print(get_eta('10:10', get_dhc8_eet('HKNW', 'Htkj')))
# print(get_eta('10:10', get_c208_eet('HKNW', 'Htkj')))