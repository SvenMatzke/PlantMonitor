import dht
import machine
import time
import tsl2561
import ujson
import os
import gc
import error

_adc = None
_dht = None
_light_sensor = None
_power = machine.Pin(13, machine.Pin.OUT)
_power.value(1)


def power_on():
    _power.value(1)


def power_off():
    _power.value(0)


try:
    _adc = machine.ADC(0)
except Exception:
    error.add_error("ADC is not defined")

try:
    _dht = dht.DHT22(machine.Pin(12))
except Exception:
    error.add_error("Dht22 is not running.")

try:
    _scl = machine.Pin(14)
    _sda = machine.Pin(2)
    _i2c = machine.I2C(scl=_scl, sda=_sda)
except Exception:
    error.add_error("Lightsensor is not running.")

_config_file = "sensor_config.json"
history_sensor_data_file = "sensor_data_log.json"
power_off()


def configure_sensor():
    """
    saves max sensor values for configuration
    :return: dict
    """
    power_on()
    time.sleep(1)
    try:
        config = {"adc_max": _adc.read()}
    except:
        power_off()
        return {"adc_max": 1024}
    finally:
        power_off()

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
            read_file = file_ptr.read()
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
    if _adc is None:
        return (("soil moisture", -1),)

    adc_max = _loaded_config.get("adc_max", 1024)
    adc_read = _adc.read() * 100
    return (("soil moisture", 100 - adc_read // adc_max),)


def _get_temperature_and_humidity():
    """
    :return: Returns temperature and humidity at the given pin
    :rtype: tuple[tuple]
    """
    if _dht is None:
        return ("temperature", -100), ("humidity", -1)

    _dht.measure()
    return ("temperature", _dht.temperature()), ("humidity", _dht.humidity())


def _get_light_measure():
    _light_sensor = tsl2561.TSL2561(_i2c, address=0x39)
    return (("light", _light_sensor.read()),)

