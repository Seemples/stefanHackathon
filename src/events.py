import requests
import json
from random import randint

city="London"

events=requests.get('http://api.event.ly/v3/venues/search.json?city='+city+'&api_key=8145e1ce63396b62')


events=events.json()
i=0
while i<3:
    artist=randint(0,99)
    print events[artist]['name']
    i+=1
