from argparse import ArgumentParser

import cozmo

from song_match import SongMatch


def main():
    args = parse_args()
    num_players = args['num_players']
    song_match = SongMatch(num_players=num_players)
    cozmo.run_program(song_match.play)


def parse_args() -> dict:
    arg_parser = ArgumentParser(description='Play Song Match with Cozmo.')
    num_players_argument_kwargs = get_num_players_argument_kwargs()
    arg_parser.add_argument('-p', **num_players_argument_kwargs)
    args = arg_parser.parse_args()
    return vars(args)


def get_num_players_argument_kwargs() -> dict:
    return {
        'action': 'store',
        'dest': 'num_players',
        'metavar': 'N',
        'type': int,
        'choices': range(1, 6),
        'help': 'The number of players for the game.',
        'default': 1
    }


if __name__ == '__main__':
    main()
