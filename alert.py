import requests
import json


def listen_to_stream(url):
    with requests.get(url, stream=True) as response: #recieve data continuously 
        for line in response.iter_lines(): #reads the streamed response line-by-line
            if line:
                decoded = line.decode('utf-8') #convert to string
                if decoded.startswith("data:"):
                    json_data = decoded[6:]  # Remove "data: " only json string left
                    data = json.loads(json_data) 
                    temp_f = data.get('temperature_f')
                    if temp_f is not None:
                        print(f"🌡Temp: {temp_f}°F")
                        if temp_f > 212:
                            print("ALERT: Temperature exceeds boiling point!")

if __name__ == '__main__':
    raspberry_pi_ip = "http://172.20.10.2:5000/stream" #pi ip stream from serve 
    listen_to_stream(raspberry_pi_ip)  
