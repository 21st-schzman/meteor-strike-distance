import requests
import json
import haversine
from pprint import pprint
import math

# global distances_cato
# distances_cato = {}

def get_closest_meteor_strike(local_coordinates = [42.7051216,-71.4850696]):

    url = "https://data.nasa.gov/resource/y77d-th95.json"

    payload = ""
    headers = {
        'cache-control': "no-cache",
        'Postman-Token': "08b3092e-47d1-45fd-a24b-579d482f7dbe"
    }

    response = requests.request("GET", url, data=payload, headers=headers)

    ## DEBUG CODE ##
    # with open("text.txt", "wb") as out_file:
        # out_file.write(response.text.encode("utf-8"))
    # print(response.text.encode("utf-8"))
    ## END DEBUG Code

    strike_data = json.loads(response.text.encode("utf-8"))

    for i, item in enumerate(strike_data):
        if 'geolocation' in item:
            # print(item['geolocation']['coordinates'])
            distance = haversine.haversine(local_coordinates, item['geolocation']['coordinates'])
            strike_data[i]['distance'] = distance

    strike_data.sort(key=get_distance)
    no_distance_count = len([i for i in strike_data if 'distance' not in i])
    print("NO DISTANCE COUNT: {0}".format(no_distance_count))

    for i in range(no_distance_count):
        strike_data.pop()

    pprint(strike_data[0:15])
    print("=======================")
    pprint(strike_data[-1:-16:-1])

    return strike_data[-1]

def get_distance(strike):
    return strike.get('distance', math.inf)

strike_datum = get_closest_meteor_strike()

print("Shortest distance meteor strike from current location: {0} kilometers".format(strike_datum['distance']))
print("Strike Data:\n")
pprint(strike_datum)
