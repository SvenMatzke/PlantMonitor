import uasyncio as asyncio
import ujson


STATUS_CODES = {
    100: b'Continue',
    101: b'Switching Protocols',
    102: b'Processing',
    200: b'OK',
    201: b'Created',
    202: b'Accepted',
    203: b'Non-Authoritative Information',
    204: b'No Content',
    205: b'Reset Content',
    206: b'Partial Content',
    207: b'Multi-Status',
    208: b'Already Reported',
    300: b'Multiple Choices',
    301: b'Moved Permanently',
    302: b'Found',
    303: b'See Other',
    304: b'Not Modified',
    305: b'Use Proxy',
    400: b'Bad Request',
    401: b'Unauthorized',
    403: b'Forbidden',
    404: b'Not Found',
    405: b'Method Not Allowed',
    406: b'Not Acceptable',
    407: b'Proxy Authentication Required',
    408: b'Request Timeout',
    409: b'Conflict',
    410: b'Gone',
    415: b'Unsupported Media Type',
    417: b'Expectation Failed',
    422: b'Unprocessable Entity',
    423: b'Locked',
    424: b'Failed Dependency',
    426: b'Upgrade Required',
    428: b'Precondition Required',
    429: b'Too Many Requests',
    431: b'Request Header Fields Too Large',
    500: b'Internal Server Error',
    501: b'Not Implemented',
    502: b'Bad Gateway',
    503: b'Service Unavailable',
    511: b'Network Authentication Required'
}
HTTP_METHODS = ('GET', 'POST', 'PUT', 'HEAD', 'OPTIONS', 'PATCH', 'DELETE')


async def _render_headers(*args):
    """

    :param args:
    :rtype: binary
    """
    content_str = b""
    for header, content in args:
        content_str += b"%s: %s\r\n" % (header, content)
    return content_str


# Response part
async def text(data, status=200, content_type="text/html", headers=None):
    """
    :type data: str
    :type status: int
    :type content_type: str
    :type headers: list
    :return: binary
    """
    if headers is None:
        headers = list()
    else:
        headers = list(headers)
    headers.append(("Content-Type", "%s; utf-8" % content_type))
    headers.append(("Content-Length", str(len(data))))
    html_string = b"HTTP/1.1 %i %s\r\n" \
                  b"%s" \
                  b"\r\n" \
                  b"%s\r\n" % (
                      status,
                      STATUS_CODES.get(status, b"NA"),
                      await _render_headers(*headers),
                      data
                  )
    return html_string


async def json(data, status=200, headers=None):
    """
    casts the data contrainer into an string and returns a complete response string
    """
    content_type = "application/json"
    try:
        data_string = ujson.dumps(data)
    except:
        return await text(
            "",
            status=422,
            headers=headers
        )
    return await text(
        data_string,
        status=status,
        content_type=content_type,
        headers=headers
    )


# Request part
"""
 GET / HTTP/1.1\r\nAccept: text/html, application/xhtml+xml, image/jxr, */*\r\nAccept-Language: de-DE,de;q=0.8,en-US;q=0.5,en;q=0.3\r\nUser-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063\r\nAccept-Encoding: gzip, deflate\r\nHost: 192.168.4.1\r\nConnection: Keep-Alive\r\n\r\n'

'GET /favicon.ico HTTP/1.1\r\nHost: 192.168.4.1\r\nConnection: keep-alive\r\nPragma: no-cache\r\nCache-Control: no-cache\r\nUser-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36\r\nAccept: image/webp,image/apng,image/*,*/*;q=0.8\r\nReferer: http://192.168.4.1/\r\nAccept-Encoding: gzip, deflate\r\nAccept-Language: de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7\r\n\r\n'
'GET / HTTP/1.1\r\nHost: 192.168.4.1\r\nConnection: keep-alive\r\nCache-Control: max-age=0\r\nUser-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36\r\nUpgrade-Insecure-Requests: 1\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8\r\nAccept-Encoding: gzip, deflate\r\nAccept-Language: de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7\r\n\r\n'



"""


def unquote_plus(s):
    # TODO: optimize
    s = s.replace("+", " ")
    arr = s.split("%")
    arr2 = [chr(int(x[:2], 16)) + x[2:] for x in arr[1:]]
    return arr[0] + "".join(arr2)


def parse_qs(s):
    res = {}
    if s:
        pairs = s.split("&")
        for p in pairs:
            vals = [unquote_plus(x) for x in p.split("=", 1)]
            if len(vals) == 1:
                vals.append(True)
            if vals[0] in res:
                res[vals[0]].append(vals[1])
            else:
                res[vals[0]] = [vals[1]]
    return res


async def parse_request(request_string):
    """
    Parses a request and splits them into an dict to return
    :param request_string: str
    :return: dict
    """
    heading, data = request_string.split("\r\n\r\n")
    header = heading.split("\r\n")
    data.rstrip("\r\n")
    method, route, http_version = header[0].split(" ")
    return dict(
        method=method,
        route=route,
        http_version=http_version,
        # header=parse_qs(header[1:]), # TODO
        body=data.rstrip("\r\n")
    )


class App:

    def __init__(self):
        self._routes = dict()

    def add_route(self, route, callback, method='GET'):
        if method not in HTTP_METHODS:
            raise AttributeError("Method %s is not supported" % method)
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
            route_with_slash = route+"/"
            route_without_slash = route

        route_method_dict = self._routes.get(route_with_slash, self._routes.get(route_without_slash, None))
        if route_method_dict is None:
            return 404

        return route_method_dict.get(method, 405)

    async def run_handle(self, reader, writer):
        complete_request = await reader.read()
        parsed_request = await parse_request(complete_request.decode())
        callback = await self._get_callback(route=parsed_request.get('route'), method=parsed_request.get('method'))
        if callback in [404, 405]:
            await text("Requested Route or method is not available", status=callback)
        response = await callback(parsed_request)
        await writer.awrite(
            response
        )
        await writer.aclose()
