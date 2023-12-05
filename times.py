import json
import datetime


def calculate_times(dep, dest):
    with open('timings.json') as f:
        timings = json.load(f)

    try:
        eet = timings["C208"][dep.upper()][dest.upper()]
    except KeyError:
        eet = timings["C208"][dest.upper()][dep.upper()]

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
##    return f'{eta.hour}:{eta.minute}'

