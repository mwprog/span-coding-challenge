from league.league import __read_matches
from league.league import __write_standings


def test_read_matches():
    matches = __read_matches('tests_integration/input/input.txt')

    assert matches
    assert len(matches) == 5
    assert matches[0] == ['Lions 3', ' Snakes 3']
    assert matches[4] == ['Lions 4', ' Grouches 0']


def test_read_matches_empty_input():
    matches = __read_matches('tests_integration/input/empty_input.txt')

    assert len(matches) == 0


def test_read_matches_missing_file():
    matches = __read_matches('tests_integration/input/missing_input.txt')
    assert matches is None


def test_create_standings_output():
    standings = [('Lions', 12)]
    standings_file_path = 'tests_integration/output/standings_test.txt'
    result = __write_standings(standings, standings_file_path)
    assert result

    with open(standings_file_path, 'r') as file:
        data = file.read().strip()
        assert '1. Lions, 12 pts' == data

