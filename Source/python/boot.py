# This file is executed on every boot (including wake-boot from deepsleep)
import gc
import error
import time
gc.collect()

_batch_file = "batch_file.json"

try:
    import wlan
    import settings
    import machine
    import ujson
    import ntptime
    import sensor
    import os

    print("deactivate wlan")
    wlan.ap_if.active(False)
    wlan.sta_if.active(False)

    print("Starting boot routine")
    loaded_settings = settings.get_settings()
    reads_without_send = loaded_settings.get("reads_without_send", 10)
    request_url = loaded_settings.get("request_url", None)

    # load batch data
    if _batch_file in os.listdir():
        _batch_file_ptr = open(_batch_file, "r")
        batches = ujson.loads(_batch_file_ptr.read())
        _batch_file_ptr.close()
    else:
        batches = list()

    # with every start we gather sensor data at least once
    sensor_data = sensor.sensor_data()
    sensor_data.update(loaded_settings.get('added_infos_to_sensor_data', {}))
    batches.append(sensor_data)

    # save batch data
    # and only save max reads batches
    _batch_file_ptr = open(_batch_file, "w")
    _batch_file_ptr.write(ujson.dumps(batches[-reads_without_send:]))
    _batch_file_ptr.close()

    # if we have enough batches and a request_url
    # hard reset starts webserver
    if (len(batches) >= reads_without_send and request_url is not None) or machine.reset_cause() == machine.HARD_RESET:

except Exception as e:
    print(e)
    error.add_error(ujson.dumps({'time': time.time(), 'error': "boot: " + str(e)}))
finally:
    gc.collect()
