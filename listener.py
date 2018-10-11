from http.server import BaseHTTPRequestHandler, HTTPServer

class testHTTPServer_RequestHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        
        self.send_response(200)
        
#        print(self.raw_requestline)
        
    def do_POST(self):    
        self.send_response(200)
        if str(self.raw_requestline).find("5e3fdb3a4379a75cf8d06c25fd4b9f78") == -1:
            print("\n\n" + self.raw_requestline)
        else:
            print("New message")
            