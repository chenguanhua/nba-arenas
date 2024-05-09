import folium
import streamlit as st
import pandas as pd
from nba_api.stats.static import teams
from nba_api.stats.endpoints import commonteamroster, teamestimatedmetrics

from streamlit_folium import st_folium
from pathlib import Path

nba_teams = pd.DataFrame(teams.get_teams())

path = Path(__file__).parent / "nba_team_arena.csv"

df = pd.read_csv(path)

m = folium.Map(location=[39.8283, -98.5795], zoom_start=4)

for i, row in df.iterrows():
    lat, lng = row['latitude'], row['longitude']
    info = f"<strong>Team: </strong>{row['team name']}\nArena: {row['stadium']}"
    folium.Marker(
        [lat, lng],
        # popup = info,
        tooltip = info
    ).add_to(m)

output = st_folium(
        m, width=700, height=500)

# st.markdown(output)
last_obj = output['last_object_clicked']
last = output['last_clicked']

# st.markdown((last, last_obj))
if last_obj:
    teams = df[df['latitude']==last_obj['lat']]
    st.markdown('Team: ')
    st.dataframe(teams)
    for i, row in teams.iterrows():
        mask = nba_teams['full_name'] == row['team name']
        id = nba_teams[mask]['id'].values[0]

        team_stats = teamestimatedmetrics.TeamEstimatedMetrics().get_data_frames()[0]
        st.markdown(f'{row["team name"]} Stats: ')
        st.dataframe(team_stats[team_stats['TEAM_ID']==id])

        info = commonteamroster.CommonTeamRoster(id)
        roster = info.get_data_frames()[0]
        st.markdown(f'{row["team name"]} Roster: ')
        st.dataframe(roster)