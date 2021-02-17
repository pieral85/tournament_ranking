#test le (just for fun) from my_app import app
from distutils.util import strtobool
from flask import Blueprint, current_app, render_template, request

from .. import session
from ..models.club import Club
from ..models.player import Player
from ...tools.ranking import get_ranks

main = Blueprint('main', __name__, template_folder='templates',
    static_folder='static', static_url_path='/main/static')

club_rankings = get_ranks(session.query(Club).all())
player_rankings = get_ranks(session.query(Player).all())



def _url_param_to_bool(param_name):
    """Smartly convert an URL parameter to a boolean.

       Here are all use cases for `param_name` and related returned values:
       (let's suppose URL is `...?param_name=param_value&...`)
        * `param_name` not set in the URL --> False
        * `param_name` set but no `param_value` --> False
        * `param_value` == `0` --> False
        * `param_value` == `1` --> True
        * `param_value` == `f`|`false`|`n`|`no` --> False
          (see https://docs.python.org/3/distutils/apiref.html#distutils.util.strtobool for more details)
        * `param_value` == "any other value" --> True

    Args:
        param_name (str): Name of the URL parameter
         i.e. `127.0.0.1:5000/my?param_name=param_value&p2=v1`

    Returns:
        bool: The parameter value converted into a boolean
    """
    param = request.args.get(param_name, '0')
    try:
        param = bool(strtobool(param))
    except (AttributeError, ValueError):
        param = bool(param)
    return param

@main.route('/')
def index():
    return render_template('layout.html')

@main.route('/clubs')
def clubs():
    show_ranking = _url_param_to_bool('show_ranking')
    return render_template('clubs.html', rankings=club_rankings, show_ranking=show_ranking)

@main.route('/joueurs')
def players():
    show_ranking = _url_param_to_bool('show_ranking')
    return render_template('players.html', rankings=player_rankings, show_ranking=show_ranking)

@main.route('/matchs')
def matches():
    return 'TODO'
    show_ranking = _url_param_to_bool('show_ranking')
    return render_template('matches.html', rankings=club_rankings, show_ranking=show_ranking)

@main.route('/clubs/<int:club_id>')#, methods=['GET'])
def club(club_id):
    show_ranking = _url_param_to_bool('show_ranking')
    current_app.logger.info(f'Displaying club id={club_id}')  # not working TODO Let it work
    club = session.query(Club).filter_by(id=club_id).first()
    try:
        ranking = [ranking for ranking in club_rankings if ranking[2].id == club_id][0]
    except IndexError:
        ranking = None
    players_rankings = [ranking for ranking in player_rankings if ranking[2].club == club_id]
    return render_template('club.html', club=club, ranking=ranking, players_rankings=players_rankings, show_ranking=show_ranking)

@main.route('/players/<int:player_id>')
def player(player_id):
    player = session.query(Player).filter_by(id=player_id).first()
    try:
        ranking = [ranking for ranking in player_rankings if ranking[2].id == player_id][0]
    except IndexError:
        ranking = None
    return render_template('player.html', player=player, ranking=ranking)
