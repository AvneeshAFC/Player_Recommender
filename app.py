import streamlit as st
import pandas as pd
import numpy as np
import pickle
import time


@st.cache(show_spinner=False)
def getData():
    # loading outfield players pickles
    player_df = pd.read_pickle(r'Data\outfield.pkl')
    with open(r'Data\player_ID.pickle', 'rb') as file:
        player_ID = pickle.load(file)
    with open(r'Data\engine.pickle', 'rb') as file:
        engine = pickle.load(file)

    # loading gk players pickles
    gk_df = pd.read_pickle(r'Data\gk.pkl')
    with open(r'Data\gk_ID.pickle', 'rb') as file:
        gk_ID = pickle.load(file)
    with open(r'Data\gk_engine.pickle', 'rb') as file:
        gk_engine = pickle.load(file)

    return [player_df, player_ID, engine], [gk_df, gk_ID, gk_engine]
    

outfield_data, gk_data = getData()


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
        radio = st.radio('Player type', ['Outfield players', 'Goal Keepers'])    
    with col2:
        if radio=='Outfield players':
            df, player_ID, engine = outfield_data
        else:
            df, player_ID, engine = gk_data
        players = list(player_ID.keys())
        age_default = (min(df['Age']), max(df['Age']))
        query = st.selectbox('Player name', players)

    col3, col4 = st.beta_columns([1, 2])
    with col3:
        comp = st.selectbox('League', ['All', 'Premier League', 'La Liga', 'Serie A', 'Bundesliga', 'Ligue 1'],
            help='Leagues to get recommendations from. All 5 leagues by default.')
    with col4:
        age = st.slider('Age bracket', min_value=age_default[0], max_value=age_default[1], value=age_default, 
        help='Age range to get recommendations from. Drag the sliders on either side. All ages by default.')
    

    col5, col6 = st.beta_columns([1, 1])
    with col5:
        if radio=='Outfield players':
            res, val, step = (5, 20), 10, 5
        else:
            res, val, step = (3, 10), 5, 1
        st.slider('Number of results', min_value=res[0], max_value=res[1], value=val, step=step)
    with col6:
        with st.spinner(text='running recommendation engine'):
            time.sleep(1)
            st.success('Done')

    
    