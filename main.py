from argparse import ArgumentParser
from random import choice
from typing import Dict

import cozmo

from song_match import HotCrossBuns
from song_match import MaryHadALittleLamb
from song_match import RainRainGoAway
from song_match import Song
from song_match import SongMatch


def main():
    song_match_kwargs = get_song_match_kwargs()
    song_match = SongMatch(**song_match_kwargs)
    cozmo.run_program(song_match.play)


def get_song_match_kwargs() -> dict:
    args = parse_args()

    songs = get_songs()
    song_key = args['song_key']
    song = songs[song_key]

    num_players = args['num_players']

    return {
        'song': song,
        'num_players': num_players
    }


def parse_args() -> dict:
    arg_parser = ArgumentParser(description='Play Song Match with Cozmo.')

    song_argument_kwargs = get_song_argument_kwargs()
    arg_parser.add_argument('-s', **song_argument_kwargs)

    num_players_argument_kwargs = get_num_players_argument_kwargs()
    arg_parser.add_argument('-p', **num_players_argument_kwargs)

    args = arg_parser.parse_args()
    return vars(args)


def get_song_argument_kwargs() -> dict:
    song_choices = list(get_songs().keys())
    return {
        'action': 'store',
        'dest': 'song_key',
        'metavar': 'S',
        'type': str,
        'choices': song_choices,
        'help': ('The song to play. ' +
                 'Hot Cross Buns (hcb), Mary Had A Little Lamb (mhall), or Rain Rain Go Away (rrga). ' +
                 'Defaults to a random song.'),
        'default': choice(song_choices)
    }


def get_songs() -> Dict[str, Song]:
    return {
        'hcb': HotCrossBuns(),
        'mhall': MaryHadALittleLamb(),
        'rrga': RainRainGoAway()
    }


def get_num_players_argument_kwargs() -> dict:
    return {
        'action': 'store',
        'dest': 'num_players',
        'metavar': 'N',
        'type': int,
        'choices': range(1, 4),
        'help': ('The number of players for the game. Defaults to None. ' +
                 'If None then selecting the number of players will be handled in game.'),
        'default': None
    }


if __name__ == '__main__':
    main()
