# Code to automatically geolocate phone and post to WWW page
# Written by BMG, 18jun2019

import requests
import reverse_geocode
import fileinput

file = 'HTML file to post to'
phrase1 = 'text preceding geotag'
phrase2 = 'text following geotag'
url = 'URL of API that provides longitude and latitude'

try:
    u = requests.get(url)
    lat = u.json()['Data'][0]["Latitude"]
    long = u.json()['Data'][0]["Longitude"]

    coordinates = (lat,long),
    city = reverse_geocode.search(coordinates)[0]["city"]
    country = reverse_geocode.search(coordinates)[0]["country"]
    loc = city+', '+country+phrase2

    with fileinput.FileInput(file,inplace=True,backup='.bak') as file:
        for line in file:
            if phrase1 in line:
                head, sep, tail = line.partition(phrase1)
                print(head+sep+loc)
            else:
                print(line,end='')
except:
    pass

