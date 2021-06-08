import streamlit as st
import pandas as pd
import pickle
from pathlib import Path



@st.cache(show_spinner=False)
def getData():
    # loading outfield players' cleaned data and engine
    player_df = pd.read_pickle(r'data\outfield.pkl')
    with open(r'data\player_ID.pickle', 'rb') as file:
        player_ID = pickle.load(file)
    with open(r'data\engine.pickle', 'rb') as file:
        engine = pickle.load(file)

    # loading gk players' cleaned data and engine
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


with header:
    st.title('Player Recommender Tool')


with data_info1:
    st.markdown('Based on the 2020/21 season data for the **Big 5** European leagues :soccer:')
    @st.cache
    def read_info(path):
        return Path(path).read_text(encoding='utf8')

    st.markdown(read_info('info.md'), unsafe_allow_html=True)



with params:
    st.text(' \n')
    st.text(' \n')
    st.header('Tweak the parameters')
    
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
            help='Type without deleting a character. To search from a specific team, just type in the club\'s name.')

    col3, col4, col5, col6 = st.beta_columns([0.7, 1, 1, 1])
    with col3:
        if radio=='Outfield players':
            res, val, step = (5, 20), 10, 5
        else:
            res, val, step = (3, 10), 5, 1
        count = st.slider('Number of results', min_value=res[0], max_value=res[1], value=val, step=step)
    with col4:
        comp = st.selectbox('League', ['All', 'Premier League', 'La Liga', 'Serie A', 'Bundesliga', 'Ligue 1'],
            help='Leagues to get recommendations from. \'All\' leagues by default.')
    with col5:
        comparison = st.selectbox('Comparison with', ['All positions', 'Same position'],
            help='Whether to compare the selected player with all positions or just the same defined position in the dataset. \'All \
            positions\' by default.')
    with col6:
        age = st.slider('Age bracket', min_value=age_default[0], max_value=age_default[1], value=age_default, 
        help='Age range to get recommendations from. Drag the sliders on either side. \'All\' ages by default.')
    

    
with result:
    st.text(' \n')
    st.text(' \n')
    st.text(' \n')
    st.markdown('_showing recommendations for_ **{}**'.format(query))
    

    def getRecommendations(metric, league='All', comparison='All positions', age=age_default, count=val):
        df_res = df.iloc[:, [1, 3, 5, 6, 11]].copy()
        df_res['Player'] = list(player_ID.keys())
        df_res.insert(1, 'Similarity', metric)
        df_res = df_res.sort_values(by=['Similarity'], ascending=False)
        metric = [str(num) + '%' for num in df_res['Similarity']]
        df_res['Similarity'] = metric
        df_res = df_res.iloc[1:, :]

        
        if comparison == 'Same position':
            q_pos = list(df[df['Player']==query.split(' (')[0]].Pos)[0]
            df_res = df_res[df_res['Pos']==q_pos]


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
        if len(df)==2040:
            mp90 = [str(round(num, 1)) for num in df_res['90s']]
            df_res['90s'] = mp90
        df_res.rename(columns={'Pos':'Position', 'Comp':'League'}, inplace=True)
        return df_res


    sims = engine[query]
    recoms = getRecommendations(sims, league=comp, comparison=comparison, age=age, count=count)
    st.table(recoms)