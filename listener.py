from http.server import BaseHTTPRequestHandler, HTTPServer

class testHTTPServer_RequestHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        
        self.send_response(200)
        
        print(self.raw_requestline)
        
    def do_POST(self):    
        self.send_response(200)
        if self.raw_requestline == "b'POST /5e3fdb3a4379a75cf8d06c25fd4b9f78 HTTP/1.1\\r\\n'":
            print("New message")