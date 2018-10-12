import data

dp_teams = ["Royals","Dodgers","Cubs"]
teams = [
    "Orioles",
    "Indians",
    "Tigers",
    "Astros",
    "Angels",
    "Twins",
    "Yankees",
    "Athletics",
    "Mariners",
    "Royals",
    "Dodgers",
    "Cubs",
    "Rays",
    "Rangers",
    "D-backs",
    "Braves",
    "Reds",
    "Rockies",
    "Marlins",
    "Brewers",
    "Mets",
    "Phillies",
    "Pirates",
    "Padres",
    "Giants",
    "Cardinals",
    "Nationals",
    "Blue Jays",
    "Red Sox",
    "White Sox"]

def sanitizer(text):
    text = text.replace("bosox","RED")
    text = text.replace("a's","athletics")
    text = text.replace("cards","cardinals")
    text = text.replace("nats","nationals")
    text = text.replace("box score","box")
    text = text.replace("boxscore","box")
    text = text.replace("o's","orioles")
    text = text.replace("asstros","astros")
    text = text.replace("angles","angels")
    text = text.replace("twinkies","twins")
    text = text.replace("diamondbacks","d-backs")
    text = text.replace("dbags","d-backs")
    text = text.replace("dbacks","d-backs")
    text = text.replace("brew crew","brewers")
    text = text.replace("brewcrew","brewers")
    text = text.replace("royals2","brewers")
    text = text.replace("pads","padres")
    text = text.replace("vagiants","giants")
    text = text.replace("beantown","RED")
    text = text.replace("white sox","WHITE")
    text = text.replace("red sox","RED")
    text = text.replace("blue jays","BLUE")
    return text

def fixnames(arguments):
    for i in range(len(arguments)):
        if arguments[i] == "RED":
            arguments[i] = "red sox"
        elif arguments[i] == "WHITE":
            arguments[i] = "white sox"
        elif arguments[i] == "BLUE":
            arguments[i] = "blue jays"
    return arguments

def userinput(iostring):
    #check that input is a string
    if isinstance(iostring, str):
        #check that input isn't empty
        if iostring != "":
            #lowercase for sanity
            sanitizedstring = sanitizer(iostring.lower())
            #split test into args
            arguments = sanitizedstring.split()
#            print(arguments)
            ui = fixnames(arguments)
#            print(ui)
            #box scores
            if ui[0] == "!box" or ui[0] == "!status" or ui[0] == "!info":
                return status(ui)
            elif ui[0] == "!ump" or ui[0] == "!umps" or ui[0] == "!umpire" or ui[0] == "!umpires":
                return umpires(ui)
            elif ui[0] == "!replay" or ui[0] == "!replays" or ui[0] == "!challenge" or ui[0] == "!challenges":
                return challenges(ui)
            elif ui[0] == "!batter" or ui[0] == "!batters" or ui[0] == "!batting" or ui[0] == "!order" or ui[0] == "!lineup":
                return batting_order(ui)
            elif ui[0] == "!pitcher" or ui[0] == "!pitchers":
                return pitchers(ui)
            elif ui[0] == "!bench":
                return bench(ui)
            elif ui[0] == "!bullpen" or ui[0] == "!pen" or ui[0] == "!relievers" or ui[0] == "!relief":
                return bullpen(ui)
            elif ui[0] == "!pk":
                return pk(ui)
            elif ui[0][0] == "!":
                return print_help()
        else:
            return 0
    else:
        return 0


def pk(arguments):         
    #check for additional args
    if len(arguments) > 1:
    #check to see if a team was entered
        for i in teams:
            if arguments[1] == i.lower():
                game_info = data.get_scoreboard(i)
                return game_info.print_pk()
        return f"Invalid team {arguments[1]}.\n{print_help()}"
    else:
        return print_help()  

            
def umpires(arguments):         
    #check for additional args
    if len(arguments) > 1:
    #check to see if a team was entered
        for i in teams:
            if arguments[1] == i.lower():
                game_info = data.get_scoreboard(i)
                return game_info.print_umpires()
        return f"Invalid team {arguments[1]}.\n{print_help()}"
    else:
        return print_help()            


def challenges(arguments):         
    #check for additional args
    if len(arguments) > 1:
    #check to see if a team was entered
        for i in teams:
            if arguments[1] == i.lower():
                game_info = data.get_scoreboard(i)
                return game_info.print_challenges()
        return f"Invalid team {arguments[1]}.\n{print_help()}"
    else:
        return print_help()    


def status(arguments):         
    #check for additional args
    if len(arguments) > 1:
    #check to see if a team was entered
        for i in teams:
            if arguments[1] == i.lower():
                game_info = data.get_scoreboard(i)
                return game_info.game_info()
        return f"Invalid team {arguments[1]}.\n{print_help()}"
    else:
        return print_help()
    
    
def batting_order(arguments):         
    #check for additional args
    if len(arguments) > 1:
    #check to see if a team was entered
        for i in teams:
            if arguments[1] == i.lower():
                game_info = data.get_scoreboard(i)
                return game_info.print_batting_order(data.get_team_id(i))
        return f"Invalid team {arguments[1]}.\n{print_help()}"
    else:
        return print_help()


def pitchers(arguments):         
    #check for additional args
    if len(arguments) > 1:
    #check to see if a team was entered
        for i in teams:
            if arguments[1] == i.lower():
                game_info = data.get_scoreboard(i)
                return game_info.print_pitchers(data.get_team_id(i))
        return f"Invalid team {arguments[1]}.\n{print_help()}"
    else:
        return print_help()

    
def bench(arguments):         
    #check for additional args
    if len(arguments) > 1:
    #check to see if a team was entered
        for i in teams:
            if arguments[1] == i.lower():
                game_info = data.get_scoreboard(i)
                return game_info.print_bench(data.get_team_id(i))
        return f"Invalid team {arguments[1]}.\n{print_help()}"
    else:
        return print_help()    

    
def bullpen(arguments):         
    #check for additional args
    if len(arguments) > 1:
    #check to see if a team was entered
        for i in teams:
            if arguments[1] == i.lower():
                game_info = data.get_scoreboard(i)
                return game_info.print_bullpen(data.get_team_id(i))
        return f"Invalid team {arguments[1]}.\n{print_help()}"
    else:
        return print_help()   


def print_help():
    help_dialogue = ('Commands:\n'                        
        '!status [team]\n'
        '-   Returns general info for today\'s [team] game\n'
        '!umpires [team]\n'
        '-   Returns the umpires in today\'s [team] game\n'
        '!replay [team]\n'
        '-   Returns # of replays used/available in today\'s [team] game\n'
        '!batters [team]\n'
        '-   Returns the batting order for today\'s [team] game\n'
        '!pitchers [team]\n'
        '-   Returns the pitchers on the roster for today\'s [team] game\n'
        '!bench [team]\n'
        '-   Returns players still on the bench in today\'s [team] game\n'
        '!bullpen [team]\n'
        '-   Returns the pitchers in the bullpen in today\'s [team] game'

        )
            
    return help_dialogue


