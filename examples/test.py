import requests
import json

print "Requesting info about flights from GLA to NRT..."
r = requests.get("http://partners.api.skyscanner.net/apiservices/browsequotes/v1.0/GB/GBP/en-GB/GLA/NRT/2014-12-30?apiKey=prtl6749387986743898559646983194")
#r = requests.get("http://partners.api.skyscanner.net/apiservices/pricing/v1.0/69ce9038cc1e466c96f9e285474e2fe7_elhhpiln_3C0363B7FADA78837F0778C16D08B242?apikey=hck01722056005870195080684980065")
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
# print r.json()["Places"]

