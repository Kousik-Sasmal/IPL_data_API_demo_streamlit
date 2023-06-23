import streamlit as st
import analysis
from analysis import df_ball,df_matches,ball_match

st.set_page_config(page_title='IPL Analysis',layout='wide')
st.title('Documentation for API services of IPL data analysis')
st.markdown('Upto 2022 IPL Season')

option = st.selectbox('Select an API',['Overall teams','Overall bowlers','Overall batsmans',
                                                'Team players','Team players played till date',
                                                'Overall winning details','Teamwise winning details',
                                                'Team vs Team winning details','Top bowlers Season-wise',
                                                'Top batsmans Season-wise','Bowler record',
                                                'Batsman record','Team record'])
                                                
if option=='Overall teams':
    st.header('Overall teams')
    code = """#Python
import requests
API_URL =  "https://kousiksasmal.pythonanywhere.com/api/teams"
response = requests.get(API_URL)
response.json()"""
    st.code(code, language='python')

    response = analysis.total_teams()
    st.write(response)


elif option=='Overall bowlers':
    st.header('Overall bowlers')
    code = """#Python
import requests
API_URL =  "https://kousiksasmal.pythonanywhere.com/api/bowlers"
response = requests.get(API_URL)
response.json()"""
    st.code(code, language='python')

    response = analysis.total_bowlers()
    st.write(response)


elif option=='Overall batsmans':
    st.header('Overall batsmans')
    code = """#Python
import requests
API_URL =  "https://kousiksasmal.pythonanywhere.com/api/batsmans"
response = requests.get(API_URL)
response.json()"""
    st.code(code, language='python')

    response = analysis.total_batsmans()
    st.write(response)


elif option=='Team players':
    st.header('Team players season-wise')
    code = """#Python
import requests
API_URL =  "https://kousiksasmal.pythonanywhere.com/api/seasonwise-teamplayers?team=Kolkata Knight Riders&season=2020"
response = requests.get(API_URL)
response.json()"""
    st.code(code, language='python')

    team = st.selectbox('Select the Team',list(set(df_ball['BattingTeam'])))
    year = st.selectbox('Select the Season',list(range(2008,2023)))
    response = analysis.team_players_yearwise(team,year)
    st.write(response)


elif option=='Team players played till date':
    st.header('Team players played till date')
    code = """#Python
import requests
API_URL =  "https://kousiksasmal.pythonanywhere.com/api/teamwise-players?team=Kolkata Knight Riders"
response = requests.get(API_URL)
response.json()"""
    st.code(code, language='python')

    team = st.selectbox('Select the Team',list(set(df_ball['BattingTeam'])))
    response = analysis.teamwise_players_played(team)
    st.write(response)


elif option=='Overall winning details':
    st.header('Overall winning details')
    code = """#Python
import requests
API_URL =  "https://kousiksasmal.pythonanywhere.com/api/overall-winnings"
response = requests.get(API_URL)
response.json()"""
    st.code(code, language='python')
    
    response = analysis.winning_details_all_team()
    st.write(response)


elif option=='Teamwise winning details':
    st.header('Teamwise winning details')
    code = """#Python
import requests
API_URL =  "https://kousiksasmal.pythonanywhere.com/api/teamwise-winnings?team=Kolkata Knight Riders"
response = requests.get(API_URL)
response.json()"""
    st.code(code, language='python')

    team = st.selectbox('Select the Team',list(set(df_ball['BattingTeam'])))
    response = analysis.number_of_winnings(team)
    st.write(response)


elif option=='Team vs Team winning details':
    st.header('Team vs Team winning details')
    code = """#Python
import requests
API_URL =  "https://kousiksasmal.pythonanywhere.com/api/teamvsteam-winnings?team1=Rajasthan Royals&team2=Kolkata Knight Riders"
response = requests.get(API_URL)
response.json()"""
    st.code(code, language='python')

    team1 = st.selectbox('Select the Team 1',list(set(df_ball['BattingTeam'])))
    team2 = st.selectbox('Select the Team 2',list(set(df_ball['BattingTeam'])))
    response = analysis.team_vs_team(team1,team2)
    st.write(response)


elif option=='Top bowlers Season-wise':
    st.header('Top bowlers Season-wise')
    code = """#Python
import requests
API_URL =  "https://kousiksasmal.pythonanywhere.com/api/top-bowlers?season=2008&n=5"
response = requests.get(API_URL)
response.json()"""
    st.code(code, language='python')

    year = st.selectbox('Select the Season',list(range(2008,2023)))
    n = st.selectbox('Select the number of top bowlers',list(range(5,25,5)))
    response = analysis.top_bowler_yearwise(year,top_k=n)
    st.write(response)


elif option=='Top batsmans Season-wise':
    st.header('Top batsmans Season-wise')
    code = """#Python
import requests
API_URL =  "https://kousiksasmal.pythonanywhere.com/api/top-batsmans?season=2008&n=5"
response = requests.get(API_URL)
response.json()"""
    st.code(code, language='python')

    year = st.selectbox('Select the Season',list(range(2008,2023)))
    n = st.selectbox('Select the number of top batsmans',list(range(5,25,5)))
    response = analysis.top_batsman_yearwise(year,top_k=n)
    st.write(response)


elif option=='Bowler record':
    st.header('Bowler Record')
    code = """#Python
import requests
API_URL =  "https://kousiksasmal.pythonanywhere.com/api/bowler-record?bowler=JJ Bumrah"
response = requests.get(API_URL)
response.json()"""
    st.code(code, language='python')

    bowler = st.selectbox('Select the Bowler',list(set(df_ball['bowler'])))
    response = analysis.bowler_record(bowler)
    st.write(response)


elif option=='Batsman record':
    st.header('Batsman Record')
    code = """#Python
import requests
API_URL =  "https://kousiksasmal.pythonanywhere.com/api/batsman-record?batsman=MS Dhoni"
response = requests.get(API_URL)
response.json()"""
    st.code(code, language='python')

    batsman = st.selectbox('Select the Bowler',list(set(df_ball['batter'])))
    response = analysis.batsman_record(batsman)
    st.write(response)


elif option=='Team record':
    st.header('Team record')
    code = """#Python
import requests
API_URL =  "https://kousiksasmal.pythonanywhere.com/api/team-record?team=Chennai Super Kings"
response = requests.get(API_URL)
response.json()"""
    st.code(code, language='python')

    team = st.selectbox('Select the Team',list(set(df_ball['BattingTeam'])))
    response = analysis.team_record(team)
    st.write(response)

