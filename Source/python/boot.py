# This file is executed on every boot (including wake-boot from deepsleep)
import gc
gc.collect()
import wlan
import settings
import deepsleep
import requests
import tsl2561
import sensor
import settings
import userv


def setup_network():
    config_data = settings.get_settings()
    wlan_config = config_data.get('wlan', {})

    print("connect existing network")
    return wlan.connect_to_existing_network(
        essid=wlan_config.get('ssid'),
        password=wlan_config.get('password'),
    )


print("deactivate wlan")
wlan.ap_if.active(False)
wlan.sta_if.active(False)

if not setup_network():
    wlan.create_an_network()

gc.collect()
