# This file is executed on every boot (including wake-boot from deepsleep)
import gc
gc.collect()
import wlan
import settings
import machine

print("deactivate wlan")
wlan.ap_if.active(False)
wlan.sta_if.active(False)

config_data = settings.get_settings()
wlan_config = config_data.get('wlan', {})
# On Hardreset we want to configure on a fresh network
if machine.reset_cause() != machine.HARD_RESET:
    print("connect existing network")
    network_connected = wlan.connect_to_existing_network(
        essid=wlan_config.get('ssid'),
        password=wlan_config.get('password'),
    )
    if not network_connected:
        wlan.create_an_network()
else:
    wlan.create_an_network()
