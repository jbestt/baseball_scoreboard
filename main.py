import datetime
import data
import vocabulary

now = datetime.datetime.now()
game_info = data.get_scoreboard("Dodgers")

print(game_info.gamePk)
#print(game_info.game_state_code)
#print(game_info.game_state)
#print(game_info.game_info())

user_input = input("Enter command:\n")
print(vocabulary.userinput(user_input))
