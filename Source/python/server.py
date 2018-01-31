import picoweb
import uasyncio

app = picoweb.WebApp("PlantMonitor")
loop = uasyncio.get_event_loop()


@app.route("/")
def index(req, resp):
    yield from picoweb.start_response(resp)

    yield from resp.awrite("We need to serve a static index ")


@app.route("/data", method=['GET'])
def get_data(req, resp):
    yield from picoweb.start_response(resp)
    yield from picoweb.jsonify(resp, {"data": "data"})


@app.route("/data", method=['POST'])
def post_data(req, resp):
    yield from picoweb.start_response(resp)
    yield from picoweb.jsonify(resp, {"data": "postdata"})


@app.route("/settings", method=['GET'])
def get_settings(req, resp):
    yield from picoweb.start_response(resp)
    yield from picoweb.jsonify(resp, {"data": "damnget"})


@app.route("/settings", method=['POST'])
def post_settings(req, resp):
    yield from picoweb.start_response(resp)
    yield from picoweb.jsonify(resp, {"data": "damn"})


def shutdown_timeout():
    yield uasyncio.sleep(60)
    loop.stop()


import logging

logging.basicConfig(level=logging.INFO)

loop.create_task(shutdown_timeout())
app.run(port=80)
