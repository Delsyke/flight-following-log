from openpyxl import load_workbook
from datetime import date
from routes import get_route, take_routes
from dhc8_from_to import dhc8_routing, dhc8_writer
from c208_from_to import c208_writer


today = date.today()
filename = today.strftime('%d.%m.%Y')
c208_routes = take_routes()


with open('departure_times.txt') as f:
    times = f.readline().strip()
c208_departure_times = times.split(' ')

with open('dhc8_times.txt') as f:
    au_routes = f.readlines()

wb = load_workbook('log.xlsx')
sheet = wb['FF']

au_routes = dhc8_routing(au_routes)

i = c208_writer(c208_routes, c208_departure_times, sheet, 5)
dhc8_writer(au_routes, sheet, row_num=i)


wb.save(f'FF LOG {filename}.xlsx')