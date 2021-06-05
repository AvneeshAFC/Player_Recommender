import streamlit as st
import pandas as pd
import numpy as np
import pickle
import time


@st.cache(show_spinner=False)
def getData():
    # loading outfield players pickles
    player_df = pd.read_pickle(r'data\outfield.pkl')
    with open(r'data\player_ID.pickle', 'rb') as file:
        player_ID = pickle.load(file)
    with open(r'data\engine.pickle', 'rb') as file:
        engine = pickle.load(file)

    # loading gk players pickles
    gk_df = pd.read_pickle(r'data\gk.pkl')
    with open(r'data\gk_ID.pickle', 'rb') as file:
        gk_ID = pickle.load(file)
    with open(r'data\gk_engine.pickle', 'rb') as file:
        gk_engine = pickle.load(file)

    return [player_df, player_ID, engine], [gk_df, gk_ID, gk_engine]
    

outfield_data, gk_data = getData()


header = st.beta_container()
data_info1 = st.beta_container()
params = st.beta_container()
result = st.beta_container()
data_info2 = st.beta_container()


with header:
    st.title('Player Recommender Tool')


with data_info1:
    st.markdown('Based on the 2020/21 season data for the **Big 5** European leagues')

    # make images of same sizes by default. load them in st.cache
    # credit, img1, img2 = st.beta_columns([4, 10, 10])
    # with credit:
    #     st.markdown('Data via')
    # with img1:
    #     st.image(r'img/fbref.png')
    # with img2:
    #     st.image(r'img/sb.png')


with params:
    st.text(' \n')
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
        players = sorted(list(player_ID.keys()))
        age_default = (min(df['Age']), max(df['Age']))
        query = st.selectbox('Player name', players, 
                            help='To search from a specific team, just type in the club\'s name.')

    col3, col4, col5 = st.beta_columns([1, 1, 1])
    with col3:
        if radio=='Outfield players':
            res, val, step = (5, 20), 5, 5
        else:
            res, val, step = (3, 10), 5, 1
        count = st.slider('Number of results', min_value=res[0], max_value=res[1], value=val, step=step)
    with col4:
        comp = st.selectbox('League', ['All', 'Premier League', 'La Liga', 'Serie A', 'Bundesliga', 'Ligue 1'],
            help='Leagues to get recommendations from. All 5 leagues by default.')
    with col5:
        age = st.slider('Age bracket', min_value=age_default[0], max_value=age_default[1], value=age_default, 
        help='Age range to get recommendations from. Drag the sliders on either side. All ages by default.')
    

    
with result:
    st.text(' \n')
    st.text(' \n')
    st.text(' \n')
    st.markdown('_showing recommendations for_ **{}**'.format(query))
    

    def getRecommendations(metric, league='All', age=age_default, count=val):
        df_res = df.iloc[:, [1, 3, 5, 6, 11]].copy()
        df_res['Player'] = list(player_ID.keys())
        df_res.insert(1, 'Similarity', metric)
        df_res = df_res.sort_values(by=['Similarity'], ascending=False)
        metric = [str(num) + '%' for num in df_res['Similarity']]
        df_res['Similarity'] = metric
        df_res = df_res.iloc[1:, :]

        
        if league=='All':
            pass
        else:
            df_res = df_res[df_res['Comp']==league]
        
        
        if age==age_default:
            pass
        else:
            df_res = df_res[(df_res['Age'] >= age[0]) & (df_res['Age'] <= age[1])]
        
        
        df_res = df_res.iloc[:count, :].reset_index(drop=True)
        df_res.index = df_res.index + 1
        return df_res

    sims = engine[query]
    recoms = getRecommendations(sims, league=comp, age=age, count=count)
    st.table(recoms)


with data_info2:
    st.markdown('**{}** dataset info'.format(radio))
    info1, info2 = st.beta_columns([1.5, 2])
    with info1:
        st.write('Total number of players: ', len(df))
    with info2:
        st.write('Total number of features compared: ', len(df.columns)-12)