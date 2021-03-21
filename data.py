import datetime
import urllib3
import json
import game
import pytz

#Running from a server in Central Time. Days reset at 3am Pacific.
#now = datetime.datetime.now()-datetime.timedelta(hours=5, minutes=0)
#deug, remove line below
#now = datetime.datetime.now()-datetime.timedelta(days=2, hours=5, minutes=0)

def get_team_names():
    return ["Royals","Dodgers","Cubs"]

def get_team_list():
    now = datetime.datetime.now()-datetime.timedelta(hours=5, minutes=0)
    year=now.year
    http = urllib3.PoolManager()
    request = http.request('GET','http://statsapi.mlb.com/api/v1/teams?sportId=1&season=%d' % year)
    teams = json.loads(request.data)
    return teams

def get_team_id(team):
    teams = get_team_list()
    for i in teams["teams"]:
        if i["teamName"] == team:
            team_id = i["id"]
            return team_id
    return 0

def get_game_pk(team):
    now = datetime.datetime.now()-datetime.timedelta(hours=5, minutes=0)
    year=now.year
    month=now.month
    day=now.day
    team_id = get_team_id(team)
    http = urllib3.PoolManager()
    request = http.request('GET','http://statsapi.mlb.com/api/v1/schedule?sportId=1&date='
                           '{0:02d}%2F{1:02d}%2F{2}'.format(month,day,year))
    schedule = json.loads(request.data)
    for i in schedule["dates"][0]["games"]:
        if i["teams"]["away"]["team"]["id"] == team_id or i["teams"]["home"]["team"]["id"] == team_id: 
            return(i['gamePk'])
    return 0    

def get_tv_runner_info(pk):
    now = datetime.datetime.now()-datetime.timedelta(hours=5, minutes=0)
    year=now.year
    month=now.month
    day=now.day

    
    http = urllib3.PoolManager()
    request = http.request('GET','http://gd.mlb.com/components/game/mlb/year_{0}/month_{1:02d}/day_{2:02d}/master_scoreboard.json'.format(year,month,day))
    alt_scoreboard = json.loads(request.data)
    alt_info = ""
    if alt_scoreboard['data']['games']['game'][0]['game_media']:
        print("one game today")
        alt_info = alt_scoreboard['data']['games']['game'][0]
#    elif '0' in alt_scoreboard['data']['games']['game']:
    else:
        print("multiple games today")
        for i in alt_scoreboard['data']['games']['game']:
#            print(i)
#            print(i['game_pk'])
#            print("ref" + pk)
            if str(i['game_pk']) == str(pk):
                alt_info = i
            
    return alt_info

    
def get_scoreboard(team):
    
    game_pk = get_game_pk(team)
    http = urllib3.PoolManager()
    request = http.request('GET','http://statsapi.mlb.com/api/v1.1/game/' + str(game_pk) + '/feed/live')
    scoreboard = json.loads(request.data)
    game_info = game.Game(scoreboard)
    return game_info

def convert_mlbtime_pacific(time):
    #convert mlb time to datetime object
    mlb_date = datetime.datetime.strptime(time, "%Y-%m-%dT%H:%M:%SZ")
    #add utc timezone to mlb datetime object
    utc_date = mlb_date.replace(tzinfo=pytz.utc)
    #convert to pacific time
    date = utc_date.astimezone(pytz.timezone('US/Pacific'))
    return date
