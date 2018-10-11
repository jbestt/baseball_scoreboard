from http.server import BaseHTTPRequestHandler, HTTPServer

class testHTTPServer_RequestHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        
        self.send_response(200)
        
        print(self.raw_requestline)