from urllib.parse import urlparse, parse_qs
from http.server import BaseHTTPRequestHandler, HTTPServer

with open("index.html", mode="r") as f:
    index = f.read()
with open("next.html", mode="r") as f:
    next = f.read()

routes = []


def route(path, method):
    routes.append((path, method))


route("/", "index")
route("/index", "index")
route("/next", "next")
route("/xml", "xml")


class HelloServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        global routes
        _url = urlparse(self.path)
        for r in routes:
            if r[0] == _url.path:
                eval("self." + r[1] + "()")
                break
        else:
            self.error()
        return

    def index(self):
        _url = urlparse(self.path)
        self.send_response(200)
        self.end_headers()
        html = index.format(
            titel="Hello",
            link="/next?" + _url.query,
            message="HTTPServerの世界へようこそ！"
        )
        self.wfile.write(html.encode("utf-8"))
        return

    def next(self):
        self.send_response(200)
        self.end_headers()
        html = next.format(
            message="header data",
            data=self.headers
        )
        self.wfile.write(html.encode("utf-8"))
        return

    def xml(self):
        xml='''<?xml version="1.0" encoding="UTF-8"?>
        <data>
            <person>
                <name>Taro</name>
                <mail>taro@yamada</mail>
                <age>39</age>
            </person>
        </data>'''
        self.send_response(200)
        self.send_header("Content-Type", "application/xml; charset=utf-8")
        self.end_headers()
        self.wfile.write(xml.encode("utf-8"))
        return

    def error(self):
        self.send_error(404, "CANNOT ACCESS!!")
        return


HTTPServer(("", 8000), HelloServerHandler).serve_forever()
