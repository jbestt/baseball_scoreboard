#
import datetime
import data
import vocabulary

now = datetime.datetime.now()
game_info = data.get_scoreboard("D-backs")

print(game_info.gamePk)
print(game_info.game_state_code)
print(game_info.game_state)
print(game_info.game_info())


user_input = input("enter team")
print(vocabulary.userinput(user_input))
