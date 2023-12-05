from openpyxl import load_workbook
from routes import get_route, take_routes
from datetime import datetime, timedelta, date
from times import calculate_times, get_eta


today = date.today()
filename = today.strftime('%d.%m.%Y')
routes = take_routes()

with open('departure_times.txt') as f:
    times = f.readline().strip()
departure_times = times.split(' ') #list of all etds for each route in routings.txt


wb = load_workbook('log.xlsx')
sheet = wb['FF']

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
        sheet['I'+row].value = f'{eta.hour}:{eta.minute}'

        ground_time = timedelta(minutes=10)
        departure_time = eta + ground_time

        i+=1
        sheet['H'+str(i)].value = f'{departure_time.hour}:{departure_time.minute}'
        r+=1

    sheet['H'+str(i)].value = ''
    i+=1
    t+=1


wb.save(f'FLIGHT FOLLOWING LOG {filename}.xlsx')