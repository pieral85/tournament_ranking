#test le (just for fun) from my_app import app
from flask import Blueprint, current_app, render_template, request

from .. import session
from ..models.club import Club
from ..models.player import Player
from ...tools.ranking import get_ranks

main = Blueprint('main', __name__, template_folder='templates',
    static_folder='static', static_url_path='/main/static')

club_rankings = get_ranks(session.query(Club).all())
player_rankings = get_ranks(session.query(Player).all())

@main.route('/')
def index():
    return render_template('layout.html')

@main.route('/clubs')
def clubs():
    # club_id = request.args.get('club_id')
    # if club_id:
    #     club = session.query(Club).filter_by(id=club_id).first()
    # else:
    #     TODO a lot of work...
    #     clubs = session.query(Club).all()
    clubs = session.query(Club).all()
    return render_template('clubs.html', clubs=clubs)

@main.route('/clubs/<int:club_id>')#, methods=['GET'])
def club(club_id):
    # club_id = request.args.get('club_id')
    current_app.logger.info(f'Displaying club id={club_id}')  # not working TODO Let it work
    # club_name = 'BC Saint-Légerr'
    # saint_leger = session.query(Club).filter_by(name=club_name).first()
    # import ipdb; ipdb.set_trace()

    club = session.query(Club).filter_by(id=club_id).first()
    try:
        ranking = [ranking for ranking in club_rankings if ranking[2].id == club_id][0]
    except IndexError:
        ranking = None
    players_rankings = [ranking for ranking in player_rankings if ranking[2].club == club_id]
    # matches = session.query(Match)
    return render_template('club.html', club=club, ranking=ranking, players_rankings=players_rankings)#, matches=matches)

@main.route('/players/<int:player_id>')
def player(player_id):
    player = session.query(Player).filter_by(id=player_id).first()
    try:
        ranking = [ranking for ranking in player_rankings if ranking[2].id == player_id][0]
    except IndexError:
        ranking = None
    return render_template('player.html', player=player, ranking=ranking)

@main.route('/clubs/ranking')
def clubs_ranking():
    clubs = session.query(Club).all()
    # club_name = 'BC Saint-Légerr'
    # saint_leger = session.query(Club).filter_by(name=club_name).first()
    # import ipdb; ipdb.set_trace()
    # club = session.query(Club).filter_by(id=club_id).first()
    # 2021-02-07 rankings = get_ranks(session.query(Club).all())
    return render_template('clubs_ranking.html', rankings=club_rankings)
    return f'Hello, {"---".join((c.name + str(": ") + str(c.points)) for c in clubs)}'#, {results}'
