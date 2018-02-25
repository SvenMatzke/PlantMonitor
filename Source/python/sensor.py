import dht
import machine
import time
import tsl2561

_adc = machine.ADC(0)
_dht = dht.DHT22(machine.Pin(2))
_scl = machine.Pin(5)
_sda = machine.Pin(4)
_i2c = machine.I2C(scl=_scl, sda=_sda)
_light_sensor = tsl2561.TSL2561(_i2c, address=0x39)


def _get_soil_moisture():
    """
    :return: returns the soil_moisture in percentage
    :rtype: tuple(key, int)
    """
    # max wert ist der höchste und geringste solle
    return (("soil moisture", _adc.read() / 1024),)


def _get_temperature_and_humidity():
    """
    :return: Returns temperature and humidity at the given pin
    :rtype: tuple[tuple]
    """
    _dht.measure()
    return ("temperature", _dht.temperature()), ("humidity", _dht.humidity())


def _get_light_measure():
    return (("light", _light_sensor.read()),)


def sensor_data():
    """
    :rtype: dict
    """
    data = dict(time=time.time())
    data.update(_get_soil_moisture())
    data.update(_get_temperature_and_humidity())
    data.update(_get_light_measure())
    return data
