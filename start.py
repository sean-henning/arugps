# app.py

from flask import Flask, jsonify, request, send_from_directory
import json
import geocoder
import socket 
import requests

app = Flask(__name__)

KEY = ""

@app.route('/receive', methods=['POST'])
def json_example():
    global KEY
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

    band = req_data['band']
    bssid = req_data['bssid']
    channel = req_data['channel']
    frequency = req_data['frequency']
    rates = req_data['rates']
    rssi = req_data['rssi']
    security = req_data['security']
    ssid = req_data['ssid']
    timestamp = req_data['timestamp']
    vendor = req_data['vendor']
    width = req_data['width']

    with open('scans.json', mode='w') as f:
        saveable_scan = [{"apscan_data": [{"band": band, "bssid": bssid, "channel": channel, "frequency": frequency, "rates": rates, "rssi":  rssi, "security": security, "ssid": ssid, "timestamp": timestamp, "vendor": vendor, "width": width}]}]
        f.write(json.dumps(saveable_scan))

    '''a google api alternative utilising the new HTML5 geolocation feature, not ideal if device has no ip :)'''
    # def send_location():
    #     try: 
    #         host_name = socket.gethostname()
    #         host_ip = socket.gethostbyname(host_name) 
    #         myloc = geocoder.ip(host_ip)
    #         acc = "html accurate"
    #         dvloc = {"location": {"lat": myloc.lat, "lng": myloc.lng },"accuracy" : acc }
    #         return(dvloc)
    #     except: 
    #         print("Unable to get Hostname and/or IP")

    url = "https://www.googleapis.com/geolocation/v1/geolocate"

    querystring = {"key":"AIzaSyAn5aF2aAGpTOZh3ZZT86vcfa-PSUIoxoI"}
    #payload = request_body
    payload = "{\n    \"wifiAccessPoints\": [\n        {\n            \"channel\": \""+channel+"\",\n            \"macAddress\": \""+bssid+"\"\n        }\n    ]\n}"
    headers = {
        'Content-Type': "application/json",
        'cache-control': "no-cache"
        }

    response = requests.request("POST", url, data=payload, headers=headers, params=querystring)

    return response.text, 201

if __name__ == '__main__':
    app.run(debug=True, port=5000)  
