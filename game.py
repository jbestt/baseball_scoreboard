import data

class Game:
    def __init__(self, scoreboarddata):
        self.var = scoreboarddata
        if "messageNumber" in scoreboarddata or "message" in scoreboarddata:
            print("Data unavailable.")
        else:
            print("game on!")
        
        self.gamePk = self.var["gamePk"]
        self.home_team = self.var["gameData"]["teams"]["home"]["teamName"]
        self.home_team_abbreviation = self.var["gameData"]["teams"]["home"]["abbreviation"]  
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

        if self.game_state_code != "S":
            self.home_challenges_used = self.var["gameData"]["review"]["home"]["used"]
            self.home_challenges_remaining = self.var["gameData"]["review"]["home"]["remaining"]
            self.away_challenges_used = self.var["gameData"]["review"]["away"]["used"]
            self.away_challenges_remaining = self.var["gameData"]["review"]["away"]["remaining"]
            self.inning = self.var["liveData"]["linescore"]["currentInning"]
            self.inning_ordinal = self.var["liveData"]["linescore"]["currentInningOrdinal"]
            self.inning_state = self.var["liveData"]["linescore"]["inningState"]
            
        
        
    def game_info(self):
        if self.game_state_code == "S" or self.game_state_code == "P":
            return self.print_preview()
        elif self.game_state_code == "F" or self.game_state_code == "O":
            return self.print_final()
        elif self.game_state_code == "I":
            return self.print_live_status()
        else:
            return "Data unavailable."

    def print_preview(self):
        if self.game_state_code == "S" or self.game_state_code == "P":
            return f"{self.start_time_formatted}: {self.away_team} ({self.away_team_wins}-{self.away_team_losses}) @ {self.home_team} ({self.home_team_wins}-{self.home_team_losses})"
        return "Data unavailable."
        
    def print_live_status(self):
        current_score = f"{self.away_team} {self.away_score} - {self.home_team} {self.home_score}"
        inning_info = f"{self.inning_state} of the {self.inning_ordinal}"
        outs_balls_strikes = ""
        if self.inning_state == "Top" or self.inning_state == "Bottom":
            outs_balls_strikes = f"\nOuts Balls Strikes"
        
        return f"Game in progress.\n{current_score}\n{inning_info}{outs_balls_strikes}"
            
        
        
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
        if self.game_state_code != "S":
            return f"Challenges (Team: Used - Remaining):\n{self.away_team}: {self.away_challenges_used} - {self.away_challenges_remaining}\n{self.home_team}: {self.home_challenges_used} - {self.home_challenges_remaining}"
        else:
            return "Data unavailable."
    
    
    
    
    
    