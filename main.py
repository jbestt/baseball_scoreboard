import listener
from http.server import HTTPServer

server_address = ('69.164.192.232', 9090)

httpd = HTTPServer(server_address, listener.testHTTPServer_RequestHandler)
httpd.serve_forever()