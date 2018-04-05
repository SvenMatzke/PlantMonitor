import gc
import wlan
import os
import error

_batch_file = "batch_file.json"

loaded_settings = {}

try:
    gc.collect()

    buf = bytearray(2048)

    import time
    import urequests
    import userv
    import sensor
    import settings
    import ujson
    import machine
    import deepsleep
    import server

    # get config data
    print("Starting main routine")
    loaded_settings = settings.get_settings()

    # normal awake time
    keep_alive_time = loaded_settings.get('keep_alive_time_s')
    restful_online_time = loaded_settings.get('max_awake_time_s')

    request_url = loaded_settings.get("request_url", None)
    if wlan.sta_if.isconnected() and request_url is not None:

        _batch_file_ptr = open(_batch_file, "r")
        try:
            batches = ujson.loads(_batch_file_ptr.read())
            for batch in batches:
                # send plant_monitor data
                response = urequests.post(
                    request_url,
                    json=batch
                )

                if int(response.status_code) >= 300:
                    error.add_error(
                        ujson.dumps({'time': time.time(), 'status': response.status_code, 'body': response.body})
                    )

        except Exception as e:
            error.add_error(ujson.dumps({'time': time.time(), 'error': "Sending batches: " + str(e)}))
        finally:
            _batch_file_ptr.close()
            os.remove(_batch_file)

    # Only start server if there is a network
    if wlan.sta_if.isconnected() or wlan.ap_if.isconnected():
        if machine.reset_cause() == machine.HARD_RESET:
            print("Hard reset its config time")
            restful_online_time = loaded_settings.get('awake_time_for_config', 300)
            keep_alive_time = restful_online_time

        # power up esp while running the server
        machine.freq(160000000)
        server.run_server(buf, restful_online_time, keep_alive_time, loaded_settings)
except Exception as e:
    error.add_error(ujson.dumps({'time': time.time(), 'error': "main: " + str(e)}))
finally:
    gc.collect()
    machine.freq(80000000)
    wlan.ap_if.active(False)
    wlan.sta_if.active(False)

deepsleep.set_awake_time_and_put_to_deepsleep(
    loaded_settings.get("deepsleep_s", 100)
)
