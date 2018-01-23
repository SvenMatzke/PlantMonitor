"""

Booting will just decide which wlan connection we will choose

http://docs.micropython.org/en/latest/esp8266/esp8266/tutorial/network_basics.html
http://docs.micropython.org/en/latest/esp8266/esp8266/tutorial/powerctrl.html

"""
# This file is executed on every boot (including wake-boot from deepsleep)
import gc
import webrepl  #TODO webrepl rausnehmen wenn stable
import wlan
import settings
webrepl.start()
gc.collect()

wlan.ap_if.active(False)
wlan.sta_if.active(False)

config_data = settings.get_settings()
wlan_config = config_data.get('wlan')

network_adapter = wlan.connect_to_existing_network(
    essid=wlan_config.get('ssid'),
    password=wlan_config.get('password'),
)
if not network_adapter.is_connected():
    wlan.create_an_network()
