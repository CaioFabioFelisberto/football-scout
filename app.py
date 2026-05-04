from flask import Flask, render_template, request

app = Flask(__name__)


@app.template_filter('format_money')
def format_money(value):
    if value is None:
        return "-"

    value = float(value)

    if value >= 1_000_000:
        return f"€{value/1_000_000:.1f}M"
    elif value >= 1_000:
        return f"€{value/1_000:.0f}K"
    else:
        return f"€{value:.0f}"


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/wonderkids')
def wonderkids():
    from funcs1 import get_wonderkids

    position = request.args.get('players_position')

    if not position:
        return render_template(
            'wonderkids.html',
            players=[],
            page=1,
            total_pages=1,
            position=''
        )

    page = request.args.get('page', 1, type=int)

    data = get_wonderkids(f'{position}').to_dict(orient='records')

    per_page = 10
    total = len(data)

    start = (page - 1) * per_page
    end = start + per_page

    players_page = data[start:end]
    total_pages = (total + per_page - 1) // per_page

    return render_template(
        'wonderkids.html',
        players=players_page,
        page=page,
        total_pages=total_pages,
        position=position
    )


@app.route('/similar_players')
def similar_players():
    from funcs1 import get_similar_players
    player_name = request.args.get('player_name')
    if not player_name:
        return render_template('similar_players.html', similar_players=[], player_name=player_name, page=1, total_pages=1)
    page = request.args.get('page', 1, type=int)
    data = get_similar_players(player_name).to_dict(orient='records')
    per_page = 10
    total = len(data)
    start = (page - 1) * per_page
    end = start + per_page
    players_page = data[start:end]
    total_pages = (total + per_page - 1) // per_page
    return render_template('similar_players.html', similar_players=players_page, player_name=player_name, page=page, total_pages=total_pages)


@app.route('/veterans')
def veterans():
    from funcs1 import get_veterans
    position = request.args.get('players_position')
    if not position:
        return render_template(
            'veterans.html',
            players=[],
            page=1,
            total_pages=1,
            position=''
        )
    page = request.args.get('page', 1, type=int)
    data = get_veterans(f'{position}').to_dict(orient='records')
    per_page = 10
    total = len(data)
    start = (page - 1) * per_page
    end = start + per_page
    players_page = data[start:end]
    total_pages = (total + per_page - 1) // per_page
    return render_template('veterans.html', players=players_page, page=page, total_pages=total_pages, position=position)


@app.route('/players_evolution')
def players_evolution():
    from funcs2 import get_player_evolution
    name = request.args.get('player_name')
    years = request.args.get('years_ahead', 5, type=int)
    if not name:
        return render_template(
            'players_evolution.html',
            player_name='',
            years_ahead=years,
            evolution_html=''
        )
    evolution_html = get_player_evolution(name, years)
    return render_template(
        'players_evolution.html',
        player_name=name,
        years_ahead=years,
        evolution_html=evolution_html
    )


@app.route('/archetypes')
def archetypes():
    from funcs1 import get_forward_archetypes, get_midfielder_archetypes, get_defender_archetypes, get_goalkeeper_archetypes
    area = request.args.get('area', 'forward')
    archetype = request.args.get('archetype', '')
    if area == 'forward':
        archetypes = get_forward_archetypes(
            archetype).to_dict(orient='records')
        page = request.args.get('page', 1, type=int)
        per_page = 10
        total = len(archetypes)
        start = (page - 1) * per_page
        end = start + per_page
        players_page = archetypes[start:end]
        total_pages = (total + per_page - 1) // per_page
        return render_template('archetypes.html', players=players_page, area=area, archetype=archetype, page=page, total_pages=total_pages)
    elif area == 'midfielder':
        archetypes = get_midfielder_archetypes(
            archetype).to_dict(orient='records')
        page = request.args.get('page', 1, type=int)
        per_page = 10
        total = len(archetypes)
        start = (page - 1) * per_page
        end = start + per_page
        players_page = archetypes[start:end]
        total_pages = (total + per_page - 1) // per_page
        return render_template('archetypes.html', players=players_page, area=area, archetype=archetype, page=page, total_pages=total_pages)
    elif area == 'defender':
        archetypes = get_defender_archetypes(
            archetype).to_dict(orient='records')
        page = request.args.get('page', 1, type=int)
        per_page = 10
        total = len(archetypes)
        start = (page - 1) * per_page
        end = start + per_page
        players_page = archetypes[start:end]
        total_pages = (total + per_page - 1) // per_page
        return render_template('archetypes.html', players=players_page, area=area, archetype=archetype, page=page, total_pages=total_pages)
    elif area == 'goalkeeper':
        archetypes = get_goalkeeper_archetypes(
            archetype).to_dict(orient='records')
        page = request.args.get('page', 1, type=int)
        per_page = 10
        total = len(archetypes)
        start = (page - 1) * per_page
        end = start + per_page
        players_page = archetypes[start:end]
        total_pages = (total + per_page - 1) // per_page
        return render_template('archetypes.html', players=players_page, area=area, archetype=archetype, page=page, total_pages=total_pages)
    else:
        return render_template('archetypes.html', players=[], area=area, archetype=archetype, page=1, total_pages=1)


@app.route('/bargain_players')
def bargain_players():
    from funcs1 import get_bargain_players
    position = request.args.get('position')
    if not position:
        return render_template(
            'bargain_players.html',
            position='',
            players_page=[],
            page=1,
            total_pages=1
        )
    data = get_bargain_players(position).to_dict(orient='records')
    page = request.args.get('page', 1, type=int)
    per_page = 10
    total = len(data)
    start = (page - 1) * per_page
    end = start + per_page
    players_page = data[start:end]
    total_pages = (total + per_page - 1) // per_page
    return render_template('bargain_players.html', position=position, players=players_page, page=page, total_pages=total_pages)


@app.route('/players_by_league')
def players_by_league():
    from funcs1 import get_players_by_league
    position = request.args.get('position')
    league = request.args.get('league')
    value = request.args.get('value', type=float)
    if not position or not league or value is None:
        return render_template(
            'players_by_league.html',
            position='',
            league='',
            value='',
            players_page=[],
            page=1,
            total_pages=1
        )
    data = get_players_by_league(
        position, league, value).to_dict(orient='records')
    page = request.args.get('page', 1, type=int)
    per_page = 10
    total = len(data)
    start = (page - 1) * per_page
    end = start + per_page
    players_page = data[start:end]
    total_pages = (total + per_page - 1) // per_page
    return render_template('players_by_league.html', position=position, league=league, value=value, players=players_page, page=page, total_pages=total_pages)


@app.route('/players_comparison')
def players_comparison():
    from funcs2 import get_players_comparison
    name1 = request.args.get('player1')
    name2 = request.args.get('player2')
    if not name1 or not name2:
        return render_template('players_comparison.html', error="Please provide both player names.")
    comparison_fig = get_players_comparison(name1, name2)
    return render_template('players_comparison.html', player1=name1, player2=name2, comparison=comparison_fig)


@app.route('/late_bloomers')
def late_bloomers():
    from funcs2 import find_late_bloomers

    position = request.args.get('players_position')

    if not position:
        return render_template(
            'late_bloomers.html',
            players=[],
            page=1,
            total_pages=1,
            position=''
        )

    page = request.args.get('page', 1, type=int)

    data = find_late_bloomers(f'{position}').to_dict(orient='records')

    per_page = 10
    total = len(data)

    start = (page - 1) * per_page
    end = start + per_page

    players_page = data[start:end]
    total_pages = (total + per_page - 1) // per_page

    return render_template(
        'late_bloomers.html',
        players=players_page,
        page=page,
        total_pages=total_pages,
        position=position
    )


if __name__ == "__main__":
    app.run(debug=True)
