import dht
import machine
import time
import tsl2561
import ujson
import os
import gc

_power_adc = machine.Pin(14, machine.Pin.OUT)
_adc = machine.ADC(0)
_power_dht = machine.Pin(13, machine.Pin.OUT)
_dht = dht.DHT22(machine.Pin(12))
_power_tsl = machine.Pin(2, machine.Pin.OUT)
_power_tsl.value(1)
_scl = machine.Pin(5)
_sda = machine.Pin(4)
_i2c = machine.I2C(scl=_scl, sda=_sda)
_light_sensor = tsl2561.TSL2561(_i2c, address=0x39)
_config_file = "sensor_config.json"
history_sensor_data_file = "sensor_data_log.json"

# all power off
_power_adc.value(0)
_power_dht.value(1)
_power_tsl.value(0)


def _trim_sensor_data(total_lines, keep_lines):
    os.rename(history_sensor_data_file, "temp.json")
    file_ptr = open("temp.json", "r")
    for _ in range(0, total_lines-keep_lines):
        file_ptr.readline()
        gc.collect()
    new_file_ptr = open(history_sensor_data_file, "a")
    while True:
        read = file_ptr.readline()
        if read == "":
            break
        else:
            new_file_ptr.write(read)
        gc.collect()

    new_file_ptr.close()
    file_ptr.close()
    os.remove("temp.json")


def _save_sensor_data(sensor_data):
    string_to_write = ujson.dumps(sensor_data)+"\n"
    file_ptr = open(history_sensor_data_file, "a")
    file_ptr.write(ujson.dumps(sensor_data)+"\n")
    end_byte = file_ptr.tell()
    file_ptr.close()
    assumed_total_lines = int(end_byte) // len(string_to_write)
    if assumed_total_lines > 1200:
        _trim_sensor_data(assumed_total_lines, 1000)


def configure_sensor():
    """
    saves max sensor values for configuration
    :return: dict
    """
    _power_adc.value(1)
    time.sleep(1)
    try:
        config = {"adc_max": _adc.read()}
    except:
        return {"adc_max": 1024}

    file_ptr = open(_config_file, "w")
    try:
        file_ptr.write(ujson.dumps(config))
    finally:
        file_ptr.close()
    _power_adc.value(0)
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
    _power_adc.value(1)
    _power_tsl.value(1)
    start_time = time.time()
    while time.time() <= start_time + 3:
        try:
            data.update(_get_soil_moisture())
            data.update(_get_light_measure())
            data.update(_get_temperature_and_humidity())
        except Exception as msg:
            print(msg)
    _power_adc.value(0)
    _power_tsl.value(0)
    if len(data) >= 5:
        _save_sensor_data(data)
    return data
