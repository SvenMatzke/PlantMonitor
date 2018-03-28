import gc
import os

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

    # webserver will be started to listen
    accumulated_time = 0
    start_time = time.time()
    last_request_time = time.time()


    def shutdown_reached():
        return (time.time() - start_time) < restful_online_time and (time.time() - last_request_time) <= keep_alive_time


    # declare pages
    plant_app = userv.App()


    def _index(writer, request):
        global last_request_time
        last_request_time = time.time()
        return userv.static_file(writer, "index.html", buf)


    def _static_js(writer, request):
        return userv.static_file(writer, "app.bundle.js", buf)


    def _static_css(writer, request):
        return userv.static_file(writer, "styles.bundle.css", buf)


    def _get_data(writer, request):
        global last_request_time
        last_request_time = time.time()
        sens_data = sensor.sensor_data()
        settings_data = settings.get_settings()
        sens_data.update(settings_data.get('added_infos_to_sensor_data', {}))
        return userv.json(writer, sens_data)


    def _history_data(writer, request):
        global last_request_time
        last_request_time = time.time()

        content_len = 0
        if sensor.history_sensor_data_file not in os.listdir():
            content_len = os.stat(sensor.history_sensor_data_file)[6]

        writer.write(
            userv._response_header(
                status=200,
                content_type="application/json",
                content_length=content_len + 2 - 1  # +2 braces -1 tailoring \n
            )
        )
        writer.write("[")
        if content_len > 0:
            file_ptr = open(sensor.history_sensor_data_file, "r")
            read = ""
            while True:
                if read != "":
                    writer.write(",")
                read = file_ptr.readline().replace("\n", "")
                writer.write(read)
                gc.collect()
                if read == "":
                    break
            file_ptr.close()

        writer.write("]")
        return


    def _sensor_configure(writer, request):
        global last_request_time
        last_request_time = time.time()
        configuration_data = sensor.configure_sensor()
        return userv.json(writer, configuration_data)


    def _send_deepsleep(writer, request):
        deepsleep.set_awake_time_and_put_to_deepsleep(
            loaded_settings.get("deepsleep_s", 100)
        )


    def _get_settings(writer, request):
        global last_request_time
        last_request_time = time.time()
        return userv.json(writer, settings.get_settings())


    def _post_settings(writer, request):
        global last_request_time
        last_request_time = time.time()
        try:
            new_settings = ujson.loads(request.get('body'))
        except Exception as e:
            error_file_ptr.write(ujson.dumps({'error': str(e)}) + "\n")
            return userv.json(writer, {"message": "Request had no valid json body."}, status=406)
        updated_settings = settings.save_settings(settings.get_settings(), new_settings)
        return userv.json(writer, updated_settings)


    # routes
    plant_app.add_route("/", _index, method='GET')
    plant_app.add_route("/app.bundle.js", _static_js, method='GET')
    plant_app.add_route("/styles.bundle.css", _static_css, method='GET')
    plant_app.add_route("/rest/data", _get_data, method='GET')
    plant_app.add_route("/rest/sensor_history", _history_data, method='GET')
    plant_app.add_route("/rest/configure", _sensor_configure, method='POST')
    plant_app.add_route("/rest/senddeepsleep", _send_deepsleep, method="POST")
    plant_app.add_route("/rest/settings", _get_settings, method='GET')
    plant_app.add_route("/rest/settings", _post_settings, method='POST')

    # run server
    plant_app.run_server(
        timeout_callback=shutdown_reached
    )
except Exception as e:
    error_file_ptr.write(ujson.dumps({'error': str(e)}) + "\n")
finally:
    error_file_ptr.close()
    gc.collect()

deepsleep.set_awake_time_and_put_to_deepsleep(
    loaded_settings.get("deepsleep_s", 100)
)
