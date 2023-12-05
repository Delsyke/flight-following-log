from openpyxl import load_workbook
from routes import get_route, take_routes
from datetime import datetime, timedelta, date
from times import calculate_times, get_eta
##from validators import aircraft_validator


today = date.today()
filename = today.strftime('%d.%m.%Y')
routes = take_routes()

with open('departure_times.txt') as f:
    times = f.readline().strip()
departure_times = times.split(' ') #list of all etds for each route in routings.txt



wb = load_workbook('log.xlsx')
sheet = wb['FF']
sheet2 = wb['CONFIG']

i = 5 #start row
t = 0 #start index of departure_times
##a = 0



for stops in routes:
    r=0
    legs = get_route(stops)
    departure_time = departure_times[t]
    sheet['H'+str(i)].value = departure_time

    for _ in range(len(legs)):
        row = str(i)
        dep, dest = legs[r][0], legs[r][1]
        eet = calculate_times(dep,dest)
        eta = get_eta(departure_time, eet)

        sheet['E'+row].value = dep
        sheet['F'+row].value = dest

        eta_hr_str = str(eta.hour)
        eta_min_str = str(eta.minute)

        if len(eta_hr_str) == 1:
            eta_hr_str = '0' + eta_hr_str
        if len(eta_min_str) == 1:
            eta_min_str = '0' + eta_min_str

        sheet['I'+row].value = f'{eta_hr_str}:{eta_min_str}'

        ground_time = timedelta(minutes=10)
        departure_time = eta + ground_time

        dep_time_hr_str = str(departure_time.hour)
        dep_time_min_str = str(departure_time.minute)

        if len(dep_time_hr_str) == 1:
            dep_time_hr_str = '0' + dep_time_hr_str
        if len(dep_time_min_str) == 1:
            dep_time_min_str = '0' + dep_time_min_str

        i+=1
        sheet['H'+str(i)].value = f'{dep_time_hr_str}:{dep_time_min_str}'
        r+=1

    sheet['H'+str(i)].value = ''
    i+=1
    t+=1


##aircraft_validator(sheet)

wb.save(f'FF LOG {filename}.xlsx')