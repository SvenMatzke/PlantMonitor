import userv
import sensor
import settings
import time
import ujson

plant_app = userv.App()
last_request_time = time.time()


async def index(writer, request):
    global last_request_time
    last_request_time = time.time()
    return await userv.static_file(writer, "index.html")


async def static_js(writer, request):
    global last_request_time
    last_request_time = time.time()
    return await userv.static_file(writer, "app.bundle.js")


async def static_css(writer, request):
    global last_request_time
    last_request_time = time.time()
    return await userv.static_file(writer, "styles.bundle.css")


async def get_data(writer, request):
    global last_request_time
    last_request_time = time.time()
    sens_data = sensor.sensor_data()
    settings_data = settings.get_settings()
    sens_data.update(settings_data.get('added_infos_to_sensor_data', {}))
    return await userv.json(writer, sens_data)


async def get_setting(writer, request):
    global last_request_time
    last_request_time = time.time()
    return await userv.json(writer, settings.get_settings())


async def post_settings(writer, request):
    global last_request_time
    last_request_time = time.time()
    try:
        new_settings = ujson.loads(request.get('body'))
    except:
        return await userv.json(writer, {"message": ""}, status=406)
    updated_settings = settings.save_settings(settings.get_settings(), new_settings)
    return await userv.json(writer, updated_settings)


# routes
plant_app.add_route("/", index, method='GET')
plant_app.add_route("/app.bundle.js", static_js, method='GET')
plant_app.add_route("/styles.bundle.css", static_css, method='GET')
plant_app.add_route("/data", get_data, method='GET')
plant_app.add_route("/settings", get_setting, method='GET')
plant_app.add_route("/settings", post_settings, method='POST')
