import data

class Game:
    def __init__(self, scoreboarddata):
        self.var = scoreboarddata
        
        if "messageNumber" in scoreboarddata or "message" in scoreboarddata:
            self.gamePk = 0
            self.game_state_code = "UNPOPULATED"
        else:
            
            self.gamePk = self.var["gamePk"]
            self.home_team_id = self.var["gameData"]["teams"]["home"]["id"]
            self.home_team = self.var["gameData"]["teams"]["home"]["teamName"]
            self.home_team_abbreviation = self.var["gameData"]["teams"]["home"]["abbreviation"]  
            self.away_team_id = self.var["gameData"]["teams"]["away"]["id"]
            self.away_team = self.var["gameData"]["teams"]["away"]["teamName"]
            self.away_team_abbreviation = self.var["gameData"]["teams"]["away"]["abbreviation"]
            self.venue = self.var["gameData"]["teams"]["home"]["venue"]["name"]
            self.doubleHeader = self.var["gameData"]["game"]["doubleHeader"]
            self.home_team_wins =  self.var["gameData"]["teams"]["home"]["record"]["wins"]
            self.home_team_losses = self.var["gameData"]["teams"]["home"]["record"]["losses"] 
            self.away_team_wins = self.var["gameData"]["teams"]["away"]["record"]["wins"]
            self.away_team_losses = self.var["gameData"]["teams"]["away"]["record"]["losses"]
            self.start_time_full = data.convert_mlbtime_pacific(self.var["gameData"]["datetime"]["dateTime"])
            self.start_time_formatted = self.start_time_full.strftime('%b %d %H:%M PT')
            self.game_state_code = self.var["gameData"]["status"]["codedGameState"]
            self.game_state = self.var["gameData"]["status"]["detailedState"]
            self.home_score = self.var["liveData"]["boxscore"]["teams"]["home"]["teamStats"]["batting"]["runs"]
            self.away_score = self.var["liveData"]["boxscore"]["teams"]["away"]["teamStats"]["batting"]["runs"]
            self.abstract = self.var["gameData"]["status"]["abstractGameState"]
            
            if self.game_state_code != "S" and self.game_state_code != "P":
                self.home_challenges_used = self.var["gameData"]["review"]["home"]["used"]
                self.home_challenges_remaining = self.var["gameData"]["review"]["home"]["remaining"]
                self.away_challenges_used = self.var["gameData"]["review"]["away"]["used"]
                self.away_challenges_remaining = self.var["gameData"]["review"]["away"]["remaining"]
                self.inning = self.var["liveData"]["linescore"]["currentInning"]
                self.inning_ordinal = self.var["liveData"]["linescore"]["currentInningOrdinal"]
                self.inning_state = self.var["liveData"]["linescore"]["inningState"]
                self.all_officials = self.var["liveData"]["boxscore"]["officials"]
                
                
                        
#                self.tv
                
                if self.abstract == "Live":
                    self.count_balls = self.var["liveData"]["plays"]["currentPlay"]["count"]["balls"]
                    self.count_strikes = self.var["liveData"]["plays"]["currentPlay"]["count"]["strikes"]
                    self.count_outs = self.var["liveData"]["plays"]["currentPlay"]["count"]["outs"]
                    self.current_batter = self.var["liveData"]["plays"]["currentPlay"]["matchup"]["batter"]["fullName"]
                    self.current_pitcher = self.var["liveData"]["plays"]["currentPlay"]["matchup"]["pitcher"]["fullName"]
                    
                    self.current_play_info = self.var["liveData"]["plays"]["currentPlay"]["result"]
                    
                    if "event" in self.current_play_info:
                        self.current_play = self.var["liveData"]["plays"]["currentPlay"]["result"]["description"]
                    else:
                        self.current_play = ""
                        
                    self.alt_info = data.get_tv_runner_info(self.gamePk)
                    
                    if self.alt_info != "":
                        self.home_tv = self.alt_info['broadcast']['home']['tv']
                        self.away_tv = self.alt_info['broadcast']['away']['tv']
                        
                        self.baserunners = {'1b':"",'2b':"",'3b':""}
                        if 'runner_on_1b' in self.alt_info['runners_on_base']:
                            self.baserunners['1b'] = f"{self.alt_info['runners_on_base']['runner_on_1b']['last']}"
                        if 'runner_on_2b' in self.alt_info['runners_on_base']:
                            self.baserunners['2b'] = f"{self.alt_info['runners_on_base']['runner_on_2b']['last']}"
                        if 'runner_on_3b' in self.alt_info['runners_on_base']:
                            self.baserunners['3b'] = f"{self.alt_info['runners_on_base']['runner_on_3b']['last']}"
                    else:
                        self.home_tv = ""
                        self.away_tv = ""
                        self.baserunners = ""
                        
                        
    def game_info(self):
        if self.game_state_code == "S" or self.game_state_code == "P":
            return self.print_preview()
        elif self.game_state_code == "F" or self.game_state_code == "O":
            return self.print_final()
        elif self.game_state_code == "UNPOPULATED":
            return self.print_fail_status()
        else:
            return self.print_live_status()
     
        
    def print_umpires(self):
        if self.game_state_code != "S" and self.game_state_code != "P" and self.game_state_code != "UNPOPULATED":
            umpstring = f"Umpires for {self.away_team} @ {self.home_team}:"
            
            for i in self.all_officials:
                if i != 0:
                    umpstring = f"{umpstring}\n"
                umpstring = f"{umpstring}{i['officialType']}: {i['official']['fullName']}"
            return umpstring

        else:
            umpstring = "Umpire information unavailable."
            return umpstring
        

    def print_fail_status(self):
        return "Error: No game information was found."


    def print_preview(self):
        if self.game_state_code == "S" or self.game_state_code == "P":
            return f"{self.start_time_formatted}: {self.away_team} ({self.away_team_wins}-{self.away_team_losses}) @ {self.home_team} ({self.home_team_wins}-{self.home_team_losses})"
        return "Data unavailable."

        
    def print_live_status(self):
        current_score = f"{self.away_team} {self.away_score} - {self.home_team} {self.home_score}"
        inning_info = f"{self.inning_state} of the {self.inning_ordinal}"
        if self.inning_state == "End" or self.inning_state == "Middle":
            return f"Game in progress.\n{current_score}\n{inning_info}"
        at_bat = ""
        runners = self.print_runners()
        if self.current_play != "":
            at_bat = self.current_play
        else:
            at_bat = f"{runners}{self.current_pitcher} pitches to {self.current_batter}."
        outs_balls_strikes = f"\nBalls: {self.count_balls} Strikes: {self.count_strikes} Outs: {self.count_outs}"

        return f"Game in progress.\n{current_score}\n{inning_info}\n{at_bat}{outs_balls_strikes}"
                    
        
    def print_runners(self): 
        runnerstring = "Bases empty"   
        if self.baserunners['1b'] != "":
            runnerstring = f"{self.baserunners['1b']} on 1B"
        if self.baserunners['2b'] != "":
            if runnerstring != "Bases empty":
                runnerstring = f"{runnerstring}, "
            runnerstring = f"{self.baserunners['2b']} on 2B"
        if self.baserunners['3b'] != "":
            if runnerstring != "Bases empty":
                runnerstring = f"{runnerstring}, "
            runnerstring = f"{self.baserunners['3b']} on 3B"
        runnerstring = f"{runnerstring}.\n"
        return runnerstring

        
    def print_final(self):
        if self.game_state_code == "F" or self.game_state_code == "O":
            self.pitcher_win = self.var["liveData"]["decisions"]["winner"]["fullName"]
            self.pitcher_lose = self.var["liveData"]["decisions"]["loser"]["fullName"]
            try:
                self.pitcher_save = self.var["liveData"]["decisions"]["save"]["fullName"]
                pitchstring = f"WP: {self.pitcher_win}\nLP: {self.pitcher_lose}\nSV: {self.pitcher_save}"
            except:
                pitchstring = f"WP: {self.pitcher_win}\nLP: {self.pitcher_lose}"
                
            extras = ""
            
            if int(self.inning) > 9:
                extras = f"/{self.inning}"
            
            scorestring = f"{self.away_team} {self.away_score} - {self.home_team} {self.home_score} Final{extras}"
            return f"{scorestring}\n{pitchstring}"
        
        else:
            return "Data unavailable."
    
    
    def print_challenges(self):
        if self.game_state_code != "S" and self.game_state_code != "P" and self.game_state_code != "UNPOPULATED":
            return f"Challenges (Used - Remaining):\n{self.away_team}: {self.away_challenges_used} - {self.away_challenges_remaining}\n{self.home_team}: {self.home_challenges_used} - {self.home_challenges_remaining}"
        else:
            return "Replay data unavailable."

    
    def print_batting_order(self, team_id):
        if self.game_state_code != "S" and self.game_state_code != "P" and self.game_state_code != "UNPOPULATED":
            if team_id == self.away_team_id:
                batting_order = self.var["liveData"]["boxscore"]["teams"]["away"]["players"]
                teamdict = {}
                teamstring = ""
                for i in batting_order:
                    if "battingOrder" in self.var["liveData"]["boxscore"]["teams"]["away"]["players"][i]:
                        playername = self.var['liveData']['boxscore']['teams']['away']['players'][i]['person']['fullName']
                        playerpos = self.var['liveData']['boxscore']['teams']['away']['players'][i]['position']['abbreviation']
                        batorder = self.var["liveData"]["boxscore"]["teams"]["away"]["players"][i]["battingOrder"]
                        teamdict[batorder] = f"{playername} {playerpos}"
                for d in sorted(teamdict.keys()):
                    if d != "100":
                        teamstring = f"{teamstring}\n"
                    if int(d)%100 == 0:
                        teamstring = f"{teamstring}{int(int(d)/100)} "
                    if int(d)%100:
                        teamstring = f"{teamstring}   \_"
                    teamstring = f"{teamstring}{teamdict[d]}"
                return teamstring
            elif team_id == self.home_team_id:
                batting_order = self.var["liveData"]["boxscore"]["teams"]["home"]["players"]
                teamdict = {}
                teamstring = ""
                for i in batting_order:
                    if "battingOrder" in self.var["liveData"]["boxscore"]["teams"]["home"]["players"][i]:
                        playername = self.var['liveData']['boxscore']['teams']['home']['players'][i]['person']['fullName']
                        playerpos = self.var['liveData']['boxscore']['teams']['home']['players'][i]['position']['abbreviation']
                        batorder = self.var["liveData"]["boxscore"]["teams"]["home"]["players"][i]["battingOrder"]
                        teamdict[batorder] = f"{playername} {playerpos}"
                for d in sorted(teamdict.keys()):
                    if d != "100":
                        teamstring = f"{teamstring}\n"
                    if int(d)%100 == 0:
                        teamstring = f"{teamstring}{int(int(d)/100)} "
                    if int(d)%100:
                        teamstring = f"{teamstring}   \_"
                    teamstring = f"{teamstring}{teamdict[d]}"
                return teamstring
        else:
            return "Batting order not found."

 
    def print_pitchers(self, team_id):
        if self.game_state_code != "S" and self.game_state_code != "P" and self.game_state_code != "UNPOPULATED":
            if team_id == self.away_team_id:
                pitchers = {}
                pitchers = self.var["liveData"]["boxscore"]["teams"]["away"]["pitchers"]
                teamstring = ""
                increment = 0
                for i in pitchers:
                    if increment != 0:
                        teamstring = f"{teamstring}\n"
                    increment = 1
                    pitch_id = "ID" + str(i)
                    pitch_name = self.var['liveData']['boxscore']['teams']['away']['players'][pitch_id]['person']['fullName']
                    pitch_ip = self.var['liveData']['boxscore']['teams']['away']['players'][pitch_id]['stats']['pitching']['inningsPitched']
                    pitch_er = self.var['liveData']['boxscore']['teams']['away']['players'][pitch_id]['stats']['pitching']['earnedRuns']
#                    pitch_strikes = self.var['liveData']['boxscore']['teams']['away']['players'][pitch_id]['stats']['pitching']['strikes']
                    pitch_k = self.var['liveData']['boxscore']['teams']['away']['players'][pitch_id]['stats']['pitching']['strikeOuts']
#                    pitch_walk = self.var['liveData']['boxscore']['teams']['away']['players'][pitch_id]['stats']['pitching']['baseOnBalls']
                    teamstring = f"{teamstring}{pitch_name} ({pitch_ip} IP, {pitch_er} ER, {pitch_k} K)"
                    
                return teamstring
                    
        if team_id == self.home_team_id:
                pitchers = {}
                pitchers = self.var["liveData"]["boxscore"]["teams"]["home"]["pitchers"]
                teamstring = ""
                increment = 0
                for i in pitchers:
                    if increment != 0:
                        teamstring = f"{teamstring}\n"
                    increment = 1
                    pitch_id = "ID" + str(i)
                    pitch_name = self.var['liveData']['boxscore']['teams']['home']['players'][pitch_id]['person']['fullName']
                    pitch_ip = self.var['liveData']['boxscore']['teams']['home']['players'][pitch_id]['stats']['pitching']['inningsPitched']
                    pitch_er = self.var['liveData']['boxscore']['teams']['home']['players'][pitch_id]['stats']['pitching']['earnedRuns']
#                    pitch_strikes = self.var['liveData']['boxscore']['teams']['home']['players'][pitch_id]['stats']['pitching']['strikes']
                    pitch_k = self.var['liveData']['boxscore']['teams']['home']['players'][pitch_id]['stats']['pitching']['strikeOuts']
#                    pitch_walk = self.var['liveData']['boxscore']['teams']['home']['players'][pitch_id]['stats']['pitching']['baseOnBalls']
                    teamstring = f"{teamstring}{pitch_name} ({pitch_ip} IP, {pitch_er} ER, {pitch_k} K)"
                    
                return teamstring
        return "No data found."


    def print_bullpen(self, team_id):
        if self.game_state_code != "S" and self.game_state_code != "P" and self.game_state_code != "UNPOPULATED":
            if team_id == self.away_team_id:
                pitchers = {}
                pitchers = self.var["liveData"]["boxscore"]["teams"]["away"]["bullpen"]
                teamstring = ""
                increment = 0
                for i in pitchers:
                    if increment != 0:
                        teamstring = f"{teamstring}\n"
                    increment = 1
                    pitch_id = "ID" + str(i)
                    pitch_name = self.var['liveData']['boxscore']['teams']['away']['players'][pitch_id]['person']['fullName']
#                    pitch_ip = self.var['liveData']['boxscore']['teams']['away']['players'][pitch_id]['seasonStats']['pitching']['inningsPitched']
                    pitch_era = self.var['liveData']['boxscore']['teams']['away']['players'][pitch_id]['seasonStats']['pitching']['era']
#                    pitch_whip = self.var['liveData']['boxscore']['teams']['away']['players'][pitch_id]['seasonStats']['pitching']['whip']
#                    pitch_k_bb = self.var['liveData']['boxscore']['teams']['away']['players'][pitch_id]['seasonStats']['pitching']['strikeoutWalkRatio']
#                    teamstring = f"{teamstring}{pitch_name} ({pitch_era} ERA/{pitch_whip} WHIP/{pitch_k_bb} K:BB, {pitch_ip} IP)"
                    teamstring = f"{teamstring}{pitch_name} ({pitch_era} ERA)"
                    
                return teamstring
                    
        if team_id == self.home_team_id:
                pitchers = {}
                pitchers = self.var["liveData"]["boxscore"]["teams"]["home"]["bullpen"]
                teamstring = ""
                increment = 0
                for i in pitchers:
                    if increment != 0:
                        teamstring = f"{teamstring}\n"
                    increment = 1
                    pitch_id = "ID" + str(i)
                    pitch_name = self.var['liveData']['boxscore']['teams']['home']['players'][pitch_id]['person']['fullName']
#                    pitch_ip = self.var['liveData']['boxscore']['teams']['home']['players'][pitch_id]['seasonStats']['pitching']['inningsPitched']
                    pitch_era = self.var['liveData']['boxscore']['teams']['home']['players'][pitch_id]['seasonStats']['pitching']['era']
#                    pitch_whip = self.var['liveData']['boxscore']['teams']['home']['players'][pitch_id]['seasonStats']['pitching']['whip']
#                    pitch_k_bb = self.var['liveData']['boxscore']['teams']['home']['players'][pitch_id]['seasonStats']['pitching']['strikeoutWalkRatio']
#                    teamstring = f"{teamstring}{pitch_name} ({pitch_era} ERA/{pitch_whip} WHIP/{pitch_k_bb} K:BB, {pitch_ip} IP)"
                    teamstring = f"{teamstring}{pitch_name} ({pitch_era} ERA)"
                    
                return teamstring
        return "No data found."

    def print_bench(self, team_id):
        if self.abstract.lower() == "live":
            if team_id == self.away_team_id:
                bench = {}
                bench = self.var["liveData"]["boxscore"]["teams"]["away"]["bench"]
                teamstring = ""
                increment = 0
                if len(bench) <1 :
                    return "No players on bench."
                for i in bench:
                    if increment != 0:
                        teamstring = f"{teamstring}\n"
                    increment = 1
                    bench_id = "ID" + str(i)
                    bench_name = self.var['liveData']['boxscore']['teams']['away']['players'][bench_id]['person']['fullName']
                    bench_pos = self.var['liveData']['boxscore']['teams']['away']['players'][bench_id]['position']['abbreviation']
                    bench_avg = self.var['liveData']['boxscore']['teams']['away']['players'][bench_id]['seasonStats']['batting']['avg']
                    bench_obp = self.var['liveData']['boxscore']['teams']['away']['players'][bench_id]['seasonStats']['batting']['obp']
                    bench_slg = self.var['liveData']['boxscore']['teams']['away']['players'][bench_id]['seasonStats']['batting']['slg']
                    bench_ab = self.var['liveData']['boxscore']['teams']['away']['players'][bench_id]['seasonStats']['batting']['atBats']
                    teamstring = f"{teamstring}{bench_name} ({bench_pos}, {bench_avg}/{bench_obp}/{bench_slg}, {bench_ab} AB)"
                    
                return teamstring
                    
            if team_id == self.home_team_id:
                bench = {}
                bench = self.var["liveData"]["boxscore"]["teams"]["home"]["bench"]
                teamstring = ""
                increment = 0
                if len(bench) <1 :
                    return "No players on bench."
                for i in bench:
                    if increment != 0:
                        teamstring = f"{teamstring}\n"
                    increment = 1
                    bench_id = "ID" + str(i)
                    bench_name = self.var['liveData']['boxscore']['teams']['home']['players'][bench_id]['person']['fullName']
                    bench_pos = self.var['liveData']['boxscore']['teams']['home']['players'][bench_id]['position']['abbreviation']
                    bench_avg = self.var['liveData']['boxscore']['teams']['home']['players'][bench_id]['seasonStats']['batting']['avg']
                    bench_obp = self.var['liveData']['boxscore']['teams']['home']['players'][bench_id]['seasonStats']['batting']['obp']
                    bench_slg = self.var['liveData']['boxscore']['teams']['home']['players'][bench_id]['seasonStats']['batting']['slg']
                    bench_ab = self.var['liveData']['boxscore']['teams']['home']['players'][bench_id]['seasonStats']['batting']['atBats']
                    teamstring = f"{teamstring}{bench_name} ({bench_pos}, {bench_avg}/{bench_obp}/{bench_slg}, {bench_ab} AB)"
                                        
                return teamstring
        return "No data found."    

    def print_tv(self, team_id):
        if self.abstract == "Live":
            if team_id == self.away_team_id:
                info = f"{self.away_team} TV info:\n{self.away_tv}"
                return info
                    
            if team_id == self.home_team_id:
                info = f"{self.home_team} TV info:\n{self.home_tv}"
                return info
        return "No data found."    
    
    def print_pk(self):
        return str(self.gamePk)
        
    
    