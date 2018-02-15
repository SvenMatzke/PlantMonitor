Frontend of Plantmonitor is static website with backend communication to the esp

Intention will be a webpacked javascript framework delivering everything we need even without internet.

we have 4 mb flash drive but there is also micropython and your python source on it.
this results in your webpacked static files should be less then 3 mb.
"""

Booting will just decide which wlan connection we will choose

http://docs.micropython.org/en/latest/esp8266/esp8266/tutorial/network_basics.html
http://docs.micropython.org/en/latest/esp8266/esp8266/tutorial/powerctrl.html

"""

Puts your device to deepsleep for a given time.
Hardware note:
connect gpio16 to reset to be able to deep sleep

"""
This will be the only file which may need to be customised
http://docs.micropython.org/en/latest/esp8266/esp8266/tutorial/dht.html
https://github.com/adafruit/micropython-adafruit-tsl2561/blob/master/docs/tsl2561.rst

"""