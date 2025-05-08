from flask import Flask, Response
import os
import time
import json

app = Flask(__name__)
SENSOR_ID = "28-0f6e0087ecae"

def read_temp(sensor_id):
    try:
        path = f'/sys/bus/w1/devices/{sensor_id}/w1_slave'
        with open(path, 'r') as f:
            lines = f.readlines()
        if lines[0].strip()[-3:] != 'YES': #indicates vlaid temp
            return None
        temp_data = lines[1].split('t=')[-1] #loaction of data in file
        celsius = float(temp_data) / 1000.0
        fahrenheit = celsius * 1.8 + 32
        return round(celsius, 2), round(fahrenheit, 2)
    except:
        return None

def event_stream():         #get data from sensor every 2 seconds 
    while True:
        temp = read_temp(SENSOR_ID)
        if temp:
            data = {
                'sensor_id': SENSOR_ID,
                'temperature_c': temp[0],
                'temperature_f': temp[1],
                'timestamp': time.strftime("%Y-%m-%d %H:%M:%S")
            }
            yield f"data: {json.dumps(data)}\n\n"
        time.sleep(2)

@app.route('/stream')
def stream():    #push temp 
    return Response(event_stream(), mimetype='text/event-stream')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
