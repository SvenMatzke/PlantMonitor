import ujson
import os
import requests


async def text(writer, data, status=200, content_type="text/html", headers=None):
    if headers is None:
        headers = list()
    else:
        headers = list(headers)
    headers.append(("Content-Type", "%s; utf-8" % content_type))
    headers.append(("Content-Length", str(len(data))))
    html_string = b"%s" \
                  b"%s\r\n" % (
                      requests.response_header(
                          status=status,
                          content_type=content_type,
                          content_length=len(data),
                          headers=headers
                      ),
                      data
                  )

    return await writer.awrite(html_string)


async def json(writer, data, status=200, headers=None):
    content_type = "application/json"
    try:
        data_string = ujson.dumps(data)
    except:
        return await text(
            writer,
            "",
            status=422,
            headers=headers
        )
    return await text(
        writer,
        data_string,
        status=status,
        content_type=content_type,
        headers=headers
    )


async def static_file(writer, fname):
    if fname not in os.listdir():
        await writer.awrite(
            await text(
                writer,
                "File %s is not available " % fname,
                status=404
            )
        )
    else:
        mime_type = requests.get_mime_type(fname)
        if mime_type is None:
            await writer.awrite(
                await text(
                    writer,
                    "",
                    status=415,
                )
            )
        else:
            # serve static file
            await  writer.awrite(
                requests.response_header(
                    status=200,
                    content_type=mime_type,
                    content_length=os.stat(fname)[0]
                )
            )
            file_ptr = open(fname)
            buf = bytearray(64)
            while True:
                l = file_ptr.readinto(buf)
                if not l:
                    break
                await writer.awrite(buf, 0, l)
            file_ptr.close()


class App:

    def __init__(self):
        self._routes = dict()

    def add_route(self, route, callback, method='GET'):
        if route in self._routes:
            self._routes[route][method] = callback
        else:
            self._routes[route] = {method: callback}

    async def _get_callback(self, route, method):
        """
        :type route: str
        :type method: str
        """
        if route.endswith("/"):
            route_with_slash = route
            route_without_slash = route[:-1]
        else:
            route_with_slash = route + "/"
            route_without_slash = route

        route_method_dict = self._routes.get(route_with_slash, self._routes.get(route_without_slash, None))
        if route_method_dict is None:
            return 404

        return route_method_dict.get(method, 405)

    async def run_handle(self, reader, writer):
        complete_request = await reader.read()
        parsed_request = requests.parse_request(complete_request.decode())
        route = parsed_request.get('route')

        # routes
        callback = await self._get_callback(route=route, method=parsed_request.get('method'))
        if callback in [404, 405]:
            await text("Requested Route or method is not available", status=callback)
        # send response
        await callback(writer, parsed_request)
        await writer.aclose()
