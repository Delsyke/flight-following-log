
def get_route(stops):
    i = 0
    route = stops.split(' ')
    legs = []

    for i in range(len(route)-1):
        leg = (route[i], route[i+1])
        legs.append(leg)

    return legs #list with tuples of all sectors for a given routing


def read_routes():
    schedule = list()
    j = 0

    with open('routings.txt') as f:
        lines = f.readlines()
        # print('lines is:', lines)

    for line in lines:
        if line:
            line = line.strip()
            if len(line) != 0 and line[2] == ':': 
                etd = line[0:5]
                route = line[6:]
                schedule.append((etd, route))
                
            elif len(line) != 0 and line[2] != ':':
                au_code = line[0:3]
                route = line[4:]
                schedule.append((au_code, route))

            else:
                j+=1
                schedule.append(('SKIP THIS LINE'+str(j),))   
                
    # print('schedule is :', schedule)
    return schedule # a list of tuples each containing either the etd/au_code (for c208 or dhc8 respectively) and the corresponding route


if __name__ == '__main__':
    read_routes()
