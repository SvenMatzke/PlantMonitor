import dht
import machine
import time
import tsl2561
import ujson
import os

_adc = machine.ADC(0)
_dht = dht.DHT22(machine.Pin(2))
_scl = machine.Pin(5)
_sda = machine.Pin(4)
_i2c = machine.I2C(scl=_scl, sda=_sda)
_light_sensor = tsl2561.TSL2561(_i2c, address=0x39)
_config_file = "sensor_config.json"


def configure_sensor():
    """
    saves max sensor values for configuration
    :return: dict
    """
    try:
        config = {"adc_max": _adc.read()}
    except:
        return {"adc_max": 1024}

    file_ptr = open(_config_file, "w")
    try:
        file_ptr.write(ujson.dumps(config))
    finally:
        file_ptr.close()
    return config


def _load_configuration():
    if _config_file in os.listdir():
        file_ptr = open(_config_file, "r")
        try:
            read_file =file_ptr.read()
            print(read_file)
            loaded_config = ujson.loads(read_file)
        except ValueError:
            os.remove(_config_file)
            loaded_config = {"abc_max": 1024}
        finally:
            file_ptr.close()
    else:
        loaded_config = configure_sensor()
    return loaded_config


_loaded_config = _load_configuration()


def _get_soil_moisture():
    """
    :return: returns the soil_moisture in percentage
    :rtype: tuple(key, int)
    """
    adc_max = _loaded_config.get("adc_max", 1024)
    adc_read = _adc.read()*100
    return (("soil moisture", 100 - adc_read//adc_max),)


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
