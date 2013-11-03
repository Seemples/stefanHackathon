import requests
import json
from random import randint


def a():
    city="Budapest"

    events=requests.get('http://api.event.ly/v3/venues/search.json?city='+city+'&api_key=8145e1ce63396b62')


    events=events.json()
    i=0
    b=[]
    venues=[]
    while i<3:
        try:
            artist=randint(0,len(events))
            b=events[artist]['name']
            i+=1
            venues+=[b]
        except:
            return []
    return venues

    
print a()
