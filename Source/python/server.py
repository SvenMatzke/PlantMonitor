import userv
# import sensor
import settings
import ujson

plant_app = userv.App()


def _index(writer, request):
    return userv.static_file(writer, "index.html")


def _static_js(writer, request):
    return userv.static_file(writer, "app.bundle.js")


def _static_css(writer, request):
    return userv.static_file(writer, "styles.bundle.css")


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
