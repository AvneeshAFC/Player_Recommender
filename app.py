import streamlit as st
import pandas as pd
import numpy as np
import time


header = st.beta_container()
params = st.beta_container()
result = st.beta_container()

with header:
    st.title('Player Recommender Tool')
    st.text('Based on the 2020/21 season data for the Big 5 European leagues.')

with params:
    st.header('Tweak the parameters')
    # st.text('Choose the player name, type, leagues to get recommendation from, age bracket and \nthe number of results.')
    
    col1, col2 = st.beta_columns([1, 2])
    with col1:
        st.radio('Player type', ['Outfield players', 'Goal Keepers'])    
    with col2:    
        st.selectbox('Player name', ['Messi', 'Ronaldo', 'Ozil'])


    col3, col4 = st.beta_columns([1, 2])
    with col3:
        st.selectbox('League', ['All', 'Premier League', 'La Liga', 'Serie A', 'Bundesliga', 'Ligue 1'],
            help='Leagues to get recommendations from. All 5 leagues by default.')
    with col4:
        lower, upper = st.slider('Age bracket', min_value=15, max_value=42, value=(15, 42), 
        help='Age range to get recommendations from. Drag the sliders on either side. All ages by default.')
    

    col5, col6 = st.beta_columns([1, 1])
    with col5:
        st.slider('Number of results', min_value=5, max_value=30, value=10, step=5)
    with col6:
        with st.spinner(text='running recommendation engine'):
            time.sleep(1.25)
            st.success('Done')
    