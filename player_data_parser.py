import csv
import re

class GameEvent:
    
    def __init__(self):
        self.id = 0
        self.game_id = 0
        self.rush_yards = 0
        self.receiving_yards = 0
        self.receptions = 0
        self.passing_yards = 0
        self.opponent_name = ''
        self.team_name = ''
        self.player_name = ''
        self.player_id = ''
        self.touchdown = 0


class Player:

    def __init__(self):
        self.name = ''
        
        

with open('player_data.csv', 'r') as csvfile:
    fieldnames = ['Minute','Second','OffenseTeam','DefenseTeam','Down','ToGo','YardLine','SeriesFirstDown','NextScore','Description','TeamWin','SeasonYear','Yards','Formation','PlayType','IsRush','IsPass','IsIncomplete','IsTouchdown','PassType','IsSack','IsChallenge','IsChallengeReversed','Challenger','IsMeasurement','IsInterception','IsFumble','IsPenalty','IsTwoPointConversion','IsTwoPointConversionSuccessful','RushDirection','YardLineFixed','YardLineDirection','IsPenaltyAccepted','PenaltyTeam','IsNoPlay','PenaltyType','PenaltyYards']
    reader = csv.DictReader(csvfile, fieldnames=fieldnames)

    

def parse_game_event(event):

    if(event['IsRush'] = '1'):
        #Rush events are of the form:
        #(13:19) (SHOTGUN) 29-J.FORSETT RIGHT GUARD TO CLE 28 FOR 2 YARDS (90-E.OGBAH).

        to_parse = event['Description']
        
        #Player name is first 1-2 numbers followed by a dash(-)
        #m = re.search('(?<=-)\w+', 'spam-egg')
        #m.group(0)
        player_name = re.search('(?<=[0-9]+-)\w+',to_parse).group(0)

        #Player id is TEAM-#-player_name
        player_number = re.search('[0-9]+-', to_parse).group(0)
        player_id = event['OffenseTeam'] + player_number + player_name

        #Number of yards is followed by the string 'YARDS'
        yards_statement = re.search('FOR [0-9]+ YARDS', to_parse).group(0)
        rush_yards = re.search('[0-9]+', yards_statement).group(0)

   
    else if(event['IsPass'] = '1'):
        #Pass events are of the form:
        #(3:30) (SHOTGUN) 12-T.BRADY PASS SHORT RIGHT TO 11-J.EDELMAN TO NYJ 37 FOR 6 YARDS (45-R.MILES).
        #This means that 2 players get updated, the QB and the receiver

        to_parse = event['Description']

        #QB name is first 1-2 numbers followed by a dash(-)
        #Player name is first 1-2 numbers followed by a dash(-)
        #m = re.search('(?<=-)\w+', 'spam-egg')
        #m.group(0)
        qb_name = re.search('(?<=[0-9]+-)\w+',to_parse).group(0)

        #WR name is next 1-2 numbers followed by a dash(-)
        receiver_name = re.search('(?<=[0-9]+-)\w+',to_parse).group(1)
        
        #Number of yards is followed by the string 'YARDS'
        yards_statement = re.search('FOR [0-9]+ YARDS', to_parse).group(0)
        receiving_yards = re.search('[0-9]+', yards_statement).group(0)
        passing_yards = receiving_yards
        
    #For touchdown check 'IsTouchdown' field
    touchdown = event['IsTouchdown']





