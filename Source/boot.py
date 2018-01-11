"""
http://docs.micropython.org/en/latest/esp8266/esp8266/tutorial/network_basics.html
http://docs.micropython.org/en/latest/esp8266/esp8266/tutorial/powerctrl.html

#uploading files
https://learn.adafruit.com/micropython-basics-load-files-and-run-code/boot-scripts
"""
# pip install pico web as dependency oder nur uaio
import machine
import network
import time
import hashlib


def set_and_put_to_deepsleep(time_in_s):
    """
    Puts your device to deepsleep for a given time.
    Hardware note:
    connect gpio16 to reset to be able to deep sleep

    :param time_in_s: time to be in deepsleep
    """
    # configure RTC.ALARM0 to be able to wake the device
    rtc = machine.RTC()
    rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEPSLEEP)

    # set RTC.ALARM0 to fire after 10 seconds (waking the device)
    rtc.alarm(rtc.ALARM0, time_in_s * 1000)

    # put the device to sleep
    machine.deepsleep()


# after wake up to determine sleep mode
# if machine.reset_cause() == machine.DEEPSLEEP_RESET:
#     print('woke from a deep sleep')
# else:
#     print('power on or hard reset')


def connect_to_existing_network(essid, password):
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(essid, password)
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())
    return sta_if


def create_an_network():
    """

    :return: connected WLAN class
    """
    ap_if = network.WLAN(network.AP_IF)
    # TODO not sure if this will work with password
    ident_hash = hashlib.sha1(time.time())
    essid = "plant(%s)" % ident_hash
    password = "plantdata"
    ap_if.config(essid=essid, password=password, authmode=4)
    print('essid: %s, pw: %s' % (essid, password))
    print('network config:', ap_if.ifconfig())
    return ap_if



# thats to open listening
# but in doing so we cant lookup data anymore
# TODO going async
html = """<!DOCTYPE html>
<html>
    <head> <title>ESP8266 Pins</title> </head>
    <body> <h1>ESP8266 Pins</h1>
        <table border="1"> <tr><th>Pin</th><th>Value</th></tr> %s </table>
    </body>
</html>
"""

import socket

addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

s = socket.socket()
s.bind(addr)
s.listen(1)

print('listening on', addr)

while True:
    cl, addr = s.accept()
    print('client connected from', addr)
    cl_file = cl.makefile('rwb', 0)
    while True:
        line = cl_file.readline()
        if not line or line == b'\r\n':
            break
    rows = ['<tr><td>%s</td><td>%d</td></tr>' % (str(p), p.value()) for p in pins]
    response = html % '\n'.join(rows)
    cl.send(response)
    cl.close()

'''
http://docs.micropython.org/en/latest/esp8266/library/index.html
'''

'''
http://docs.micropython.org/en/latest/esp8266/reference/speed_python.html
'''
