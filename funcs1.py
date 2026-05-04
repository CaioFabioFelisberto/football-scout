import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

cols = ['player_id', 'short_name', 'long_name', 'fifa_version', 'overall', 'potential', 'value_eur', 'player_positions', 'preferred_foot',
        'league_name', 'club_name', 'nationality_name', 'pace', 'shooting', 'passing', 'dribbling', 'defending', 'physic', 'age', 'height_cm', 'weight_kg', 'goalkeeping_handling', 'goalkeeping_diving', 'goalkeeping_kicking', 'goalkeeping_positioning', 'goalkeeping_speed', 'goalkeeping_reflexes']

df = pd.read_csv('male_players(legacy).csv', usecols=cols, low_memory=False)

df_sorted = df.sort_values(
    by=['player_id', 'fifa_version'], ascending=[True, False])

df_scout = df_sorted.drop_duplicates(subset=['player_id'], keep='first')

df_scout = df_scout.reset_index(drop=True)


def get_wonderkids(position):
    df_wonderkids = df_scout.copy()

    wonderkids = df_wonderkids[(df_wonderkids['player_positions'].str.contains(position, na=False)) &
                               (df_wonderkids['age'] <= 21) &
                               (df_wonderkids['potential'] >= 80) &
                               (df_wonderkids['value_eur'] <= 20000000)

                               ]

    wonderkids = wonderkids.sort_values(
        by=['fifa_version', 'potential', 'value_eur'], ascending=[False, False, True])

    interest_columns = ['fifa_version', 'short_name', 'long_name', 'age', 'preferred_foot', 'overall',
                        'potential', 'player_positions', 'nationality_name', 'league_name', 'club_name', 'value_eur']

    return wonderkids[interest_columns]


def get_veterans(position, value=1000000000):
    df_veterans = df_scout.copy()

    veterans = df_veterans[(df_veterans['player_positions'].str.contains(position, na=False)) &
                           (df_veterans['age'] >= 29) &
                           (df_veterans['overall'] >= 80) &
                           (df_veterans['value_eur'] <= value)

                           ]

    veterans = veterans.sort_values(
        by=['fifa_version', 'overall', 'value_eur'], ascending=[False, False, True])

    interest_columns = ['fifa_version', 'short_name', 'long_name', 'age', 'preferred_foot',
                        'overall', 'player_positions', 'nationality_name', 'league_name', 'club_name', 'value_eur']

    return veterans[interest_columns]


def get_bargain_players(position):
    df_bargain = df_scout.copy()

    bargain_players = df_bargain[(
        df_bargain['player_positions'].str.contains(position, na=False))]

    bargain_players['score'] = ((bargain_players['overall'] +
                                bargain_players['potential']) / bargain_players['value_eur']).round(5)

    bargain_players = bargain_players[bargain_players['score'].notna()]
    bargain_players = bargain_players[~np.isinf(bargain_players['score'])]

    bargain_players = bargain_players.sort_values(by=['score','overall'], ascending=[False, False])

    interest_columns = ['fifa_version', 'short_name', 'long_name', 'age', 'preferred_foot', 'overall',
                        'potential', 'score', 'player_positions', 'nationality_name', 'league_name', 'club_name', 'value_eur']

    return bargain_players[interest_columns]


def get_similar_players(name):
    attributes = ['pace', 'shooting', 'passing',
                  'dribbling', 'defending', 'physic']
    df_calc = df_scout.dropna(subset=attributes).copy()

    target = df_calc[df_calc['short_name'].str.contains(
        name, case=False, na=False)]
    if target.empty:
        return "Jogador não encontrado"

    target = target.iloc[0]
    scaler = MinMaxScaler()
    df_calc[attributes] = scaler.fit_transform(df_calc[attributes])

    target_status = df_calc.loc[target.name, attributes].values.reshape(1, -1)
    all_status = df_calc[attributes].values

    similarities = cosine_similarity(target_status, all_status)[0]

    df_calc['similarity'] = similarities.round(5)

    similars = df_calc[df_calc['player_id'] != target['player_id']]
    similars = similars.sort_values(by=['similarity','overall'], ascending=[False, False])

    final_cols = ['short_name', 'similarity', 'overall','age',
                  'preferred_foot', 'value_eur', 'player_positions']
    return similars[final_cols]


def get_forward_archetypes(archetype):
    attributes = ['pace', 'shooting', 'passing',
                  'dribbling', 'defending', 'physic']

    df_archtypes = df_scout.dropna(subset=attributes).copy()

    df_forward = df_archtypes[df_archtypes['player_positions'].str.contains(
        r'\b(RW|LW|RF|LF|CF|ST)\b')]

    scaler = StandardScaler()
    normalized_data = scaler.fit_transform(df_forward[attributes])

    kmeans_model = KMeans(n_clusters=6, random_state=42, n_init='auto')

    df_forward['cluster_id'] = kmeans_model.fit_predict(normalized_data)

    archtypes_name = {0: 'Budget Finisher', 1: 'Physical Target Man', 2: 'Elite Target Poacher',
                      3: 'Multi-Position Specialist', 4: 'Technical Inside Forward', 5: 'Complete Forward'}

    df_forward['archtype'] = df_forward['cluster_id'].map(archtypes_name)
    cols = ['fifa_version', 'short_name', 'age', 'player_positions', 'potential','overall', 'cluster_id','archtype','value_eur']

    return df_forward[cols][df_forward['archtype'] == archetype].sort_values(by='overall', ascending=False)

def get_midfielder_archetypes(archetype):
    attributes = ['pace', 'shooting', 'passing',
                  'dribbling', 'defending', 'physic']

    df_archtypes = df_scout.dropna(subset=attributes).copy()

    df_midfielder = df_archtypes[df_archtypes['player_positions'].str.contains(r'\b(CM|CDM|CAM|RM|LM)\b')]

    scaler = StandardScaler()
    normalized_data = scaler.fit_transform(df_midfielder[attributes])

    kmeans_model = KMeans(n_clusters=8, random_state=42, n_init='auto')

    df_midfielder['cluster_id'] = kmeans_model.fit_predict(normalized_data)

    archtypes_name = {0: 'Explosive Playmaker', 1: 'Defensive Specialist',2:'Low-Tier Creative Utility',3:'Technical Playmaker',4:'Physical Destroyer',
                     5:'Versatile Defensive Workhorse',6:'Creative Engine',7:'Agile Transition Winger'}

    df_midfielder['archtype'] = df_midfielder['cluster_id'].map(archtypes_name)
    cols = ['fifa_version', 'short_name', 'age', 'player_positions', 'potential','overall', 'cluster_id','archtype','value_eur']

    return df_midfielder[cols][df_midfielder['archtype'] == archetype].sort_values(by='overall', ascending=False)

def get_defender_archetypes(archetype):
    attributes = ['pace', 'shooting', 'passing',
                  'dribbling', 'defending', 'physic']
    df_archtypes = df_scout.dropna(subset=attributes).copy()

    df_defender = df_archtypes[df_archtypes['player_positions'].str.contains(r'\b(CB|LB|RB|LWB|RWB)\b')]

    scaler = StandardScaler()
    normalized_data = scaler.fit_transform(df_defender[attributes])

    kmeans_model = KMeans(n_clusters=6, random_state=42, n_init='auto')

    df_defender['cluster_id'] = kmeans_model.fit_predict(normalized_data)

    archtypes_name = {0:'Elite Offensive Full-back', 1:'Low-Tier Defensive Full-back', 2:'Physical No-Nonsense CB',3:'Versatile Defensive Utility', 4:'Budget Defensive Specialist',5:'Ball-Playing Defender'}

    df_defender['archtype'] = df_defender['cluster_id'].map(archtypes_name)

    cols = ['fifa_version', 'short_name', 'age', 'player_positions', 'potential','overall', 'cluster_id','archtype','value_eur']

    return df_defender[cols][df_defender['archtype'] == archetype].sort_values(by='overall', ascending=False)

def get_goalkeeper_archetypes(archetype):
    attributes = ['goalkeeping_diving', 'goalkeeping_handling', 'goalkeeping_kicking', 'goalkeeping_positioning', 'goalkeeping_reflexes','goalkeeping_speed']
    df_archtypes = df_scout.dropna(subset=attributes).copy()

    df_goalkeeper = df_archtypes[df_archtypes['player_positions'].str.contains(r'\b(GK)\b')]

    scaler = StandardScaler()
    normalized_data = scaler.fit_transform(df_goalkeeper[attributes])

    kmeans_model = KMeans(n_clusters=2, random_state=42, n_init='auto')

    df_goalkeeper['cluster_id'] = kmeans_model.fit_predict(normalized_data)

    archtypes_name = {0: 'Modern Sweeper-Keeper', 1: 'Traditional Goalkeeper'}
    df_goalkeeper['archtype'] = df_goalkeeper['cluster_id'].map(archtypes_name)
    cols = ['fifa_version', 'short_name', 'age', 'player_positions', 'potential','overall', 'cluster_id','archtype','value_eur']

    return df_goalkeeper[cols][df_goalkeeper['archtype'] == archetype].sort_values(by='overall', ascending=False)

def get_players_by_league(position,league,value):
    df_players = df_scout.copy()

    players = df_players[
        df_players['player_positions'].str.contains(position, na=False) &
        df_players['league_name'].str.contains(league, na=False) &
        (df_players['value_eur'] <= value)
    ]
    
    players = players.sort_values(by=['overall','value_eur'],ascending=[False,True])

    interest_columns = ['fifa_version','player_positions','short_name','age','preferred_foot','overall','potential','league_name','value_eur']

    return players[interest_columns]

if __name__ == "__main__":
    print(get_players_by_league('RW','Serie A',30000000).head(10))
