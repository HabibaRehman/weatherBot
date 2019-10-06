import json
import os
import requests

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    print(json.dumps(req, indent=4))
    
    res = processRequest(req)
    
    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def makeResponse(req):
    if req.get("queryResult").get("action") != "fetchWeatherForecast":
        return {}
    result = req.get("queryResult")
    parameters = result.get("parameters")
    city = parameters.get("city")
    if city is None:
        return None
    r=requests.get('https://samples.openweathermap.org/data/2.5/weather?q='+city+'&appid=b6907d289e10d714a6e88b30761fae22')
    json_object = r.json()
    weather=r.get("weather")
    main=weather.get("main")
    description=weather.get("main")
    speech = "The forecast for"+city+ "for "+date+" is "+main+" with "+description
    return {
    "fulfillmentText": speach,
    "source": "example.com",
    }

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print("Starting app on port %d" % port)
    app.run(debug=False, port=port, host='0.0.0.0')
