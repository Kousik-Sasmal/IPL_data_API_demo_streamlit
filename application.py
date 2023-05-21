import streamlit as st
import analysis
from analysis import df_ball,df_matches,ball_match

st.set_page_config(page_title='IPL Analysis')
st.title('IPL Data Analysis')
st.markdown('This is a demo APP for API services of IPL data (till 2022) analysis')

option = st.selectbox('Select the API',['Overall teams','Overall bowlers','Overall batsmans',
                                                'Teamwise players','Overall winning details',
                                                'Teamwise winning details','Team vs Team winning details',
                                                'Bowler record','Batsman record','Team record'])

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

elif option=='Teamwise players':
    st.header('Teamwise players')
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
    team1 = st.selectbox('Select Team 1',list(set(df_ball['BattingTeam'])))
    team2 = st.selectbox('Select Team 2',list(set(df_ball['BattingTeam'])))
    response = analysis.team_vs_team(team1,team2)
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