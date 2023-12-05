
def get_route(stops):
    i = 0
    route = stops.split(' ')
    legs = []

    for i in range(len(route)-1):
        leg = (route[i], route[i+1])
        legs.append(leg)

    return legs #list with tuples of all sectors for a given routing

get_route('WIL OLX OSJ KTJ WIL')


def take_routes():
    routes = []
    etd_times = []

    with open('routings.txt') as f:
        lines = f.readlines()


    for line in lines:
        line = line.strip()
        etd = line[0:5]
        etd_times.append(etd)
        route = line[6:]
        routes.append(route)

    with open('departure_times.txt', 'w') as f:
        for etd in etd_times:
            f.write(f' {etd}')

    return (routes) #list of strings of all routes from routings.txt


##get_route()
##print(take_routes())