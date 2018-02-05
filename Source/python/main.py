"""

#uploading files
https://learn.adafruit.com/micropython-basics-load-files-and-run-code/boot-scripts

"""
import wlan
import settings
from sensor import senor_data
import uasyncio as asyncio
from server import plant_app, last_request_time
from userv import request
import ujson as json
from deepsleep import set_awake_time_and_put_to_deepsleep
import gc
import time

# get config data
loaded_settings = settings.get_settings()

# if anything fails we are ready to set up
restful_online_time = loaded_settings.get('awake_time_for_config', 300)
keep_alive_time = restful_online_time

if wlan.sta_if.active():
    # wenn connected try to get new config if this fails we set restful_online_time
    # => this will result in more energy consumption, but else you can config this device
    request_url = loaded_settings.get("request_url", None)
    if request_url is not None:
        try:
            # get new settings  # TODO frage ob das drin bleibt
            parsed_reponse = request(request_url)
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
            parsed_reponse = request(
                request_url,
                method="POST",
                body=json.dumps(senor_data(loaded_settings.get('added_infos_to_sensor_data', {})))
            )
            if int(parsed_reponse.get('status_code', 500)) >= 300:
                raise ConnectionError("Response was incorrect")

            keep_alive_time = loaded_settings.get('keep_alive_time_s')
            restful_online_time = loaded_settings.get('max_awake_time_s')
        except Exception as e:
            # data was not send so we will need some config changes
            restful_online_time = loaded_settings.get('awake_time_for_config', 300)

# webserver will be started to listen
loop = asyncio.get_event_loop()

accumulated_time = 0


async def shutdown_timeout():
    global accumulated_time
    print("shutdown_active")
    while accumulated_time < restful_online_time and (time.time() - last_request_time) <= keep_alive_time:
        await asyncio.sleep(keep_alive_time)
        accumulated_time += int(keep_alive_time)
    print("loop closes")
    loop.stop()


# run server
gc.collect()
loop.call_soon(shutdown_timeout())
print("* Running on http://%s:%s/" % ('0.0.0.0', 80))
loop.call_soon(asyncio.start_server(plant_app.run_handle, '0.0.0.0', 80))

loop.run_forever()
loop.close()

set_awake_time_and_put_to_deepsleep(
    loaded_settings.get("deepsleep_s", 100)
)
