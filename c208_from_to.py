from routes import get_route, take_routes
from datetime import datetime, timedelta, date
from times import get_c208_eet, get_eta


def c208_writer(c208_routes, c208_departure_times, worksheet, row_num):
    """
    Writer for all c208 routes
    """
    i = row_num #the row number. start with row 5
    t = 0 #time index

    #loop through each route
    for stops in c208_routes:
        r=0
        legs = get_route(stops)
        departure_time = c208_departure_times[t]
        worksheet['H'+str(i)].value = departure_time

        for _ in range(len(legs)):
            row = str(i)
            dep, dest = legs[r][0], legs[r][1]
            eet = get_c208_eet(dep,dest)
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

            ground_time = timedelta(minutes=15)
            departure_time = eta + ground_time

            dep_time_hr_str = str(departure_time.hour)
            dep_time_min_str = str(departure_time.minute)

            if len(dep_time_hr_str) == 1:
                dep_time_hr_str = '0' + dep_time_hr_str
            if len(dep_time_min_str) == 1:
                dep_time_min_str = '0' + dep_time_min_str

            i+=1
            worksheet['H'+str(i)].value = f'{dep_time_hr_str}:{dep_time_min_str}'
            r+=1

        worksheet['H'+str(i)].value = ''
        i+=1
        t+=1

    return i