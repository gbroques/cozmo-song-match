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
        self.MEDIUM, self.LONG = self._song.get_gamelength_markers()


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
            await self.__tap_guard(lambda: self.__play_round_transition_effect())

            await self.__wait_for_players_to_match_notes(current_position)

            await sleep(TIME_IN_BETWEEN_PLAYER_AND_COZMO)

            await self.__wait_for_cozmo_to_match_notes(current_position)

            await self.__tap_guard(lambda: self.__update_if_still_in_game())

            await self.__tap_guard(lambda: self.__check_for_game_over())

            current_position = self.__update_position(current_position)

        await self.__tap_guard(lambda: self.__play_end_game_results())

    async def __wait_for_players_to_match_notes(self, current_position: int) -> None:
        notes = self._song.get_sequence_slice(current_position)

        for i, player in enumerate(self._players):
            if player.num_wrong < MAX_STRIKES:
                await self.__player_turn_prompt(i)
                await self.__tap_guard(lambda: self.__play_notes(notes))
                await self.__wait_for_player_to_match_notes(current_position, i)
        await self.__tap_guard(lambda: self.__check_for_game_over())


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
                return False

            num_notes_played += 1

        await self.__tap_guard(lambda: self.__play_correct_sequence_effect())
        return True


    async def __player_turn_prompt(self, player_index: int):
        cozmo_text = "Player " + str(player_index + 1)
        await self.__tap_guard(lambda: self._song_robot.say_text(cozmo_text).wait_for_completed())

    async def __wait_for_cozmo_to_match_notes(self, current_position: int) -> bool:
        if self._song_robot.num_wrong < MAX_STRIKES:
            notes = self._song.get_sequence_slice(current_position)
            played_correct_sequence, note = await self.__tap_guard(
                lambda: self._song_robot.play_notes(notes, with_error=True)
            )
            if played_correct_sequence:
                await self.__tap_guard(lambda: self.__play_correct_sequence_effect(current_position, self.MEDIUM, is_player=False))
            else:
                self._song_robot.num_wrong += 1
                wrong_cube_id = self._song.get_cube_id(note)
                await self.__tap_guard(lambda: self.__play_wrong_note_effect(wrong_cube_id, is_player=False))
                return False
            return True

    async def __update_if_still_in_game(self) -> None:
        for player in self._players:
            if player.num_wrong == MAX_STRIKES:
                player.did_win = False
        if self._song_robot.num_wrong == MAX_STRIKES:
            self._song_robot.did_win = False

    async def __check_for_game_over(self) -> None:
        num_of_players_out = 0
        for player in self._players:
            if player.num_wrong == MAX_STRIKES:
                num_of_players_out += 1
        if self._song_robot.num_wrong == MAX_STRIKES:
            num_of_players_out += 1
        if num_of_players_out >= len(self._players):
            await self.__tap_guard(lambda: self.__play_end_game_results())

    async def __play_end_game_results(self) -> None:
        winners = ""
        num_of_winners = 0
        for i, player in enumerate(self._players):
            if player.did_win:
                num_of_winners += 1
                if num_of_winners > 1:
                    winners += " and "
                winners += "player " + str(i + 1)
        is_cozmo = True

        if self._song_robot.did_win and num_of_winners == 0:
            winners = "I won"
        elif self._song_robot.did_win:
            winners += " and I won"
        else:
            winners += " won. "
            winners += "I lost."
            is_cozmo = False

        await self.__tap_guard(lambda: self.__play_game_over_effect(winners, is_cozmo=is_cozmo))
        await self.__tap_guard(lambda: self.__play_notes(self._song.get_sequence()))
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

    async def __play_game_over_effect(self, winners, is_cozmo):
        effect = self._effect_factory.create('GameOver')
        await effect.play(winners, is_cozmo=is_cozmo)
        
    async def __play_notes(self, notes: List[Note]) -> None:
        for note in notes:
            await self.__play_note(note)
            await sleep(note.duration)

    async def __play_note(self, note: Note) -> None:
        cube_id = self._song.get_cube_id(note)
        note_cube = NoteCube.of(self._song_robot, cube_id)
        await note_cube.blink_and_play_note()

    def __update_position(self, current_position: int) -> int:
        if current_position < self.MEDIUM or current_position == self._game_length:
            return current_position + 1
        elif current_position < self.LONG:
            current_position += 2
            if current_position > self._game_length:
                current_position = self._game_length
            return current_position
        else:
            current_position += 3
            if current_position > self._game_length:
                current_position = self._game_length
            return current_position
