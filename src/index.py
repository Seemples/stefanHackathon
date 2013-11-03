import requests
import json
from flask import Flask, jsonify, request, render_template
import socket
from urllib2 import urlopen
import urllib2
from random import randint
import atw

def keyword(variable, page):
    matches = page.count(variable)
    if matches > 10:
        return True
    else:
        return False

city="Glasgow" #we need to be careful about the wiki url

app = Flask(__name__)
key = 'hck01722056005870195080684980065'

@app.route('/')
def hello():
    return render_template('index.html')


@app.route('/api/atw')
def whoho():
    c = request.args.get('c', '', type=str)
    budget = request.args.get('budget', 50, type=int)
    date = request.args.get('date', '2013-11-04', type=str)

    r = atw.start(c, budget, date, 2)
    #print json.dumps(r, separators=(',',':'), indent=4, sort_keys=True)

    print 'THIS IS A NASKO OUTPUT'
    print r

    return json.dumps(r)

@app.route('/api/venues')
def venues():
    city = request.args.get('city', '', type=str)
    city = city.replace(' ', '_')
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
            return 'error'
    return json.dumps(venues)

@app.route('/api/wiki')
def wiki():
    city = request.args.get('city', '', type=str)
    city = city.replace(' ', '_')

    headers = {"User-Agent":"Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11"} # Bypasses the bot-block from the site
    req = urllib2.Request("http://en.wikipedia.org/wiki/" + city, headers=headers)
    page = urllib2.urlopen(req).read()   #reades the whole webpage including the html
    
    keywords = ['beach', 'mountain', 'island']
    matches = []
    for i in keywords:
        matches.append(keyword(i, page))

    return json.dumps(matches)

@app.route('/api/country')
def country():

    # Get the user input
    c = request.args.get('c', '', type=str)

    ######################
    #     API methods    #
    ######################

    # Get the API results
    url = 'http://partners.api.skyscanner.net/apiservices/autosuggest/v1.0'

    # Country
    url += '/'
    url += 'GB'

    # Curency
    url += '/'
    url += 'GBP'

    # Locale
    url += '/'
    url += 'en-GB'

    # Data to send
    url += '?apikey='
    url += key

    url += '&query='
    url += c

    #payload = {'apikey': key, 'query': 'BG'}

    headers = {'content-type': 'application/json'}
    r = requests.get(url, headers=headers)
    js = r.json()

    print json.dumps(js, separators=(',',':'), indent=4, sort_keys=True)

    # Return a JSON object with the API results
    return jsonify(result=js['Places'],c=c)

@app.route('/api/test')
def apitest():
    url = 'http://partners.api.skyscanner.net/apiservices/browseroutes/v1.0'

    # Country
    url += '/'
    url += 'GB'

    # Currency
    url += '/'
    url += 'GBP'

    # Locale
    url += '/'
    url += 'en-GB'

    # Origin
    url += '/'
    url += 'GLA'

    # Destination
    url += '/'
    url += 'anywhere'

    # Outbound date
    url += '/'
    url += '2013-11'

    # Inbound date
    url += '/'
    url += '2013-11'

    # Key
    url += '?apiKey='
    url += key

    # Headers
    headers = {'content-type': 'application/json'}
    r = requests.get(url, headers = headers)

    js = r.json()

    print json.dumps(js, separators=(',',':'), indent=4, sort_keys=True)

    Routes = js['Routes']
    Places = js['Places']

    i = 0
    d = []

    for Route in Routes:
        pid = Route['DestinationId']
        for Place in Places:
            if pid == Place['PlaceId']:
                Route['DestinationId'] = Place['Name']
                if i < 10:
                    d.append(Route)
                    i += 1

    #print json.dumps(Routes, separators=(',',':'), indent=4, sort_keys=True)

    return json.dumps(d)
 
    #print json['Routes']

    #for Route in json['Routes']:
    #    if 'Price' in Route: print Route

app.debug = True

if __name__ == "__main__":
    app.run()
