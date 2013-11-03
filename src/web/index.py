import requests
import json
from flask import Flask, jsonify, request, render_template
import socket

app = Flask(__name__)
key = 'hck01722056005870195080684980065'

@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/gallery')
def gallery():
    return render_template('gallery.html')

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

    for Route in Routes:
        pid = Route['DestinationId']
        for Place in Places:
            if pid == Place['PlaceId']:
                Route['DestinationId'] = Place['Name']

    #print json.dumps(Routes, separators=(',',':'), indent=4, sort_keys=True)

    return json.dumps(Routes)
 
    #print json['Routes']

    #for Route in json['Routes']:
    #    if 'Price' in Route: print Route

app.debug = True

if __name__ == "__main__":
    app.run()
