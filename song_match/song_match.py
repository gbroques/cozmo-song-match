"""Module containing :class:`~song_match.song_match.SongMatch`."""

from asyncio import sleep
from sys import exit
from typing import Callable, List

from cozmo.objects import EvtObjectTapped
from cozmo.robot import Robot

from song_match.cube import NoteCube
from song_match.cube import NoteCubes
from .config import init_mixer
from .effect import EffectFactory
from .game_constants import MAX_STRIKES
from .game_constants import STARTING_POSITION
from .game_constants import TIME_IN_BETWEEN_PLAYERS_AND_COZMO
from .option_prompter import OptionPrompter
from .player import Player
from .song import MaryHadALittleLamb
from .song import Note
from .song import Song
from .song_robot import SongRobot


class SongMatch:
    """Main game class."""

    def __init__(self, song: Song = None, num_players: int = None):
        self._song = MaryHadALittleLamb() if song is None else song
        self._num_players = num_players

        self._song_robot = None
        self._note_cubes = None
        self._effect_factory = None
        self._players = None

        self._prevent_tap = True  # Flag to prevent player from interrupting game by tapping cubes
        self._played_final_round = False  # Keep track of whether the final round has been played

        init_mixer()

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
        self._players = await self.__setup_players(self._song_robot)
        await self.__setup()
        await self.__init_game_loop()

    async def __setup_players(self, song_robot: SongRobot) -> List[Player]:
        num_players = self._num_players
        if num_players is None:
            num_players = await self.__get_number_of_players(song_robot)
        return self.__get_players(num_players)

    @staticmethod
    def __get_players(num_players: int):
        return [Player(i) for i in range(1, num_players + 1)]

    async def __setup(self) -> None:
        await self._song_robot.world.wait_until_num_objects_visible(3)
        self._song_robot.world.add_event_handler(EvtObjectTapped, self.__tap_handler)
        self._note_cubes.turn_on_lights()

    @staticmethod
    async def __get_number_of_players(song_robot: SongRobot) -> int:
        prompt = 'How many players?'
        options = ['One?', 'Two?', 'Three?']
        option_prompter = OptionPrompter(song_robot)
        return await option_prompter.get_option(prompt, options)

    async def __tap_handler(self, evt, obj=None, tap_count=None, **kwargs) -> None:
        if self._prevent_tap:
            return
        cube = evt.obj
        note_cube = NoteCube(cube, self._song)
        await note_cube.blink_and_play_note()

    async def __init_game_loop(self) -> None:
        current_position = STARTING_POSITION
        while self._song.is_not_finished(current_position):
            await self.__play_round_transition_effect()

            notes = self._song.get_sequence_slice(current_position)
            await self.__play_notes(notes)

            await self.__wait_for_players_to_match_notes(current_position)

            await sleep(TIME_IN_BETWEEN_PLAYERS_AND_COZMO)

            await self.__wait_for_cozmo_to_match_notes(current_position)

            await self.__check_for_game_over()

            current_position = self.__update_position(current_position)

        await self.__play_end_game_results()

    async def __wait_for_players_to_match_notes(self, current_position: int) -> None:
        for i, player in enumerate(self._players):
            if player.num_wrong < MAX_STRIKES:
                await self.__player_turn_prompt(player)
                await self.__wait_for_player_to_match_notes(current_position, i)
        await self.__check_for_game_over()

    async def __wait_for_player_to_match_notes(self, current_position: int, player_index: int) -> None:
        num_notes_played = 0
        notes = self._song.get_sequence_slice(current_position)
        while num_notes_played != current_position:
            event = await self.__lift_tap_guard(lambda: self._song_robot.world.wait_for(EvtObjectTapped))
            tapped_cube = NoteCube(event.obj, self._song)
            correct_note = notes[num_notes_played]

            if tapped_cube.note != correct_note:
                self._players[player_index].num_wrong += 1
                await self.__play_wrong_note_effect(tapped_cube.cube_id)
                return

            num_notes_played += 1

        await self.__play_correct_sequence_effect(current_position)

    async def __lift_tap_guard(self, callable_function: Callable):
        self._prevent_tap = False
        result = await callable_function()
        self._prevent_tap = True
        return result

    async def __player_turn_prompt(self, player: Player) -> None:
        if len(self._players) > 1:
            prompt = str(player)
            await self._song_robot.say_text(prompt).wait_for_completed()

    async def __wait_for_cozmo_to_match_notes(self, current_position: int) -> None:
        if self._song_robot.num_wrong < MAX_STRIKES:
            notes = self._song.get_sequence_slice(current_position)
            played_correct_sequence, note = await self._song_robot.play_notes(notes, with_error=True)
            if played_correct_sequence:
                await self.__play_correct_sequence_effect(current_position, is_player=False)
            else:
                self._song_robot.num_wrong += 1
                wrong_cube_id = self._song.get_cube_id(note)
                await self.__play_wrong_note_effect(wrong_cube_id, is_player=False)

    async def __check_for_game_over(self) -> None:
        all_players = self._players + [self._song_robot]
        out_of_game_players = self.__get_out_of_game_players(all_players)
        num_of_players_out_of_game = len(out_of_game_players)
        if num_of_players_out_of_game >= len(self._players):
            await self.__play_end_game_results()

    @staticmethod
    def __get_out_of_game_players(all_players: list) -> list:
        return [player for player in all_players if player.num_wrong == MAX_STRIKES]

    async def __play_end_game_results(self) -> None:
        winners = await self.__get_winners()
        await self.__play_game_over_effect(winners, did_cozmo_win=self._song_robot.did_win)
        await self.__play_notes(self._song.get_sequence())
        exit(0)

    async def __get_winners(self) -> List[Player]:
        return [player for player in self._players if player.did_win]

    async def __play_wrong_note_effect(self, cube_id: int, is_player=True) -> None:
        effect = self._effect_factory.create('WrongNote')
        await effect.play(cube_id, is_player=is_player)

    async def __play_correct_sequence_effect(self, current_position: int, is_player=True) -> None:
        is_sequence_long = self._song.is_sequence_long(current_position)
        effect = self._effect_factory.create('CorrectSequence')
        await effect.play(is_sequence_long=is_sequence_long, is_player=is_player)

    async def __play_round_transition_effect(self) -> None:
        effect = self._effect_factory.create('RoundTransition')
        await effect.play()

    async def __play_game_over_effect(self, winners: List[Player], did_cozmo_win: bool) -> None:
        effect = self._effect_factory.create('GameOver')
        await effect.play(winners, did_cozmo_win=did_cozmo_win)

    async def __play_notes(self, notes: List[Note]) -> None:
        for note in notes:
            await self.__play_note(note)
            await sleep(note.duration)

    async def __play_note(self, note: Note) -> None:
        cube_id = self._song.get_cube_id(note)
        note_cube = NoteCube.of(self._song_robot, cube_id)
        await note_cube.blink_and_play_note()

    def __update_position(self, current_position: int) -> int:
        current_position = self.__increment_current_position(current_position)
        return self.__round_current_position(current_position)

    def __increment_current_position(self, current_position: int) -> int:
        medium, long = self._song.get_difficulty_markers()
        if current_position < medium:
            current_position += 1
        elif current_position < long:
            current_position += 2
        else:
            current_position += 3
        return current_position

    def __round_current_position(self, current_position) -> int:
        song_length = self._song.length
        if current_position >= song_length and not self._played_final_round:
            self._played_final_round = True
            return song_length
        elif self._played_final_round:
            return song_length + 1  # The main loop only exits when current position is greater than song length
        else:
            return current_position
