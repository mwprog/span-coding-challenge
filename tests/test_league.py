from league.league import __rank_teams
from league.league import __extract_team_match_name
from league.league import __extract_team_match_goals
from league.league import __extract_team_match
from league.league import __record_win
from league.league import __record_loss
from league.league import __record_draw
from league.league import __create_standings
from league.league import __create_standings_output


def test_extract_team_match_name():
    team_match_name = __extract_team_match_name('Lions 3')

    assert team_match_name == 'Lions'


def test_extract_team_match_name_with_space():
    team_match_name = __extract_team_match_name('FC Awesome 1')

    assert team_match_name == 'FC Awesome'


def test_extract_team_match_name_leading_with_space():
    team_match_name = __extract_team_match_name(' FC Awesome 1')

    assert team_match_name == 'FC Awesome'


def test_extract_team_match_score():
    team_match_score = __extract_team_match_goals('Lions 3')

    assert team_match_score == 3


def test_extract_team_match():
    team_match = __extract_team_match('Lions 3')

    assert team_match
    assert team_match[0] == 'Lions'
    assert team_match[1] == 3


def test_record_first_win():
    team_points = {}

    team_name = 'Lions'
    __record_win(team_points, team_name)

    assert team_name in team_points
    assert team_points[team_name] == 3


def test_record_win():
    team_points = {}

    team_name = 'Lions'
    __record_win(team_points, team_name)
    __record_win(team_points, team_name)

    assert team_name in team_points
    assert team_points[team_name] == 6


def test_record_first_loss():
    team_points = {}

    team_name = 'Lions'
    __record_loss(team_points, team_name)

    assert team_name in team_points
    assert team_points[team_name] == 0


def test_record_loss():
    team_points = {}

    team_name = 'Lions'
    __record_loss(team_points, team_name)
    __record_loss(team_points, team_name)

    assert team_name in team_points
    assert team_points[team_name] == 0


def test_record_first_draw():
    team_points = {}

    team_name = 'Lions'
    __record_draw(team_points, team_name)

    assert team_name in team_points
    assert team_points[team_name] == 1


def test_record_draw():
    team_points = {}

    team_name = 'Lions'
    __record_draw(team_points, team_name)
    __record_draw(team_points, team_name)

    assert team_name in team_points
    assert team_points[team_name] == 2


def test_create_standings():
    standings = __create_standings({
        'Grouches': 0,
        'Lions': 23,
        'FC Awesome': 14,
        'Snakes': 1
    })
    assert len(standings) == 4
    assert standings[0] == ('Lions', 23)
    assert standings[1] == ('FC Awesome', 14)
    assert standings[2] == ('Snakes', 1)
    assert standings[3] == ('Grouches', 0)


def test_create_empty_standings():
    standings = __create_standings({})
    assert len(standings) == 0


def test_create_standings_with_equal_scores():
    standings = __create_standings({
        'Grouches': 4,
        'Lions': 4
    })
    assert len(standings) == 2
    assert standings[0] == ('Grouches', 4)
    assert standings[1] == ('Lions', 4)


def test_rank_teams_from_no_results():
    match_results = []

    rankings = __rank_teams(match_results)

    assert len(rankings) == 0


def test_rank_teams_from_single_result():
    match_results = [['Lions 3', 'Snakes 3']]

    rankings = __rank_teams(match_results)

    assert rankings
    assert len(rankings) == 2
    assert rankings[0] == ('Lions', 1)
    assert rankings[1] == ('Snakes', 1)


def test_rank_teams_from_several_result():
    match_results = [
        ['Lions 3', ' Snakes 3'],
        ['Tarantulas 1', ' FC Awesome 0'],
        ['Lions 1', ' FC Awesome 1'],
        ['Tarantulas 3', ' Snakes 1'],
        ['Lions 4', ' Grouches 0']
    ]

    rankings = __rank_teams(match_results)

    assert rankings
    assert len(rankings) == 5
    assert rankings[0] == ('Tarantulas', 6)
    assert rankings[1] == ('Lions', 5)
    assert rankings[2] == ('FC Awesome', 1)
    assert rankings[3] == ('Snakes', 1)
    assert rankings[4] == ('Grouches', 0)


def test_create_standings_output():
    standings = [
        ('Tarantulas', 8),
        ('Lions', 5),
        ('FC Awesome', 3),
        ('Grouches', 1)
    ]
    output = __create_standings_output(standings)

    print(output)

    assert output == """1. Tarantulas, 8 pts
2. Lions, 5 pts
3. FC Awesome, 3 pts
4. Grouches, 1 pt
"""
