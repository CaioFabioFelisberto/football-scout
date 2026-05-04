import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import plotly.graph_objects as go
import plotly.express as px
from sklearn.ensemble import RandomForestRegressor

cols = ['player_id', 'short_name', 'long_name', 'fifa_version', 'overall', 'potential', 'value_eur', 'player_positions', 'preferred_foot',
        'league_name', 'club_name', 'nationality_name', 'pace', 'shooting', 'passing', 'dribbling', 'defending', 'physic', 'age', 'height_cm', 'weight_kg', 'goalkeeping_handling', 'goalkeeping_diving', 'goalkeeping_kicking', 'goalkeeping_positioning', 'goalkeeping_speed', 'goalkeeping_reflexes']

df = pd.read_csv('male_players(legacy).csv', usecols=cols, low_memory=False)

def get_players_comparison(name1,name2):
    df_player1 = df[df['long_name'].str.contains(name1, case=False, na=False)]
    df_player2 = df[df['long_name'].str.contains(name2, case=False, na=False)]

    if df_player1.empty:
        return f"No player found with the name '{name1}'. Please check the name and try again."
    if df_player2.empty:
        return f"No player found with the name '{name2}'. Please check the name and try again."

    df_player1 = df_player1.sort_values(by='fifa_version', ascending=True)
    df_player2 = df_player2.sort_values(by='fifa_version', ascending=True)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_player1['fifa_version'], y=df_player1['overall'], mode='lines+markers', name=name1))
    fig.add_trace(go.Scatter(x=df_player2['fifa_version'], y=df_player2['overall'], mode='lines+markers', name=name2))
    fig.update_layout(title=f'Evolution of Overall Rating: {name1} vs {name2}', xaxis_title='FIFA Version', yaxis_title='Overall Rating')

    return fig.to_html(full_html=False, include_plotlyjs='cdn')

def get_player_evolution(name,years_ahead=5):
    player = df[df['long_name'].str.contains(name, case=False, na=False)]

    x = player[['age', 'overall']]
    y = player['potential']
    rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
    rf_model.fit(x, y)

    last = player.iloc[-1]

    projections = [{
        'fifa_version': last['fifa_version'],
        'long_name': last['long_name'],
        'age': last['age'],
        'overall': last['overall'],
        'potential': last['potential']
    }]

    current_age = last['age']
    current_overall = last['overall']
    current_fifa = last['fifa_version']

    for i in range(years_ahead):
        current_age += 1
        current_fifa += 1

        peak_age = 27

        age_diff = current_age - peak_age

        age_factor = -0.05 * (age_diff ** 2) + 2

        pred_overall = rf_model.predict([[current_age, current_overall]])[0]
        pred_overall += age_factor

        max_potential = last['potential'] - max(0, current_age - 30) * 0.5
        pred_overall = min(pred_overall, max_potential)

        projections.append({
            'fifa_version': current_fifa,
            'long_name': last['long_name'],
            'age': current_age,
            'overall': current_overall,
            'potential': pred_overall,
            'overall_predicted': round(pred_overall, 1)
        })

        current_overall = pred_overall
    
    future_df = pd.DataFrame(projections)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=future_df['fifa_version'], y=future_df['overall_predicted'], mode='lines+markers', name='Predicted Overall', hoverinfo='text', text=[f"Name: {row['long_name']}<br>Age: {row['age']}<br>Predicted Overall: {row['overall_predicted']}" for _, row in future_df.iterrows()]))
    fig.update_layout(title=f'Projected Evolution of Overall Rating for {name}', xaxis_title='FIFA Version', yaxis_title='Overall Rating')
    fig.update_traces(hovertemplate='FIFA Version: %{x}<br>Predicted Overall: %{y}<extra></extra>')
    fig.update_xaxes(dtick=1)

    return fig.to_html(full_html=False,include_plotlyjs='cdn')

def find_late_bloomers(position, df=df, min_late_growth=5, max_early_growth=3, min_jump=5):
    """
    Encontra jogadores que evoluíram tardiamente (late bloomers)
    
    Parâmetros:
    - df: dataframe com dados do FIFA (15 → 23)
    - position: posição desejada (ex: 'ST', 'CM', 'CB')
    - min_late_growth: crescimento mínimo após 23 anos
    - max_early_growth: crescimento máximo antes dos 23 (pra garantir que não era prodígio)
    - min_jump: diferença mínima entre pico inicial e pico tardio
    
    Retorna:
    - DataFrame com late bloomers ranqueados
    """

    df = df.copy()

    df = df[df['player_positions'].str.contains(position, na=False)]

    df = df.sort_values(['long_name', 'fifa_version'])

    df['overall_diff'] = df.groupby('long_name')['overall'].diff()

    early = df[df['age'] <= 22]
    late = df[df['age'] >= 23]

    early_growth = early.groupby('long_name')['overall_diff'].sum()
    late_growth = late.groupby('long_name')['overall_diff'].sum()

    early_max = early.groupby('long_name')['overall'].max()
    late_max = late.groupby('long_name')['overall'].max()

    result = pd.DataFrame({
        'early_growth': early_growth,
        'late_growth': late_growth,
        'early_max': early_max,
        'late_max': late_max
    }).fillna(0)

    result['late_bloomer_score'] = (
        result['late_growth'] * 2
        - result['early_growth']
        + (result['late_max'] - result['early_max'])
    )

    late_bloomers = result[
        (result['late_growth'] >= min_late_growth) &
        (result['early_growth'] <= max_early_growth) &
        ((result['late_max'] - result['early_max']) >= min_jump)
    ]

    late_bloomers = late_bloomers.sort_values('late_bloomer_score', ascending=False)

    latest_info = df.sort_values('fifa_version').groupby('long_name').tail(1)
    latest_info = latest_info.set_index('long_name')

    final = late_bloomers.join(
        latest_info[['fifa_version', 'age', 'overall', 'player_positions']]
    )

    return final.reset_index()

if __name__ == "__main__":
    print(find_late_bloomers('RB').head(10))