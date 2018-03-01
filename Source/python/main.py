import gc

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

# get config data
print("Starting main routine")
loaded_settings = settings.get_settings()
# if anything fails we are ready to set up
restful_online_time = loaded_settings.get('awake_time_for_config', 300)
keep_alive_time = restful_online_time

if wlan.sta_if.isconnected():
    # update time
    ntptime.settime()

    # wenn connected try to get new config if this fails we set restful_online_time
    # => this will result in more energy consumption, but else you can config this device
    request_url = loaded_settings.get("request_url", None)
    if request_url is not None:
        try:
            # send plant_monitor data
            sensor_data = sensor.sensor_data()
            sensor_data.update(loaded_settings.get('added_infos_to_sensor_data', {}))
            response = urequests.post(
                request_url,
                json=sensor_data
            )

            if int(response.status_code) >= 300:
                raise ConnectionError("Response was incorrect")

            keep_alive_time = loaded_settings.get('keep_alive_time_s')
            restful_online_time = loaded_settings.get('max_awake_time_s')
        except Exception as e:
            # data was not send so we will need some config changes
            restful_online_time = loaded_settings.get('awake_time_for_config', 300)

if machine.reset_cause() == machine.HARD_RESET:
    print("Hard reset its config time")
    restful_online_time = 300  # config time will be hard set
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
    # TODO
    return


def _sensor_configure(writer, request):
    global last_request_time
    last_request_time = time.time()
    configuration_data = sensor.configure_sensor()
    return userv.json(writer, configuration_data)


def _get_settings(writer, request):
    global last_request_time
    last_request_time = time.time()
    return userv.json(writer, settings.get_settings())


def _post_settings(writer, request):
    global last_request_time
    last_request_time = time.time()
    try:
        new_settings = ujson.loads(request.get('body'))
    except:
        return userv.json(writer, {"message": "Request had no valid json body."}, status=406)
    updated_settings = settings.save_settings(settings.get_settings(), new_settings)
    return userv.json(writer, updated_settings)


# routes
plant_app.add_route("/", _index, method='GET')
plant_app.add_route("/app.bundle.js", _static_js, method='GET')
plant_app.add_route("/styles.bundle.css", _static_css, method='GET')
plant_app.add_route("/rest/data", _get_data, method='GET')
plant_app.add_route("/rest/configure", _get_data, method='POST')
plant_app.add_route("/rest/settings", _get_settings, method='GET')
plant_app.add_route("/rest/settings", _post_settings, method='POST')

# run server
plant_app.run_server(
    timeout_callback=shutdown_reached
)

import deepsleep

deepsleep.set_awake_time_and_put_to_deepsleep(
    loaded_settings.get("deepsleep_s", 100)
)
