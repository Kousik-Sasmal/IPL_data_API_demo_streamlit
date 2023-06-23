import streamlit as st
import analysis
from analysis import df_ball,df_matches,ball_match

st.set_page_config(page_title='IPL Analysis',layout='wide')
st.title('IPL Data Analysis')
st.markdown('This is demo APP for API services of IPL data analysis')



st.sidebar.title('IPL Data Analysis')
option = st.sidebar.selectbox('Select the API',['Overall teams','Overall bowlers','Overall batsmans',
                                                'Team players','Team players played till date',
                                                'Overall winning details','Teamwise winning details',
                                                'Team vs Team winning details','Top bowlers Season-wise',
                                                'Top batsmans Season-wise','Bowler record',
                                                'Batsman record','Team record'])
                                                
if option=='Overall teams':
    st.header('Overall teams')
    response = analysis.total_teams()
    st.write(response)

elif option=='Overall bowlers':
    st.header('Overall bowlers')
    response = analysis.total_bowlers()
    st.write(response)

elif option=='Overall batsmans':
    st.header('Overall batsmans')
    response = analysis.total_batsmans()
    st.write(response)

elif option=='Team players':
    st.header('Team players season-wise')
    team = st.selectbox('Select the Team',list(set(df_ball['BattingTeam'])))
    year = st.selectbox('Select the Season',list(range(2008,2023)))
    response = analysis.team_players_yearwise(team,year)
    st.write(response)

elif option=='Team players played till date':
    st.header('Team players played till date')
    team = st.selectbox('Select the Team',list(set(df_ball['BattingTeam'])))
    response = analysis.teamwise_players_played(team)
    st.write(response)

elif option=='Overall winning details':
    st.header('Overall winning details')
    response = analysis.winning_details_all_team()
    st.write(response)

elif option=='Teamwise winning details':
    st.header('Teamwise winning details')
    team = st.selectbox('Select the Team',list(set(df_ball['BattingTeam'])))
    response = analysis.number_of_winnings(team)
    st.write(response)

elif option=='Team vs Team winning details':
    st.header('Team vs Team winning details')
    team1 = st.selectbox('Select the Team 1',list(set(df_ball['BattingTeam'])))
    team2 = st.selectbox('Select the Team 2',list(set(df_ball['BattingTeam'])))
    response = analysis.team_vs_team(team1,team2)
    st.write(response)

elif option=='Top bowlers Season-wise':
    st.header('Top bowlers Season-wise')
    year = st.selectbox('Select the Season',list(range(2008,2023)))
    n = st.selectbox('Select the number of top bowlers',list(range(5,25,5)))
    response = analysis.top_bowler_yearwise(year,top_k=n)
    st.write(response)

elif option=='Top batsmans Season-wise':
    st.header('Top batsmans Season-wise')
    year = st.selectbox('Select the Season',list(range(2008,2023)))
    n = st.selectbox('Select the number of top batsmans',list(range(5,25,5)))
    response = analysis.top_batsman_yearwise(year,top_k=n)
    st.write(response)

elif option=='Bowler record':
    st.header('Bowler Record')
    bowler = st.selectbox('Select the Bowler',list(set(df_ball['bowler'])))
    response = analysis.bowler_record(bowler)
    st.write(response)

elif option=='Batsman record':
    st.header('Batsman Record')
    batsman = st.selectbox('Select the Bowler',list(set(df_ball['batter'])))
    response = analysis.batsman_record(batsman)
    st.write(response)

elif option=='Team record':
    st.header('Team record')
    team = st.selectbox('Select the Team',list(set(df_ball['BattingTeam'])))
    response = analysis.team_record(team)
    st.write(response)

