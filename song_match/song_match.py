"""Module containing :class:`~song_match.song_match.SongMatch`."""

from asyncio import sleep
from sys import exit
from typing import Callable, List

from cozmo.objects import EvtObjectTapped
from cozmo.robot import Robot

from song_match.cube import NoteCube
from song_match.cube import NoteCubes
from .effect import EffectFactory
from .player import Player
from .song import MaryHadALittleLamb
from .song import Note
from .song_robot import SongRobot

MAX_STRIKES = 3  # The maximum number of notes a player can get wrong

TIME_IN_BETWEEN_PLAYER_AND_COZMO = 1  # In seconds

STARTING_POSITION = 3  # The number of notes you start with in the sequence

TIME_BETWEEN_NOTES = 0.5


class SongMatch:
    """Main game class."""

    def __init__(self, num_players: int = 1):
        self._song_robot = None
        self._note_cubes = None
        self._effect_factory = None
        self._prevent_tap = False  # Flag to prevent player from interrupting game by tapping cubes
        self._song = MaryHadALittleLamb()
        self._players = [Player(i) for i in range(num_players)]
        Note.init_mixer()
        self._game_length = len(self._song.get_sequence())

    async def play(self, robot: Robot) -> None:
        """Play the Song Match game.

        Pass this function into :func:`cozmo.run_program`.

        :param robot: Cozmo Robot instance.
        :type robot: :class:`~cozmo.robot.Robot`
        :return: None
        """
        self._song_robot = SongRobot(robot, self._song)
        self._note_cubes = NoteCubes.of(self._song_robot)
        self._effect_factory = EffectFactory(self._song_robot)
        await self.__setup()
        await self.__init_game_loop()

    async def __setup(self) -> None:
        await self._song_robot.world.wait_until_num_objects_visible(3)
        self._song_robot.world.add_event_handler(EvtObjectTapped, self.__tap_handler)
        self._note_cubes.turn_on_lights()

    async def __tap_handler(self, evt, obj=None, tap_count=None, **kwargs):
        if self._prevent_tap:
            return
        cube = evt.obj
        note_cube = NoteCube(cube, self._song)
        await note_cube.blink_and_play_note()

    async def __init_game_loop(self) -> None:
        current_position = STARTING_POSITION
        while self._song.is_not_finished(current_position, self._game_length):
            notes = self._song.get_sequence_slice(current_position)
            await self.__tap_guard(lambda: self.__play_notes(notes))

            await self.__wait_for_players_to_match_notes(current_position)

            await sleep(TIME_IN_BETWEEN_PLAYER_AND_COZMO)

            await self.__wait_for_cozmo_to_match_notes(current_position)

            await self.__tap_guard(lambda: self.__play_round_transition_effect())

            current_position = self.__update_position(current_position)

    async def __wait_for_players_to_match_notes(self, current_position: int) -> None:
        for i, player in enumerate(self._players):
            await self.__wait_for_player_to_match_notes(current_position, i)

    async def __wait_for_player_to_match_notes(self, current_position: int, player_index: int) -> bool:
        num_notes_played = 0
        notes = self._song.get_sequence_slice(current_position)
        while num_notes_played != current_position:
            event = await self._song_robot.world.wait_for(EvtObjectTapped)
            tapped_cube = NoteCube(event.obj, self._song)
            correct_note = notes[num_notes_played]

            if tapped_cube.note != correct_note:
                self._players[player_index].num_wrong += 1
                await self.__tap_guard(lambda: self.__play_wrong_note_effect(tapped_cube.cube_id))
                self.__check_for_game_over()
                return False

            num_notes_played += 1

        await self.__tap_guard(lambda: self.__play_correct_sequence_effect())
        return True

    async def __wait_for_cozmo_to_match_notes(self, current_position: int) -> bool:
        notes = self._song.get_sequence_slice(current_position)
        played_correct_sequence, note = await self.__tap_guard(
            lambda: self._song_robot.play_notes(notes, with_error=True)
        )
        if played_correct_sequence:
            await self.__tap_guard(lambda: self.__play_correct_sequence_effect(is_player=False))
        else:
            self._song_robot.num_wrong += 1
            wrong_cube_id = self._song.get_cube_id(note)
            await self.__tap_guard(lambda: self.__play_wrong_note_effect(wrong_cube_id, is_player=False))
            self.__check_for_game_over()
            return False

        return True

    def __check_for_game_over(self) -> None:
        num_wrong_per_player = [player.num_wrong for player in self._players]
        num_wrong_per_player.append(self._song_robot.num_wrong)
        for num_wrong in num_wrong_per_player:
            if num_wrong == MAX_STRIKES:
                exit(0)

    async def __tap_guard(self, callable_function: Callable):
        self._prevent_tap = True
        result = await callable_function()
        self._prevent_tap = False
        return result

    async def __play_wrong_note_effect(self, cube_id: int, is_player=True):
        effect = self._effect_factory.create('WrongNote')
        await effect.play(cube_id, is_player=is_player)

    async def __play_correct_sequence_effect(self, is_player=True):
        effect = self._effect_factory.create('CorrectSequence')
        await effect.play(is_player=is_player)

    async def __play_round_transition_effect(self):
        effect = self._effect_factory.create('RoundTransition')
        await effect.play()

    async def __play_notes(self, notes: List[Note]) -> None:
        for note in notes:
            await self.__play_note(note)
            await sleep(note.duration)

    async def __play_note(self, note: Note) -> None:
        cube_id = self._song.get_cube_id(note)
        note_cube = NoteCube.of(self._song_robot, cube_id)
        await note_cube.blink_and_play_note()

    def __update_position(self, current_position: int) -> int:
        MEDIUM, LONG = self._song.get_gamelength_markers()
        if current_position < MEDIUM or current_position == self._game_length:
            return current_position + 1
        elif current_position < LONG:
            current_position += 2
            if current_position > self._game_length:
                current_position = self._game_length
            return current_position
        else:
            current_position += 3
            if current_position > self._game_length:
                current_position = self._game_length
            return current_position
