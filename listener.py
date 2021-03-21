from http.server import BaseHTTPRequestHandler
import vocabulary
import groupy

class testHTTPServer_RequestHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        
        self.send_response(200)
        
    def do_POST(self):    
        self.send_response(200)
        if str(self.raw_requestline).find("5e3fdb3a4379a75cf8d06c25fd4b9f78") == -1:
            print("\n\n" + self.raw_requestline)
        else:
            gm_api_key = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
            scoreboard_bot_id = "YYYYYYYYYYYYYYYYYYY"
            client = groupy.Client.from_token(gm_api_key)
            dp_group_id = "4444444444"
           
            for i in client.groups.list_all():
                if i.id == dp_group_id:
                    deadpool = i
                         
            output = ""
            
            for i in deadpool.messages.list(limit=1):
                output = vocabulary.userinput(i.text)
            
            print("Output: " + str(output))
            
            if str(output) != "None" and str(output) != "":
                client.bots.post(scoreboard_bot_id, output)
                

            