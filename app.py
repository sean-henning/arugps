# app.py

from flask import Flask, jsonify, request
import json
import requests
import os
# import geocoder

'''a google api alternative utilising the new HTML5 geolocation feature, not ideal if device has no ip :)'''
# def device_location():
#     try:
#         host_name = socket.gethostname()
#         host_ip = socket.gethostbyname(host_name)
#         myloc = geocoder.ip(host_ip)
#         acc = "html accurate"
#         dvloc = {"location": {"lat": myloc.lat, "lng": myloc.lng },"accuracy" : acc }
#         return(dvloc)
#     except:
#         print("Unable to get Hostname and/or IP")


''' Function to request AP GPS details'''
def get_gps(bssid,channel):

    url = "https://www.googleapis.com/geolocation/v1/geolocate"

    querystring = {"key":""}
    payload = "{\n    \"wifiAccessPoints\": [\n        {\n            \"channel\": \""+channel+"\",\n            \"macAddress\": \""+bssid+"\"\n        }\n    ]\n}"
    headers = {
        'Content-Type': "application/json",
        'cache-control': "Private"
        }

    response = requests.request("POST", url, data=payload, headers=headers, params=querystring)

    return response.text

app = Flask(__name__) 

@app.route('/receive', methods=['POST'])
def reply_gps():
    req_data = request.get_json()
    if not req_data:
        response = {
            'message': 'No data attached.'
        }
        return jsonify(response), 400
    if 'bssid' not in req_data:
        response = {
            'message': 'No node data found.'
        }
        return jsonify(response), 400

    # band = req_data['band']
    bssid = req_data['bssid']
    channel = req_data['channel']
    # frequency = req_data['frequency']
    # rates = req_data['rates']
    rssi = req_data['rssi']
    # security = req_data['security']
    # ssid = req_data['ssid']
    # timestamp = req_data['timestamp']
    # vendor = req_data['vendor']
    # width = req_data['width']

    ''' primitive cached based on rssi (closer to 0 is stronger, further away is weaker)
        if the strength falls below -50 then goolge api will be called otherwise the cache will be used '''

    if os.path.isfile('./cache.txt') and rssi <= -50 :
        with open('cache.txt', mode='r') as data:
            cached = data.read()
            gpsco = cached[0:-1]
            data.close()
    else:
        gpsco = get_gps(bssid, channel)
        with open('cache.txt', mode='w') as data:
            data.write(gpsco)
            data.close()

    return gpsco, 201

if __name__ == '__main__':
    app.run(debug=False, port=5000)
