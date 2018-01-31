"""
http://docs.micropython.org/en/latest/esp8266/esp8266/tutorial/dht.html
https://docs.micropython.org/en/latest/pyboard/library/pyb.I2C.html
https://github.com/adafruit/micropython-adafruit-tsl2561/blob/master/docs/tsl2561.rst
"""
import dht
import machine
import tsl2561


def get_soil_moisture(pin_id):
    """
    :return: returns the soil_moisture in percentage
    :rtype: tuple(key, int)
    """
    adc = machine.ADC(pin_id)
    return (("soil moisture", adc.read() / 1024),)


def get_temperature_and_humidity(pin_id):
    """
    :return: Returns temperature and humidity at the given pin
    :rtype: tuple[tuple]
    """
    d = dht.DHT22(machine.Pin(pin_id))
    d.measure()
    return ("temperature", d.temperature()), ("humidity", d.humidity())


def get_light_measure(scl_pin, sda_pin, address=0x39):
    scl = machine.Pin(scl_pin)
    sda = machine.Pin(sda_pin)
    i2c = machine.I2C(scl=scl, sda=sda)
    light_sensor = tsl2561.TSL2561(i2c, address=address)
    return (("light", light_sensor.read()),)
