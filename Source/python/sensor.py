import dht
import machine
import time
import tsl2561


def _get_soil_moisture(pin_id):
    """
    :return: returns the soil_moisture in percentage
    :rtype: tuple(key, int)
    """
    adc = machine.ADC(pin_id)
    # max wert ist der höchste und geringste solle
    return (("soil moisture", adc.read() / 1024),)


def _get_temperature_and_humidity(pin_id):
    """
    :return: Returns temperature and humidity at the given pin
    :rtype: tuple[tuple]
    """
    d = dht.DHT22(machine.Pin(pin_id))
    d.measure()
    return ("temperature", d.temperature()), ("humidity", d.humidity())


def _get_light_measure(scl_pin, sda_pin, address=0x39):
    scl = machine.Pin(scl_pin)
    sda = machine.Pin(sda_pin)
    i2c = machine.I2C(scl=scl, sda=sda)
    light_sensor = tsl2561.TSL2561(i2c, address=address)
    return (("light", light_sensor.read()),)


def sensor_data():
    """
    :rtype: dict
    """
    data = dict(time=time.time())
    data.update(_get_soil_moisture(0))
    data.update(_get_temperature_and_humidity(2))
    data.update(_get_light_measure(5, 4))
    return data
