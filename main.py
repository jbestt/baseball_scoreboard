#===============================================================================
# from http import server
# import sys
# import select
# import datetime
# import data
# import vocabulary
#===============================================================================
import listener
import groupy
from http.server import HTTPServer


#===============================================================================
# gm_api_key = "rYeaadubaCmn1TgT3zcXAgJz49eSpn4SRp65x4Wg"
# scoreboard_bot_id = "799b29a881dc3652b0866e13c1"
# client = groupy.Client.from_token(gm_api_key)
# dp_group_id = "45030392"
# #this is the real deadpool'd id: 4476689
#===============================================================================



server_address = ('69.164.192.232', 9090)

httpd = HTTPServer(server_address, listener.testHTTPServer_RequestHandler)
httpd.serve_forever()





#===============================================================================
# 
# 
# for i in client.groups.list_all():
#     if i.id == dp_group_id:
#         deadpool = i
#         
# message_page = deadpool.messages.list()
# 
# for message in deadpool.messages.list_all():
#     print(message.text)
# 
# message_page = deadpool.messages.list_after(message_id=message)
# 
# 
# 
# #client.bots.post(scoreboard_bot_id, "tacotown2")
# 
# 
# #client.bots.create("donkey", "45030392")
# #for group in client.groups.list():
# #    if group.name == "bot test":
# #        deadpool = group
# 
# #print(deadpool.members)
# #print(deadpool.id)
# #print(deadpool.messages.list())
# #deadpool.post("hihi2")
# 
# #client.list()
#===============================================================================

#now = datetime.datetime.now()
#user_input = input("Enter command:\n")
#print(vocabulary.userinput(user_input))