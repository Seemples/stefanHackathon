import requests
import json

print "Requesting info about flights from GLA to NRT..."
r = requests.get("http://partners.api.skyscanner.net/apiservices/browsequotes/v1.0/GB/GBP/en-GB/GLA/NRT/anytime?apiKey=hck01722056005870195080684980065")
print "---"
print "Returned json!"
print
print r.json()
print
print "Can't see shit! Give me something which makes sense!"
print
print json.dumps(r.json(), separators=(',',':'), indent=4, sort_keys=True)
print
print "Ah thank god"
print
print "Can then use keywords to get shizzle from it, e.g. I want that info from the values from the places section"
print
print r.json()["Places"]
