from flask import Flask
import requests
import json
app = Flask(__name__)

@app.route('/')
def hello_world():
    print "sup"
    r = requests.get("http://partners.api.skyscanner.net/apiservices/browsequotes/v1.0/GB/GBP/en-GB/GLA/NRT/anytime?apiKey=hck01722056005870195080684980065")
    print "hello"
    return json.dumps(r.json(), separators=(',',':'), indent=4, sort_keys=True)

if __name__ == '__main__':
        app.run()
