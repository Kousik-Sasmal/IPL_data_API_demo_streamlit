import numpy as np
import pandas as pd
import ast

df_ball = pd.read_csv('notebooks/data/IPL_Ball_by_Ball_2008_2022.csv')
df_matches = pd.read_csv('notebooks/data/ipl-matches.csv')

df_matches['Team1Players'] = df_matches['Team1Players'].apply(lambda x: ast.literal_eval(x))
df_matches['Team2Players'] = df_matches['Team2Players'].apply(lambda x: ast.literal_eval(x))

# merging two dataframes `df_matches` and `df_ball`
ball_match = df_matches.merge(df_ball,on='ID')
ball_match['Date'] = pd.to_datetime(ball_match['Date'])


# Overall teams API
def total_teams():
    total_teams = df_ball['BattingTeam'].unique().tolist()
    return {'teams':total_teams}

# Overall bowlers API
def total_bowlers():
    total_bowlers = list(set(df_ball['bowler']))
    return {'bowlers':total_bowlers}

# Overall batsmans API
def total_batsmans():
    total_batsmans = list(set(df_ball['batter']))
    return {'batsmans':total_batsmans}

# API to retrieve year-wise team players
def team_players_yearwise(team_name: str, year: int):
    """
    Retrieves year-wise team players for a given team name and year.
    
    Args:
        team_name (str): The name of the team.
        year (int): The year for which team players are to be retrieved.
    
    Returns:
        dict: A dictionary containing the list of team players.
    """
    players = []
    # Retrieve team players for Team1 and Team2 matching the given team name and year
    for item in ball_match[(ball_match['Team1'] == team_name) & (ball_match['Date'].dt.year == year)]['Team1Players']:
        players.extend(item)

    for item in ball_match[(ball_match['Team2'] == team_name) & (ball_match['Date'].dt.year == year)]['Team2Players']:
        players.extend(item)

    players = list(set(players))
    return {'players': players}

# API for Team players till date
def teamwise_players_played(team_name):
    players = []
    for item in df_matches[df_matches['Team1']==team_name]['Team1Players']:
        players.extend(item)

    for item in df_matches[df_matches['Team2']==team_name]['Team2Players']:
        players.extend(item)

    players = list(set(players))
    return {'players':players}

# API for Number of Winnings of ANY team 
def number_of_winnings(team):
    temp_df = df_matches[(df_matches['Team1']==team) | (df_matches['Team2']==team)]
    total = len(temp_df)
    won = len(temp_df[temp_df['WinningTeam']==team])
    return {
        'total matches played':str(total),
        'number of winnings': str(won)
    }


# API for winning details of ALL team 
def winning_details_all_team():
    temp_series = df_matches['WinningTeam'].value_counts()
    winning_details = {'winning details of all teams': {key: str(value) for key, value in zip(temp_series.index, temp_series.values)}}
    return winning_details


# API for team-vs-team winning record
def team_vs_team(team1,team2):
    
    temp_df = df_matches[((df_matches['Team1']==team1) & (df_matches['Team2']==team2)) | (df_matches['Team1']==team2) & (df_matches['Team2']==team1)]

    total_matches = len(temp_df) 
    
    matches_won_team1 = sum(temp_df['WinningTeam']==team1)
    matches_won_team2 = sum(temp_df['WinningTeam']==team2)

    draws = total_matches - (matches_won_team1 + matches_won_team2)
    return {
        'total_matches': str(total_matches),
        'winnnings':{team1: str(matches_won_team1), team2: str(matches_won_team2)},
        'draws': str(draws)
    }


# create a function for bowler-run-record and wickets all together 
def bowler_record(bowler_name):
    
    # player of the match
    player_of_match_df = df_matches[df_matches['Player_of_Match'] == bowler_name]
    no_of_player_match = len(player_of_match_df)
    
    # how many matches played
    matchwise_teamplayer = df_matches['Team1Players'] + df_matches['Team2Players']
    match_count=0
    for player_list in matchwise_teamplayer:
        if bowler_name in player_list:
            match_count += 1
            
    temp_df = ball_match[ball_match['bowler'] == bowler_name]
    total_run_against_bowler = temp_df.groupby('ID').agg({'batsman_run':sum,'isWicketDelivery':sum})
    
    unique_combinations = temp_df[['ID','Date', 'BattingTeam']].drop_duplicates()

    bowler_run_record = unique_combinations.merge(total_run_against_bowler,on='ID')
    bowler_run_record['year'] = bowler_run_record['Date'].dt.year

    record = {}
    
    # Group the data by year
    grouped_by_year = bowler_run_record.groupby(bowler_run_record['year'])
    
    for year, group in grouped_by_year:
        record[str(year)] = {}
        group_by_team = group.groupby('BattingTeam')
        
        for team, team_group in group_by_team:
            record[str(year)][team] = {}
            group_by_date = team_group.groupby('Date')
            
            for date, date_group in group_by_date:
                total_runs = date_group['batsman_run'].sum()
                total_wickets = date_group['isWicketDelivery'].sum()
                
                record[str(year)][team][str(date.date())] = {
                    'runs': str(total_runs),
                    'wickets': str(total_wickets)
                }
    
    return {
        'overall summary':{
            'total matches played':str(match_count),
            'total wickets':str(total_run_against_bowler['isWicketDelivery'].sum()),
            'total Player of Match': str(no_of_player_match),
            'maximum runs conceded':str(bowler_run_record['batsman_run'].max()),
            'minimum runs conceded':str(bowler_run_record['batsman_run'].min()),
            'average runs conceded':str(round(bowler_run_record['batsman_run'].mean(),2))
        },
        
        'matchwise summary':record
    }


# create a function for batsman-run-record and boundaries all together 
def batsman_record(batsman_name):
    
    # player of the match
    player_of_match_df = df_matches[df_matches['Player_of_Match'] == batsman_name]
    no_of_player_match = len(player_of_match_df)
    
    # how many matches played
    matchwise_teamplayer = df_matches['Team1Players'] + df_matches['Team2Players']
    match_count=0
    for player_list in matchwise_teamplayer:
        if batsman_name in player_list:
            match_count += 1
    
    temp_df = ball_match[ball_match['batter'] == batsman_name]
    
    # fours-sixes details
    fours_df = temp_df[temp_df['batsman_run']==4]
    six_df = temp_df[temp_df['batsman_run']==6]
    
    temp_df['is_four'] = np.where(temp_df['batsman_run']==4, 1, 0)
    temp_df['is_six'] = np.where(temp_df['batsman_run']==6, 1, 0)

    total_run_by_batsman = temp_df.groupby('ID').agg({'batsman_run':sum,'is_six':sum,'is_four':sum})
    
    unique_combinations = temp_df[['ID','Date', 'BattingTeam']].drop_duplicates()
    
    batsman_run_record = unique_combinations.merge(total_run_by_batsman, on='ID')
    batsman_run_record['year'] = batsman_run_record['Date'].dt.year
    
    record = {}
    
    grouped_by_year = batsman_run_record.groupby('year')
    
    for year, group in grouped_by_year:
        record[str(year)] = {}
        group_by_team = group.groupby('BattingTeam')
        
        for team, team_group in group_by_team:
            record[str(year)][team] = {}
            group_by_date = team_group.groupby('Date')
            
            for date, date_group in group_by_date:
                total_runs = date_group['batsman_run'].sum()
                match_fours = date_group['is_four'].sum()
                match_six = date_group['is_six'].sum()
            
                record[str(year)][team][str(date.date())] = {
                    'runs': str(total_runs),
                    'fours': str(match_fours),
                    'sixes': str(match_six)
                }
                
    return {
        'overall summary':{
            'total matches played':str(match_count),
            'total runs':str(batsman_run_record['batsman_run'].sum()),
            'total Player of Match': str(no_of_player_match),
            'maximum runs':str(batsman_run_record['batsman_run'].max()),
            'minimum runs':str(batsman_run_record['batsman_run'].min()),
            'average runs':str(round(batsman_run_record['batsman_run'].mean(), 2)),
            'fours': str(len(fours_df)),
            'sixes': str(len(six_df))
        },
        
        'matchwise summary':record
    }


# API for team-record
def team_record(given_team):
    
    # winning history of the team
    all_teams = list(set(ball_match['BattingTeam']))
    winning_hist = number_of_winnings(given_team)
    
    # winning history of the team in final match
    final_temp_df = df_matches[df_matches['MatchNumber'] == 'Final']
    final_match_df = final_temp_df[(final_temp_df['Team1'] == given_team) | (final_temp_df['Team2'] == given_team)]
    
    total_final_match = len(final_match_df)
    winnings_in_final_match = sum(final_match_df['WinningTeam']==given_team)
    
    winning_hist['total final matches played'] = str(total_final_match)
    winning_hist['number of final match winnings'] = str(winnings_in_final_match)
    
    record = {}
    for other_team in all_teams:
        if other_team != given_team:
            record[str(other_team)] = team_vs_team(given_team,other_team)
            
    return {
        'overall summary':winning_hist,
        'teamwise summary':record
    }


# API for top bowlers yearwise
def top_bowler_yearwise(year: int, top_k: int = 1):
    """
    Returns the top bowlers and their corresponding wickets in a given year.
    
    Args:
        year (int): The year for which the top bowlers are to be determined.
        top_k (int, optional): The number of top bowlers to be returned. Defaults to 1.
        
    Returns:
        dict: A dictionary containing the top bowlers and their wickets.
    """
    temp_df = ball_match[
        (ball_match['Date'].dt.year == year) &
        (ball_match['kind'] != 'run out') &
        (ball_match['kind'] != 'hit wicket') &
        (ball_match['kind'] != 'obstructing the field') &
        (ball_match['kind'] != 'retired hurt') &
        (ball_match['kind'] != 'retired out')
    ]
    
    top_bowler_group = temp_df.groupby('bowler')['isWicketDelivery']
    bowlers = list(top_bowler_group.sum().sort_values(ascending=False).index[:top_k])
    wickets = list(top_bowler_group.sum().sort_values(ascending=False).values[:top_k])

    result = [{bowlers[i]: str(wickets[i])} for i in range(len(bowlers))]
    return {
        'top_bowlers': result
    }


# API for top batsman yearwise
def top_batsman_yearwise(year: int, top_k: int = 1):
    """
    Returns the top batsmen and their respective runs for a given year.
    
    Args:
        year (int): The year for which the data is to be retrieved.
        top_k (int, optional): The number of top batsmen to return. Defaults to 1.
    
    Returns:
        dict: A dictionary containing the top batsmen and their respective runs.
    """
    temp_df = ball_match[ball_match['Date'].dt.year == year]
    top_batsman_group = temp_df.groupby('batter')['batsman_run']
    
    batsmans = list(top_batsman_group.sum().sort_values(ascending=False).index[:top_k])
    runs = list(top_batsman_group.sum().sort_values(ascending=False).values[:top_k])
    
    result = [{batsmans[i]: str(runs[i])} for i in range(len(batsmans))]
    return {
        'top_batsmans': result
    }
