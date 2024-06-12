import json
import datetime
import logging

logging.basicConfig(format='%(message)s')


def get_c208_eet(dep, dest):
    with open('main/timings.json') as f:
        timings = json.load(f)

    try:
        eet = timings["C208"][dep.upper()][dest.upper()]
        return eet
    except KeyError:
        try:
            eet = timings["C208"][dest.upper()][dep.upper()]
            return eet
        except KeyError:
            msg = f'''
            ATTENTION: 
            Unknown C208 route {dep.upper()} - {dest.upper()}. Schedule not completed. 
            Please correct or complete this section manually.
            '''
            logging.error(msg)

def get_dhc8_eet(dep, dest):
    with open('main/dhc8 timings.json') as f:
        timings = json.load(f)

    try:
        eet = timings["DHC8"][dep.upper()][dest.upper()]
        return eet
    except KeyError:
        try:
            eet = timings["DHC8"][dest.upper()][dep.upper()]
            return eet
        except KeyError:
            msg = f'''
            ATTENTION: 
            Unknown DHC8 route {dep.upper()} - {dest.upper()}. Schedule not completed. 
            Please correct complete this section manually.
            '''
            logging.error(msg)


def get_eta(departure_time, eet):
    hr, mnt = eet.split(':')
    trip_time = datetime.timedelta(hours=int(hr), minutes=int(mnt))

    if isinstance(departure_time, str):
        dep_time = datetime.datetime.strptime(departure_time, '%H:%M')
        eta = dep_time + trip_time
    elif isinstance(departure_time, datetime.datetime):
        eta = departure_time + trip_time

    return eta






if __name__ == '__main__':
    print(get_dhc8_eet('HKNW', 'Htkj'))
    print(get_c208_eet('HKNW', 'Htkj'))
    print(get_eta('10:10', get_dhc8_eet('HKNW', 'Htkj')))
    print(get_eta('10:10', get_c208_eet('HKNW', 'Htkj')))