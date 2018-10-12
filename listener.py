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
            gm_api_key = "rYeaadubaCmn1TgT3zcXAgJz49eSpn4SRp65x4Wg"
            scoreboard_bot_id = "799b29a881dc3652b0866e13c1"
            client = groupy.Client.from_token(gm_api_key)
            dp_group_id = "45030392"
            #this is the real deadpool'd id: 4476689
           
            for i in client.groups.list_all():
                if i.id == dp_group_id:
                    deadpool = i
                         
            output = ""
            
            for i in deadpool.messages.list(limit=1):
                output = vocabulary.userinput(i.text)
            
            print("Output: " + str(output))
            
            #if output != "None" and output != "":
            #   client.bots.post(scoreboard_bot_id, output)
                

            