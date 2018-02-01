import uasyncio as asyncio
from userv import App, json, text

app = App()
loop = asyncio.get_event_loop()


async def index(request):
    return await text("We need to serve a static index ")


async def get_data(request):
    return await json({"data": "data"})


async def post_data(request):
    return await json({"data": "postdata"})


async def get_settings(request):
    return await json({"data": "damnget"})


async def post_settings(request):
    return await json({"data": "damn"})


# routes
app.add_route("/", index, method='GET')
app.add_route("/data", get_data, method='GET')
app.add_route("/data", post_data, method='POST')
app.add_route("/settings", get_settings, method='GET')
app.add_route("/settings", post_settings, method='POST')


async def shutdown_timeout():
    print("shutdown_active")
    await asyncio.sleep(60)
    print("loop closes")
    loop.stop()


def run_server():
    loop.call_soon(shutdown_timeout())
    print("* Running on http://%s:%s/" % ('0.0.0.0', 80))
    loop.call_soon(asyncio.start_server(app.run_handle, '0.0.0.0', 80))

    loop.run_forever()
    loop.close()
