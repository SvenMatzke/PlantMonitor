import socket
import ujson
import os
import gc

_status_lookup = (
    (200, b'OK'),
    (201, b'Created'),
    (202, b'Accepted'),
    (203, b'Non-Authoritative Information'),
    (204, b'No Content'),
    (205, b'Reset Content'),
    (206, b'Partial Content'),
    (207, b'Multi-Status'),
    (208, b'Already Reported'),
    (300, b'Multiple Choices'),
    (301, b'Moved Permanently'),
    (302, b'Found'),
    (303, b'See Other'),
    (304, b'Not Modified'),
    (305, b'Use Proxy'),
    (400, b'Bad Request'),
    (401, b'Unauthorized'),
    (403, b'Forbidden'),
    (404, b'Not Found'),
    (405, b'Method Not Allowed'),
    (406, b'Not Acceptable'),
    (407, b'Proxy Authentication Required'),
    (408, b'Request Timeout'),
    (409, b'Conflict'),
    (410, b'Gone'),
    (415, b'Unsupported Media Type'),
    (417, b'Expectation Failed'),
    (422, b'Unprocessable Entity'),
    (423, b'Locked'),
    (424, b'Failed Dependency'),
    (426, b'Upgrade Required'),
    (428, b'Precondition Required'),
    (429, b'Too Many Requests'),
    (431, b'Request Header Fields Too Large'),
    (500, b'Internal Server Error'),
    (501, b'Not Implemented'),
    (502, b'Bad Gateway'),
    (503, b'Service Unavailable'),
)


def _get_status_text(status_code):
    status_text_list = [text for code, text in _status_lookup if code == status_code]
    if len(status_text_list) == 0:
        return b"NA"
    return status_text_list[0]


def _get_mime_type(fname):
    # Provide minimal detection of important file
    # types to keep browsers happy
    if fname.endswith(".html"):
        return "text/html"
    if fname.endswith(".css"):
        return "text/css"
    if fname.endswith(".js"):
        return "text/javascript"
    if fname.endswith(".png") or fname.endswith(".jpg"):
        return "image"
    return None


def _render_headers(*args):
    content_str = b""
    for header, content in args:
        content_str += b"%s: %s\r\n" % (header, content)
    return content_str


def _response_header(status=200, content_type="text/html", content_length=None, headers=None):
    if headers is None:
        headers = list()
    else:
        headers = list(headers)
    headers.append(("Content-Type", "%s; utf-8" % content_type))
    if content_length is not None:
        headers.append(("Content-Length", str(content_length)))
    html_string = b"HTTP/1.1 %i %s\r\n" \
                  b"%s" \
                  b"\r\n" % (
                      status,
                      _get_status_text(status),
                      _render_headers(*headers),
                  )
    return html_string


def _parse_header(list_of_header_str):
    header = dict()
    for header_str in list_of_header_str:
        key, value = header_str.split(":")[:2]
        header[key] = value
    return header


def _parse_request(request_string):
    heading, data = request_string.split("\r\n\r\n")[:2]
    header = heading.split("\r\n")
    data.rstrip("\r\n")
    method, route, http_version = header[0].split(" ")[:3]
    return dict(
        method=method,
        route=route,
        http_version=http_version,
        header=_parse_header(header[1:]),
        body=data.rstrip("\r\n")
    )


def text(writer, data, status=200, content_type="text/html", headers=None):
    if headers is None:
        headers = list()
    else:
        headers = list(headers)
    html_string = b"%s" \
                  b"%s\r\n" % (
                      _response_header(
                          status=status,
                          content_type=content_type,
                          content_length=len(data),
                          headers=headers
                      ),
                      data
                  )

    writer.write(html_string)


def json(writer, data, status=200, headers=None):
    content_type = "application/json"
    try:
        data_string = ujson.dumps(data)
    except:
        text(
            writer,
            "cant decode data to json",
            status=422,
            headers=headers
        )
        return
    text(
        writer,
        data_string,
        status=status,
        content_type=content_type,
        headers=headers
    )


def static_file(writer, fname, buffer):
    if fname not in os.listdir():
        text(
            writer,
            "",
            status=404
        )
    else:
        mime_type = _get_mime_type(fname)
        if mime_type is None:
            text(
                writer,
                "",
                status=415,
            )
            return
        # serve static file
        content_len = os.stat(fname)[6]
        buffer_size = len(buffer)
        writer.write(
            _response_header(
                status=200,
                content_type=mime_type,
                content_length=content_len
            )
        )
        file_ptr = open(fname, "rb")
        for _ in range(0, (content_len // buffer_size)):
            file_ptr.readinto(buffer)
            writer.write(buffer)
            gc.collect()

        readed_len = file_ptr.readinto(buffer)
        writer.write(buffer[:readed_len])
        writer.write(b'\r\n')
        file_ptr.close()
        gc.collect()


class App:

    def __init__(self):
        self._routes = dict()

    def add_route(self, route, callback, method='GET'):
        if route in self._routes:
            self._routes[route][method] = callback
        else:
            self._routes[route] = {method: callback}

    def _get_callback(self, route, method):
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

    def read_buffered_request(self, reader):
        req = list()
        while True:
            line = reader.readline()
            req.append(line)
            if not line or line == b'\r\n':
                break
        return b"".join(req)

    def run_server(self, ip_address="0.0.0.0", port=80, timeout_callback=None):
        """
        this method will handle the gc it self and so should your sites
        :param ip_address:
        :param port:
        :param timeout_callback: if None we run forever
        """
        addr = socket.getaddrinfo(ip_address, port)[0][-1]

        # creating socket mess
        s = socket.socket()
        gc.disable()
        s.bind(addr)
        s.listen(1)
        timeout = lambda: True
        if timeout_callback is not None:
            timeout = timeout_callback
        try:
            while timeout():
                try:
                    gc.collect()
                    s.settimeout(60)
                    writer, client_addr = s.accept()

                    print('client connected from: ', client_addr)
                    # read request
                    reader = writer.makefile('rwb', 0)

                    try:
                        self.run_handle(reader, writer)
                    finally:
                        reader.close()
                    writer.close()
                except Exception as e:
                    print(e)
        finally:
            # always close the socket
            s.close()
            gc.enable()

    def run_handle(self, reader, writer):
        complete_request = self.read_buffered_request(reader)
        gc.collect()
        parsed_request = _parse_request(complete_request.decode())
        gc.collect()
        route = parsed_request.get('route')
        print("Serving ", route, " | ", parsed_request.get('method'))
        # routes
        callback = self._get_callback(route=route, method=parsed_request.get('method'))
        gc.collect()
        if not callable(callback):
            text(writer, "Requested Route or method is not available", status=404)
        else:
            callback(writer, parsed_request)
