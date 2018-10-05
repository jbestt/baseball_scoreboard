import datetime
import data
import vocabulary

now = datetime.datetime.now()
game_info = data.get_scoreboard("Dodgers")

print(game_info.gamePk)
print(game_info.game_state_code)
print(game_info.game_state)
print(game_info.game_info())
print(printers.print_overview_object(game_info))

user_input = input("enter team\n")
print(vocabulary.userinput(user_input))
