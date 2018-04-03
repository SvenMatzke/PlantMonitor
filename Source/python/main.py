import gc

_error_log_file = "error.log"

error_file_ptr = open(_error_log_file, "a")

loaded_settings = {}

try:
    gc.collect()

    buf = bytearray(2048)

    import time
    import urequests
    import wlan
    import userv
    import sensor
    import settings
    import ujson
    import machine
    import ntptime
    import deepsleep
    import server

    # get config data
    print("Starting main routine")
    loaded_settings = settings.get_settings()

    # normal awake time
    keep_alive_time = loaded_settings.get('keep_alive_time_s')
    restful_online_time = loaded_settings.get('max_awake_time_s')

    # update time
    if wlan.sta_if.isconnected():
        ntptime.settime()

    # with every start we gather sensor data at least once
    sensor_data = sensor.sensor_data()
    sensor_data.update(loaded_settings.get('added_infos_to_sensor_data', {}))

    if wlan.sta_if.isconnected():
        request_url = loaded_settings.get("request_url", None)
        if request_url is not None:
            try:
                # send plant_monitor data
                response = urequests.post(
                    request_url,
                    json=sensor_data
                )

                if int(response.status_code) >= 300:
                    error_file_ptr.write(ujson.dumps({'status': response.status_code, 'body': response.body})+"\n")

            except Exception as e:
                error_file_ptr.write(ujson.dumps({'error': str(e)}) + "\n")

    if machine.reset_cause() == machine.HARD_RESET:
        print("Hard reset its config time")
        restful_online_time = loaded_settings.get('awake_time_for_config', 300)
        keep_alive_time = restful_online_time

    server.run_server(buf, restful_online_time, keep_alive_time, loaded_settings, error_file_ptr)
except Exception as e:
    error_file_ptr.write(ujson.dumps({'error': str(e)}) + "\n")
finally:
    error_file_ptr.close()
    gc.collect()

deepsleep.set_awake_time_and_put_to_deepsleep(
    loaded_settings.get("deepsleep_s", 100)
)
