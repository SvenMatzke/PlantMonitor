# This file is executed on every boot (including wake-boot from deepsleep)
import gc

gc.collect()

_error_log_file = "error.log"
_batch_file = "batch_file.json"

error_file_ptr = open(_error_log_file, "a")

try:
    import wlan
    import settings
    import machine
    import ujson
    import ntptime
    import sensor
    import os
    import time

    print("deactivate wlan")
    wlan.ap_if.active(False)
    wlan.sta_if.active(False)

    print("Starting main routine")
    loaded_settings = settings.get_settings()
    reads_without_send = loaded_settings.get("reads_without_send", 10)

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
    _batch_file_ptr = open(_batch_file, "w")
    _batch_file_ptr.write(ujson.dumps(batches))
    _batch_file_ptr.close()

    # if we have enough batches
    if len(batches) >= reads_without_send:
        wlan_config = loaded_settings.get('wlan', {})

        print("connect existing network")
        network_connected = wlan.connect_to_existing_network(
            essid=wlan_config.get('ssid'),
            password=wlan_config.get('password'),
        )
        # only create a network when its a hard reset and no network is connected
        if not network_connected and machine.reset_cause() == machine.HARD_RESET:
            wlan.create_an_network()

        # update time
        if wlan.sta_if.isconnected():
            ntptime.settime()
except Exception as e:
    error_file_ptr.write(ujson.dumps({'time': time.time(), 'error': "boot: " + str(e)}) + "\n")
finally:
    error_file_ptr.close()
    gc.collect()
