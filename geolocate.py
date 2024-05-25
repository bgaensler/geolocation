#!/usr/local/bin/python3.7

# Code to automatically geolocate user and update WWW page
# Written by BMG, 18jun2019

file = 'HTML file to post to'
phrase1 = 'text preceding geotag'
phrase2 = 'text following geotag'
url = 'API URL and token that provides longitude and latitude'

import requests
#import reverse_geocode
import reverse_geocoder as rg
import fileinput
import pycountry

DictInvert = lambda d: dict(zip(d.values(), d.keys()))

us_states = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NA': 'National',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
}

ca_prov = {
    'AB': 'Alberta',
    'BC': 'British Columbia',
    'MB': 'Manitoba',
    'NB': 'New Brunswick',
    'NL': 'Newfoundland and Labrador',
    'NT': 'Northwest Territories',
    'NS': 'Nova Scotia',
    'NU': 'Nunavut',
    'ON': 'Ontario',
    'PE': 'Prince Edward Island',
    'QC': 'Quebec',
    'SK': 'Saskatchewan',
    'YT': 'Yukon'
}

au_states = {
        'NSW': 'New South Wales',
        'QLD': 'Queensland',
        'WA': 'Western Australia',
        'ACT': 'Australian Capital Territory',
        'SA': 'South Australia',
        'NT': 'Northern Territory',
        'TAS': 'Tasmania',
        'VIC': 'Victoria'
}

us_states = DictInvert(us_states)
ca_prov = DictInvert(ca_prov)
au_states = DictInvert(au_states)
states = {**us_states, **ca_prov, **au_states}

try:
    u = requests.get(url)
    lat = u.json()['Data'][0]["Latitude"]
    long = u.json()['Data'][0]["Longitude"]

    coordinates = (lat,long),
#    city = reverse_geocode.search(coordinates)[0]["city"]
    geo = rg.search(coordinates)[0]
    city = geo['name']
    if (city == 'East York' or city == 'Etobicoke' or city == 'Scarborough'):
        city = 'Toronto'
    if (city == 'Pasatiempo'):
        city = 'Santa Cruz'
    if (city == 'Cuauhtemoc'):
        city = 'Mexico City'

    state = geo['admin1']
    try:
        state_abbrev = ' '+states[state]
    except:
        try:
           state_abbrev = ' '+pycountry.subdivisions.lookup(state).code[3:]
        except:
           state_abbrev = ''
#   Strip any numbers out of the state_abbrev
    state_abbrev = ''.join([i for i in state_abbrev if not i.isdigit()])
#   If state_abbrev is only whitespace, then strip it
    if (state_abbrev.isspace()):
        state_abbrev=''
#   Replace '-shi' at the end of Japanese cities
    city = city.replace('-shi',' City')

    country = pycountry.countries.get(alpha_2=geo['cc']).name
    if (country == 'Korea, Republic of'):
        country = 'South Korea'
#    country = reverse_geocode.search(coordinates)[0]["country"]
    loc = city+state_abbrev+', '+country+phrase2
    print(city+state_abbrev+', '+country)

    with fileinput.FileInput(file,inplace=True,backup='.bak') as file:
        for line in file:
            if phrase1 in line:
                head, sep, tail = line.partition(phrase1)
                print(head+sep+loc)
            else:
                print(line,end='')
except:
    pass
