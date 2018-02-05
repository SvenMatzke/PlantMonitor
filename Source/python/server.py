from userv import App, json, text
from sensor import senor_data
from settings import get_settings, save_settings
import ujson
import time

plant_app = App()
last_request_time = time.time()


async def index(request):
    global last_request_time
    last_request_time = time.time()
    return await text("We need to serve a static index ")


async def get_data(request):
    global last_request_time
    last_request_time = time.time()
    settings = get_settings()
    return await json(senor_data(settings.get('added_infos_to_sensor_data', {})))


async def get_setting(request):
    global last_request_time
    last_request_time = time.time()
    return await json(get_settings())


async def post_settings(request):
    global last_request_time
    last_request_time = time.time()
    try:
        new_settings = ujson.loads(request.get('body'))
    except:
        return await json({"message": ""}, status=406)
    updated_settings = save_settings(new_settings)
    return await json(updated_settings)


# routes
plant_app.add_route("/", index, method='GET')
plant_app.add_route("/data", get_data, method='GET')
plant_app.add_route("/settings", get_setting, method='GET')
plant_app.add_route("/settings", post_settings, method='POST')
