from openpyxl import load_workbook
from datetime import date
from .routes import read_routes
from .mywriter import write_to_excel


today = date.today()
filename = today.strftime('%d.%m.%Y')
schedule = read_routes()

wb = load_workbook('main/log.xlsx')
sheet = wb['FF']

write_to_excel(schedule, sheet, 5)

wb.save(f'FF LOG {filename}.xlsx')