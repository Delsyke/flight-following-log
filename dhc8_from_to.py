from routes import get_route, take_routes
from times import get_dhc8_eet, get_eta
import json


def dhc8_routing(au_routes):
    routing = {}
    for au_route in au_routes:
        au_code = au_route.strip().split('-')[0]
        route_stops = au_route.strip().split('-')[1]
        routing[au_code] = route_stops
    return routing


def dhc8_writer(routing, worksheet, row_num):
    """
    Writer for all dch8 routings
    """

    i = row_num
    with open('dhc8 routings.json') as f:
        dhc8_schedule = json.load(f)

    for k,v in routing.items():
        r=0
        t=0
        legs = get_route(v)
        departure_time = dhc8_schedule[k][v].split()[t]
        worksheet['H'+str(i)].value = f'{departure_time}'

        for _ in range(len(legs)):
            row = str(i)
            dep, dest = legs[r][0], legs[r][1]
            eet = get_dhc8_eet(dep,dest)
            eta = get_eta(departure_time, eet)

            worksheet['E'+row].value = dep
            worksheet['F'+row].value = dest

            eta_hr_str = str(eta.hour)
            eta_min_str = str(eta.minute)

            if len(eta_hr_str) == 1:
                eta_hr_str = '0' + eta_hr_str
            if len(eta_min_str) == 1:
                eta_min_str = '0' + eta_min_str

            worksheet['I'+row].value = f'{eta_hr_str}:{eta_min_str}'

            try:
                departure_time = dhc8_schedule[k][v].split()[t+1]
            except IndexError:
                departure_time = dhc8_schedule[k][v].split()[t]

            worksheet['H'+str(i+1)].value = f'{departure_time}'

            t+=1
            i+=1
            r+=1

        worksheet['H'+str(i)].value = ''
        i+=1

    return None

