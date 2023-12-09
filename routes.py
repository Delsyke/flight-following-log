
def get_route(stops):
    i = 0
    route = stops.split(' ')
    legs = []

    for i in range(len(route)-1):
        leg = (route[i], route[i+1])
        legs.append(leg)

    return legs #list with tuples of all sectors for a given routing


def take_routes():
    c208_routes = []
    etd_times = []
    dhc8_routes = []

    with open('routings.txt') as f:
        lines = f.readlines()

    for line in lines:
        line = line.strip()

        if len(line) != 0 and line[2] == ':':
            try:
                etd = line[0:5]
                route = line[6:]
            except IndexError:
                pass
            finally:
                etd_times.append(etd)
                c208_routes.append(route)

        elif len(line) != 0 and line[2] != ':':
            try:
                au_code = line[0:3]
                route = line[4:]
            except IndexError:
                pass
            finally:
                dhc8_routes.append((au_code, route))


    with open('departure_times.txt', 'w') as f:
        for etd in etd_times:
            f.write(f' {etd}')

    with open('dhc8_times.txt', 'w') as f:
        for dhc8_route in dhc8_routes:
            f.write(f'{dhc8_route[0]}-{dhc8_route[1]}\n')

    return c208_routes #list of strings of all routes from routings.txt


# def take_dash_route():
#     routes = []
#     etd_times = []

#     with open('routings.txt') as f:
#         lines = f.readlines()

#     for line in lines:
#         line = line.strip()







# x = get_route('WIL LEW LSB WIL')
# print(x)

# y = take_routes()
# print(y[1])