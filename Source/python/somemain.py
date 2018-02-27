import gc
gc.collect()

buf = bytearray(2048)

import time
import urequests
import wlan
from Source.externalpackages import userv
import sensor
import settings
import ujson

# get config data
print(gc.mem_free())
loaded_settings = settings.get_settings()
# if anything fails we are ready to set up
restful_online_time = loaded_settings.get('awake_time_for_config', 300)
keep_alive_time = restful_online_time


# reset verhalten

# der teil ist 700 kb verlust
if wlan.sta_if.active():
    # wenn connected try to get new config if this fails we set restful_online_time
    # => this will result in more energy consumption, but else you can config this device
    request_url = loaded_settings.get("request_url", None)
    if request_url is not None:
        try:
            # get new settings  # TODO frage ob das drin bleibt
            parsed_reponse = urequests.get(request_url)
            if int(parsed_reponse.get('status_code', 500)) >= 300:
                raise ConnectionError("Response was incorrect")
            elif "application/json" not in parsed_reponse['header'].get('Content-Type', ""):
                raise ConnectionError("Mime type is not correct")
            new_config = parsed_reponse.get("body", None)
            if new_config is None or new_config == "":
                raise NotADirectoryError("New config didnt had the proper data")
            loaded_settings = settings.save_settings(
                old_config=loaded_settings,
                new_config=new_config
            )

            # send plant_monitor data
            sensor_data = sensor.sensor_data()
            sensor_data.update(loaded_settings.get('added_infos_to_sensor_data', {}))
            parsed_reponse = urequests.post(
                request_url,
                body=ujson.dumps(sensor_data)
            )
            if int(parsed_reponse.get('status_code', 500)) >= 300:
                raise ConnectionError("Response was incorrect")

            keep_alive_time = loaded_settings.get('keep_alive_time_s')
            restful_online_time = loaded_settings.get('max_awake_time_s')
        except Exception as e:
            # data was not send so we will need some config changes
            restful_online_time = loaded_settings.get('awake_time_for_config', 300)

# webserver will be started to listen
# Need to clean up some cache before its too low
print(gc.mem_free())

accumulated_time = 0
restful_online_time = 30
keep_alive_time = 10
start_time = time.time()

def shutdown_reached():
    return (time.time()-start_time) < 180
    # global accumulated_time
    # print("shutdown_active")
    # while accumulated_time < restful_online_time:# and (time.time() - server.last_request_time) <= keep_alive_time:
    #     accumulated_time += int(keep_alive_time)
    # print("loop closes")
    # loop.stop()

# declare pages




plant_app = userv.App()


def _index(writer, request):
    return userv.static_file(writer, "index.html", buf)


def _static_js(writer, request):
    return userv.static_file(writer, "app.bundle.js", buf)


def _static_css(writer, request):
    return userv.static_file(writer, "styles.bundle.css", buf)


def _get_data(writer, request):
    sens_data = sensor.sensor_data()
    settings_data = settings.get_settings()
    sens_data.update(settings_data.get('added_infos_to_sensor_data', {}))
    return userv.json(writer, sens_data)


def _get_settings(writer, request):
    return userv.json(writer, settings.get_settings())


def _post_settings(writer, request):
    try:
        new_settings = ujson.loads(request.get('body'))
    except:
        return userv.json(writer, {"message": ""}, status=406)
    updated_settings = settings.save_settings(settings.get_settings(), new_settings)
    return userv.json(writer, updated_settings)


# routes
plant_app.add_route("/", _index, method='GET')
plant_app.add_route("/app.bundle.js", _static_js, method='GET')
plant_app.add_route("/styles.bundle.css", _static_css, method='GET')
plant_app.add_route("/data", _get_data, method='GET')
plant_app.add_route("/settings", _get_settings, method='GET')
plant_app.add_route("/settings", _post_settings, method='POST')



# run server
print(gc.mem_free())

plant_app.run_server(
    timeout_callback=shutdown_reached
)
print(gc.mem_free())

# deepsleep.set_awake_time_and_put_to_deepsleep(
#     loaded_settings.get("deepsleep_s", 100)
# )