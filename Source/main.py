"""

#uploading files
https://learn.adafruit.com/micropython-basics-load-files-and-run-code/boot-scripts

"""
import wlan
import settings
from sensor.soil_moisture import get_soil_moisture
from sensor.temperature_humidity import get_temperature_and_humidity
import http
import json
import time
from deepsleep import set_and_put_to_deepsleep

# pip install pico web as dependency oder nur uaio
# from here we need a little async magic to listen to the outside world and still maintaining timeouts
# i want an async aio webinterface because
# do i want that it would be cool but naaa

# get config data

loaded_settings = settings.get_settings()

# TODO config modularised
def senor_data():
    """

    :rtype: dict
    """
    data = dict()
    # data.update(zip(*get_soil_moisture(0)))
    data.update(zip(*get_temperature_and_humidity(4)))

    return data

# 1 .
restful_online_time = 10  # TODO das müsste von config

if wlan.is_connected_to_network():
    # wenn connected try to get new config if this fails we set restful_online_time
    # => this will result in more energy consumption, but else you can config this device
    request_url = loaded_settings.get("request_url")
    try:
        new_config = json.loads(http.get(request_url))
        loaded_settings = settings.save_settings(
            old_config=loaded_settings,
            new_config=new_config
        )
        http.post(request_url, json.dumps(senor_data()))
    except:
        restful_online_time = 120 #TODO

print(senor_data()) #TODO cleanup

#  start restful config server for a given time

#TODO da brauch ich noch paar sachen
import socket
html = """<!DOCTYPE html>
<html>
    <head><title>ESP8266 Pins</title></head>
    <body>
        <h1>hello from esp</h1>
    </body>
</html>
"""

def start_webserver():
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

    s = socket.socket()
    s.bind(addr)
    s.listen(1)

    print('listening on', addr)
    start_time = time.time()
    while time.time()-(start_time+restful_online_time) >= 0:
        cl, addr = s.accept()
        print('client connected from', addr)
        cl_file = cl.makefile('rwb', 0)
        while True:
            line = cl_file.readline()
            if not line or line == b'\r\n':
                break
        response = html
        cl.send(response)
        cl.close()

'''
http://docs.micropython.org/en/latest/esp8266/library/index.html
'''

'''
http://docs.micropython.org/en/latest/esp8266/reference/speed_python.html
'''
# set_and_put_to_deepsleep(100) #TODO time from settings