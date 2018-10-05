import printers
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
            print(arguments)
            ui = fixnames(arguments)
            print(ui)
            #box scores
            if ui[0] == "box" or ui[0] == "status" or ui[0] == "info":
                return status(ui)
            else:
                return print_help()
        else:
            return print_help()
    else:
        return print_help()
            
            


def status(arguments):         
    #check for additional args
    if len(arguments) > 1:
    #check to see if a team was entered
        for i in teams:
            if arguments[1] == i.lower():
                print("check")
                game_info = data.get_scoreboard(i)
                return game_info.game_info()
            else:
                return f"Invalid team {arguments[1]}.\n{print_help()}"
    else:
        return print_help()

def print_help():
    help_dialogue = ('Commands\n'                        
        'status [Team]\n'
        '    Returns info for today\'s [Team] game\n'
        '\n'
        '\n'
        )
            
    return help_dialogue


