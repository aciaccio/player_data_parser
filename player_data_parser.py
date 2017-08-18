import csv
import re
import datetime
import sys

class GameInfo:
    def __init__(self, id, date):
        self.id = id
        self.date = date

class GameEvent:
    
    def __init__(self, id, game_id, event_type, yards, opponent_name, player_id, touchdown):
        self.id = id
        self.game_id = game_id
        self.event_type = event_type
        self.yards = yards
        self.opponent_name = opponent_name
        self.player_id = player_id
        self.touchdown = touchdown

class PlayerInfo:

    def __init__(self, id, name, team_name):
        self.id = id
        self.name = name
        self.team_name = team_name

def parse_game_event(event, game_info_set, game_event_list, player_set):

    #print('parsing data for game_id: ' + event['GameId'])
    #print('is event rush?: ' + event['IsRush'])
    #print('is event pass?: ' + event['IsPass'])

    #For touchdown check 'IsTouchdown' field
    touchdown = event['IsTouchdown']

    if event['IsRush'] == '1':
        to_parse = event['Description']

        #Rush events are of the form:
        #(13:19) (SHOTGUN) 29-J.FORSETT RIGHT GUARD TO CLE 28 FOR 2 YARDS (90-E.OGBAH).
        
        #Player name is first 1-2 numbers followed by a dash(-)
        #m = re.search('(?<=-)\w+', 'spam-egg')
        #m.group(0)
        player_name_block = re.search('[0-9]+-[a-zA-Z]+\.[ \w-]+\.?[ \w-]+FOR',to_parse)
        player_name = re.search('\w\.\w+', player_name_block.group(0)).group(0)

        #Player id is TEAM-#-player_name
        player_number = re.search('[0-9]+-', player_name_block.group(0)).group(0)
        player_id = event['OffenseTeam'] + '-' + player_number + player_name

        #Number of yards is followed by the string 'YARD'
        searched_result = re.search('FOR -?[0-9]+ YARD', to_parse)
        rush_yards = '0'
        if searched_result:
            rush_yards = re.search('-?[0-9]+', searched_result.group(0)).group(0)

        game_event_list.append(GameEvent(len(game_event_list), event['GameId'], 1, rush_yards, event['DefenseTeam'], player_id, touchdown))
        player_set.add(PlayerInfo(player_id, player_name, event['OffenseTeam']))
        game_info_set.add(GameInfo(len(game_info_set), event['GameDate']))
   
    elif event['IsPass'] == '1' and event['IsIncomplete'] == '0':
        to_parse = event['Description']

        #Pass events are of the form:
        #(3:30) (SHOTGUN) 12-T.BRADY PASS SHORT RIGHT TO 11-J.EDELMAN TO NYJ 37 FOR 6 YARDS (45-R.MILES).
        #This means that 2 players get updated, the QB and the receiver

        #QB name is first 1-2 numbers followed by a dash(-)
        #Player name is first 1-2 numbers followed by a dash(-)
        #m = re.search('(?<=-)\w+', 'spam-egg')
        #m.group(0)
        qb_name = re.search('(?<=[0-9]-)\w\.\w+',to_parse).group(0)
        qb_number = re.search('[0-9]+-', to_parse).group(0)
        qb_player_id = event['OffenseTeam'] + '-' + qb_number + qb_name

        #WR name is next 1-2 numbers followed by a dash(-)
        receiver_name = re.search('(?<=[0-9]-)\w\.\w+',to_parse).group(0)
        receiver_number = re.search('[0-9]-', to_parse).group(0)
        receiver_player_id = event['OffenseTeam'] + '-' + receiver_number + receiver_name

        #Number of yards is followed by the string 'YARD'
        searched_result = re.search('FOR -?[0-9]+ YARD', to_parse)
        receiving_yards = '0'
        passing_yards = '0'
        if searched_result:
            passing_yards = re.search('-?[0-9]+', searched_result.group(0)).group(0)
            receiving_yards = passing_yards

        game_event_id = len(game_event_list)
        game_event_list.append(GameEvent(game_event_id, event['GameId'], 2, receiving_yards, event['DefenseTeam'], receiver_player_id, touchdown))
        game_event_list.append(GameEvent(game_event_id, event['GameId'], 3, passing_yards, event['DefenseTeam'], qb_player_id, touchdown))

        player_set.add(PlayerInfo(qb_player_id, qb_name, event['OffenseTeam']))
        player_set.add(PlayerInfo(receiver_player_id, receiver_name, event['OffenseTeam']))

        game_info_set.add(GameInfo(len(game_info_set), event['GameDate']))

def main():
    
    print ("Parsing player data from file: " + sys.argv[1])
    with open(sys.argv[1], 'r') as csvfile:
        fieldnames = ['GameId','GameDate','Quarter','Minute','Second','OffenseTeam','DefenseTeam','Down','ToGo','YardLine','SeriesFirstDown','NextScore','Description','TeamWin','SeasonYear','Yards','Formation','PlayType','IsRush','IsPass','IsIncomplete','IsTouchdown','PassType','IsSack','IsChallenge','IsChallengeReversed','Challenger','IsMeasurement','IsInterception','IsFumble','IsPenalty','IsTwoPointConversion','IsTwoPointConversionSuccessful','RushDirection','YardLineFixed','YardLineDirection','IsPenaltyAccepted','PenaltyTeam','IsNoPlay','PenaltyType','PenaltyYards']
        reader = csv.DictReader(csvfile, fieldnames=fieldnames)

        game_info_set = set()
        player_set = set()
        game_event_list = []

        for event in reader:
            parse_game_event(event, game_info_set, game_event_list, player_set)

        rush_yards = 0
        touchdowns = 0

        print('finished parsing game events')

        for parsed_event in game_event_list:
            if parsed_event.player_id == 'NO-9-D.BREES' and parsed_event.event_type == 3:
                rush_yards = rush_yards + int(parsed_event.yards)
                touchdowns = touchdowns + int(parsed_event.touchdown)

        print('pass yards for d.brees: ' + str(rush_yards))
        print('touchdowns for d.brees: ' + str(touchdowns))
                
if __name__ == '__main__':
  main()
    



