import os
import re
import logging
from argparse import ArgumentParser
import csv


logging.basicConfig(
    level=os.environ.get('LOGLEVEL', 'INFO').upper()
)


def __extract_team_match_name(team_match: str) -> str:
    matches = re.search(r'(.+) \d+$', team_match.strip())
    return matches.group(1) if matches else None


def __extract_team_match_goals(team_match: str) -> str:
    matches = re.search(r'.+ (\d+)$', team_match.strip())
    return int(matches.group(1)) if matches else None


def __extract_team_match(team_match: str) -> str:
    return (
        __extract_team_match_name(team_match),
        __extract_team_match_goals(team_match)
    )


def __record_draw(team_points: dict, team_name: str):
    if team_name not in team_points:
        team_points[team_name] = 0

    team_points[team_name] += 1


def __record_win(team_points: dict, team_name: str):
    if team_name not in team_points:
        team_points[team_name] = 0

    team_points[team_name] += 3


def __record_loss(team_points: dict, team_name: str):
    if team_name not in team_points:
        team_points[team_name] = 0


def __create_standings(team_points: dict) -> list[tuple]:
    standings = team_points.items()
    return sorted(standings, key=lambda x: (-x[1], x[0]))


def __rank_teams(match_results: list[list[str]]) -> list[tuple]:
    team_points = {}

    for match_result in match_results:
        home_team_match = __extract_team_match(match_result[0])
        away_team_match = __extract_team_match(match_result[1])

        home_team_name = home_team_match[0]
        away_team_name = away_team_match[0]

        home_team_score = home_team_match[1]
        away_team_score = away_team_match[1]

        if home_team_score > away_team_score:
            __record_win(team_points, home_team_name)
            __record_loss(team_points, away_team_name)
        elif home_team_score < away_team_score:
            __record_loss(team_points, home_team_name)
            __record_win(team_points, away_team_name)
        else:
            __record_draw(team_points, home_team_name)
            __record_draw(team_points, away_team_name)

    return __create_standings(team_points)


def __read_matches(file_path: str) -> list[str]:
    try:
        content = []
        with open(file_path, 'r', encoding='utf-8') as file:
            csv_reader = csv.reader(file, delimiter=',')
            for row in csv_reader:
                content.append(row)

        return content
    except IOError:
        logging.exception(f'Unable to read match results file "{file_path}"')
        return None


def __create_standings_output(standings: dict[tuple]) -> str:
    output = ''
    for i, (team, points) in enumerate(standings, start=1):
        suffix = 'pts' if points != 1 else 'pt'
        output += f'{i}. {team}, {points} {suffix}\n'

    return output


def __write_standings(standings: list, standings_file_path: str):
    output = __create_standings_output(standings)
    logging.debug(output)

    try:
        with open(standings_file_path, 'w') as file:
            file.write(output)

        return 'success'
    except IOError:
        logging.exception(f'Unable to write standings to "{standings_file_path}"')
        return None


def main(match_data_file_path, standings_file_path):
    match_results = __read_matches(match_data_file_path)
    if match_results is not None:
        if len(match_results) > 0:
            standings = __rank_teams(match_results)
            result = __write_standings(standings, standings_file_path)

            if result is None:
                logging.error('Unable to run write standings due to error. See log for details.')
                exit(1)
            else:
                logging.info(f'Standings written to {standings_file_path}')
        else:
            logging.warning('Unable to calculate standings as no match results found in input.')
    else:
        logging.error('Unable to run programme due to error. See log for details.')
        exit(1)


if __name__ == "__main__":
    parser = ArgumentParser(prog='League Standing Calculator',
                            description='Calculates league standings of teams from match results')
    parser.add_argument('--input_file', dest='input_file', help='File to read match results from', required=True)
    parser.add_argument('--output_file', dest='output_file', help='File to write standings to', required=True)
    args = parser.parse_args()

    main(args.input_file, args.output_file)
