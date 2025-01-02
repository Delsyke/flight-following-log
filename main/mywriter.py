from .routes import read_routes, get_route
from datetime import datetime, timedelta, date
from .times import get_c208_eet, get_eta, get_dhc8_eet
import json
import logging
from flask import abort


logging.basicConfig(format='%(message)s')

def write_to_excel(schedule, worksheet, row_num):
	"""
	Writes information to the excel file as per the required format
	schedule is the user input to be written to the excel
	worksheet is the specific worksheet in the excel we want to write
	row_num is the row within the worksheet from which we start to write the schedule
	"""
	
	#to read dhc8 routes and their scheduled timings for all services
	with open('main/dhc8 routings.json') as f: 
		dhc8_schedule = json.load(f)

	i = row_num
	t=0

	for flight in schedule:
		k = flight[0] 			#either au_code for the case of DHC8 of departure time for the case of C208
		route = flight[-1]		#the complete flight associated with k

		#C208 case
		if len(k) == 5:
			r=0 #index to locate legs later
			legs = get_route(route) #list of legs for the complete flight
			departure_time = k 		#departure time for the first leg
			worksheet['H'+str(i)].value = departure_time

			#workout the eta for the first landing
			#apply a 15 minute ground time and get new etd for next leg
			#write in the excel in appropriate cells
			for _ in range(len(legs)):
				row = str(i)
				dep, dest = legs[r][0], legs[r][1] #departure and destination stations
				eet = get_c208_eet(dep,dest) #how long to fly each leg
				
				try:
					eta = get_eta(departure_time, eet) #get eta 
				except:
					break

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
				departure_time = eta + ground_time #etd for next leg

				dep_time_hr_str = str(departure_time.hour)
				dep_time_min_str = str(departure_time.minute)

				if len(dep_time_hr_str) == 1:
					dep_time_hr_str = '0' + dep_time_hr_str
				if len(dep_time_min_str) == 1:
					dep_time_min_str = '0' + dep_time_min_str

				worksheet['H'+str(i+1)].value = f'{dep_time_hr_str}:{dep_time_min_str}'
				i+=1 #next row
				r+=1 #next leg

			# skip row to separate flights
			worksheet['H'+str(i)].value = '' 
                
			i+=1 #row for the next new flight
			t+=1 #not used for the c208 case but updated incase next aircraft is a dhc8


		#DHC8 case similar logic to c208 but
		#fixed schedule used as per flight codes rather than dynamic schedule
		elif len(k) == 3:
			r=0 #index to locate legs later
			t=0
			legs = get_route(route)
			try:
				departure_time = dhc8_schedule[k][route].split()[t]
			except KeyError:
				msg = f"""
				Oooops! Unknown DHC8 route {k} {route}. Schedule not completed. 
				Please correct or complete this section manually."""
				abort(400, msg)
				logging.error(msg)
				break
			worksheet['H'+str(i)].value = f'{departure_time}'


			for _ in range(len(legs)):
				row = str(i)
				dep, dest = legs[r][0], legs[r][1]
				eet = get_dhc8_eet(dep,dest)

				try:
					eta = get_eta(departure_time, eet)
				except:
					break

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
					departure_time = dhc8_schedule[k][route].split()[t+1]
				except IndexError:
					departure_time = dhc8_schedule[k][route].split()[t]

				worksheet['H'+str(i+1)].value = f'{departure_time}'

				t+=1
				i+=1
				r+=1

			worksheet['H'+str(i)].value = ''
			i+=1

		#Line skip to separate aircraft schedules
		else:
			i+=1
			# print('Line skip to separate aircraft schedules')
