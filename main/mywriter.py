from .routes import read_routes, get_route
from datetime import datetime, timedelta, date
from .times import get_c208_eet, get_eta, get_dhc8_eet
import json
import logging



def write_to_excel(schedule, worksheet, row_num):

	with open('main/dhc8 routings.json') as f:
		dhc8_schedule = json.load(f)

	i = row_num
	t=0

	for flight in schedule:
		k = flight[0] 			#either au_code for the case of DHC8 of departure time for the case of C208
		route = flight[-1]		#the complete route associated with k

		#C208 case
		if len(k) == 5:
			r=0
			legs = get_route(route)
			departure_time = k
			worksheet['H'+str(i)].value = departure_time

			for _ in range(len(legs)):
				row = str(i)
				dep, dest = legs[r][0], legs[r][1]
				eet = get_c208_eet(dep,dest)
				
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


		#DHC8 case
		elif len(k) == 3:
			r=0
			t=0
			legs = get_route(route)
			try:
				departure_time = dhc8_schedule[k][route].split()[t]
			except KeyError:
				msg = f"""
				ATTENTION:
				Unknown DHC8 route {k} {route}. Schedule not completed. 
				Please correct or complete this section manually."""
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
