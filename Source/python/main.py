try:
    from grown import setup, run_grown
    import webrepl
    import machine

    grown = setup()
    webrepl.start()
    print("reset %s: " % machine.reset_cause())
    if machine.reset_cause() in [machine.HARD_RESET, machine.PWRON_RESET]:
        import upip

        upip.install('grown')
        machine.reset()

    from grown.light_control import add_light_control
    from grown.data_control import add_data_control
    from bh import BH1750
except ImportError:
    import network
    import ujson

    file_ptr = open("settings_store.json", "r")
    store = ujson.loads(file_ptr.read())
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect(store['wlan']['ssid'], store['wlan']['password'])
    import upip

    upip.install('grown')
    import machine

    machine.reset()

import requests
import ujson as json

import machine
import dht
import uasyncio as asyncio
import time


# light control
def _enable_light():
    current_state = json.loads(requests.get("http://192.168.2.106/report").content)
    relay_state = current_state.get('relay', True)
    if relay_state is False:
        requests.get('http://192.168.2.106/relay?state=1')


def _disable_light():
    current_state = json.loads(requests.get("http://192.168.2.106/report").content)
    relay_state = current_state.get('relay', True)
    if relay_state is True:
        requests.get('http://192.168.2.106/relay?state=0')


# sensor values
max_adc = 2350

pwr = machine.Pin(23, machine.Pin.OUT)
pwr2 = machine.Pin(18, machine.Pin.OUT)
i2c = machine.I2C(scl=machine.Pin(26), sda=machine.Pin(25))
adc = machine.ADC(machine.Pin(34))
adc.atten(machine.ADC.ATTN_11DB)
dht_sensor = dht.DHT22(machine.Pin(19))


def _convert_adc_to_precentage(adc_value):
    return adc_value * 100 / max_adc


async def get_sensor_data():
    values = {}
    print("Measure")
    try:
        pwr.on()
        pwr2.on()
        await asyncio.sleep(3)
        light = BH1750(i2c)
        dht_sensor.measure()
        await asyncio.sleep(1)
        values = {
            "moisture": _convert_adc_to_precentage(adc.read()),
            "lumen": light.luminance(0x20),
            "temperature": dht_sensor.temperature(),
            "humidity": dht_sensor.humidity()
        }
    except Exception as e:
        print("Failure in measure: %s " % str(e))
    finally:
        pwr.off()
        pwr2.off()
    return values


add_light_control(grown, _enable_light, _disable_light, lambda x: False)
add_data_control(grown, get_sensor_data)

run_grown()
