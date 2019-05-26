import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import operator
import math
import pandas as pd
import os

datadir = "\\datadir"

with open("matchinfo.txt", "w") as matchinfo_file:
    matchinfo_file.write("team1"+"\t"+"team2"+"\t"+"season"+"\t"+"venue"+"\t"+"match_number"+"\t"+"toss_won"+"\t"+"decision"+"\t"+"winner"+"\t"+"batting_first"+"\t"+"batting_second"+"\t"+ "match_id"+ "\t"+ "match_finish"+"\n")

fileslist = []

for file in os.listdir(datadir):
    if file.endswith(".csv"):
        fileslist.append(file)
master_list = []
for file in fileslist:
    with open(os.path.join(datadir, file), "r") as iplfile:
        results = [line.replace("\n", "").split(",") for line in iplfile.readlines()]
    match_dict = {}
    match_dict['team1'] = results[1][2]
    match_dict['team2'] = results[2][2]
    ball_start = 0
    #to check we've atleast some play happened for the match and create a dictionary with match info
    if len(results) >= 25:
        for m in range(3, 25):
            if results[m][0] == "info":
                match_dict[results[m][1]] = results[m][2]
            else:
                if ball_start == 0: ball_start = m
        match_finish = 'Y'
        if 'method' in match_dict: match_finish = match_dict['method']
        team1 = match_dict['team1']
        team2 = match_dict['team2']
        season_split = match_dict['season'].split("/")
        season = int(season_split[0]) + 1 if len(season_split) > 1 else season_split[0]
        city = match_dict['city']
        match_num = match_dict.get('match_number', match_dict['date'].replace('-', ''))
        toss = match_dict['toss_winner']
        decision = match_dict['toss_decision']
        winner = match_dict.get('winner', 'NA')
        if 'eliminator' in match_dict:
            winner = match_dict.get('eliminator', 'NA')
        batting_first = results[ball_start][3]
        batting_second = team1 if batting_first == team2 else team2
        #write match info file..
        with open("matchinfo.txt", "a") as frsfile:
            frsfile.write(team1 + "\t" + team2 + "\t" +str(season) + "\t" + city + "\t" + str(match_num) + "\t" +toss + "\t" +decision + "\t" +winner + "\t" +batting_first + "\t" +batting_second + "\t" + file.replace(".csv","") +  "\t" + match_finish.replace("\\","") + "\n")
        overs_list = []
        for r in range(ball_start,len(results)):
            result = results[r]
            temp_list = []
            team_name = result[3]
            opp_team = batting_second if team_name == batting_first else batting_first
            temp_list.append(team_name)
            temp_list.append(opp_team)
            #handle super overs
            if int(result[1]) == 3 or int(result[1]) == 4:
                temp_list.append(math.floor(float(result[2]) + 21))
            else:
                temp_list.append(math.floor(float(result[2]) + 1))
            temp_list.append(int(result[7]))
            temp_list.append(int(result[8]))
            wicket = 0
            if result[9] != "" and len(result[9]) > 2:
                wicket = 1
            temp_list.append(wicket)
            temp_list.append(1)
            overs_list.append(temp_list)
        df = pd.DataFrame(overs_list, columns =['batting_team','bowling_team', 'over','runs','extras','wicket','balls'])
        dfpd = df.groupby(['over', 'batting_team','bowling_team'], as_index = False)['runs','extras','wicket','balls'].sum()
        dfpd['season'] = season
        dfpd['match_num'] = match_num
        #dfpd['ball_start'] = ball_start
        dfpd['match_id'] = file.replace(".csv","")
        master_list_values = dfpd.values.tolist()
        for mm in range(len(master_list_values)):
            master_list.append(master_list_values[mm])
dff = pd.DataFrame(master_list, columns =['over','batting_team','bowling_team','runs','extras','wicket', 'balls','season', 'match_num','match_id'])
dff.to_csv("detailed.csv")

