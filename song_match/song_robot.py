"""Module containing :class:`~song_match.song_robot.SongRobot`."""

from asyncio import TimeoutError
from asyncio import sleep
from random import random
from typing import List, Tuple, Union

from cozmo.anim import Animation
from cozmo.anim import AnimationTrigger
from cozmo.objects import LightCube1Id, LightCube2Id, LightCube3Id
from cozmo.objects import LightCubeIDs
from cozmo.robot import Robot, world
from cozmo.robot import SayText
from cozmo.util import degrees

from song_match.cube_mat import CubeMat
from .cube import NoteCube
from .game_constants import MAX_STRIKES
from .song import Song, Note


class SongRobot:
    """Wrapper class for Cozmo :class:`~cozmo.robot.Robot` instance."""

    _NOTE_DELAY = 0.25  # Time to delay blinking the cube and playing the note
    _SLEEP_TIME = 0.1  # Time to sleep for while animation finishes

    def __init__(self, robot: Robot, song: Song):
        self._robot = robot
        self._song = song
        self._prev_cube_id = None  # Keep track of previously tapped cube
        self._initial_angle = robot.pose_angle
        self.num_wrong = 0  # Keep track of the number of wrong notes Cozmo taps

    async def play_notes(self, notes: List[Note], with_error=False) -> Tuple[bool, Union[None, Note]]:
        """Make Cozmo play a series of notes.

        :param notes: The series of notes to play.
        :param with_error: Whether to play the series of notes with a chance for error.
        :return: Whether cozmo played the correct notes and the incorrect note he played if any.
        :rtype: Tuple[bool, Union[None, Note]]
        """
        for note in notes:
            sequence_length = len(notes)
            error = self.__get_chance_for_error(sequence_length)
            if with_error and error:
                is_correct, note = await self.play_note_with_error(note, sequence_length)
                if not is_correct:
                    return False, note
            else:
                await self.play_note(note)
        return True, None

    async def play_note(self, note: Note) -> None:
        """Make Cozmo play a note.

        :param note: The :class:`~song_match.song.note.Note` to play.
        :return: None
        """
        cube_id = self._song.get_cube_id(note)
        note_cube = NoteCube.of(self, cube_id)
        action = await self.tap_cube(cube_id)
        await sleep(self._NOTE_DELAY)
        await note_cube.blink_and_play_note()
        await action.wait_for_completed()

    async def play_note_with_error(self, note: Note, sequence_length: int = 1) -> Tuple[bool, Note]:
        """Make Cozmo play a :class:`~song_match.song.note.Note` with a chance for error.

        :param note: The :class:`~song_match.song.note.Note` to play.
        :param sequence_length: The length of the sequence to play.
        :return: Whether Cozmo played the correct note, and the :class:`~song_match.song.note.Note` he played.
        :rtype: Tuple[bool, Note]
        """
        played_correct_note = True

        cube_id = self._song.get_cube_id(note)

        error = self.__get_chance_to_play_wrong_note(sequence_length)

        if error:
            played_correct_note = False
            cube_id = cube_id % len(LightCubeIDs) + 1
            wrong_note = self._song.get_note(cube_id)
            await self.play_note(wrong_note)
        else:
            await self.play_note(note)

        return played_correct_note, self._song.get_note(cube_id)

    def __get_chance_to_play_wrong_note(self, sequence_length: int) -> bool:
        difficulty = 0.1
        if self._song.is_sequence_long(sequence_length):
            difficulty *= 1.5
        error = self.__get_chance_for_error(sequence_length, difficulty=difficulty)
        return error

    @staticmethod
    def __get_chance_for_error(sequence_length: int, difficulty: float = .01) -> bool:
        return random() < (difficulty * sequence_length)

    async def turn_back_to_center(self, in_parallel=False) -> None:
        """Turn Cozmo back to the center.

        :param in_parallel: Whether to do the action in parallel or wait until it's completed.
        :return: None
        """
        if in_parallel:
            self._robot.turn_in_place(self._initial_angle, is_absolute=True)
        else:
            await self._robot.turn_in_place(self._initial_angle, is_absolute=True).wait_for_completed()
        self._prev_cube_id = self.__get_middle_cube_id()

    async def turn_to_cube(self, cube_id: int) -> None:
        """Make Cozmo turn in place until the specified cube is visible.

        :param cube_id: :attr:`~cozmo.objects.LightCube.cube_id` to turn to.
        :return: None
        """
        timeout = 0.1
        try:
            cube = await self.world.wait_for_observed_light_cube(timeout=timeout)
        except TimeoutError:
            cube = None  # Didn't find cube

        while cube is None or cube.cube_id != cube_id:
            await self._robot.turn_in_place(degrees(30)).wait_for_completed()

            try:
                cube = await self.world.wait_for_observed_light_cube(timeout=timeout)
            except TimeoutError:
                cube = None  # Didn't find cube

            if cube is not None and cube.cube_id == cube_id:
                break

    @property
    def did_win(self) -> bool:
        """Property for accessing whether Cozmo won the game.

        :return: Whether Cozmo won the game.
        """
        return self.num_wrong < MAX_STRIKES

    @property
    def world(self) -> world:
        """Property for accessing :attr:`~cozmo.robot.Robot.world`."""
        return self._robot.world

    @property
    def robot(self) -> Robot:
        """Property for accessing :class:`~cozmo.robot.Robot`."""
        return self._robot

    @property
    def song(self) -> Song:
        """Property for accessing :class:`~song_match.song.song.Song`."""
        return self._song

    async def tap_cube(self, cube_id) -> Animation:
        """Make Cozmo tap a cube.

        :param cube_id: :attr:`~cozmo.objects.LightCube.cube_id`
        :return: :class:`~cozmo.anim.Animation`
        """
        if self._prev_cube_id is None:
            self._prev_cube_id = self.__get_middle_cube_id()
        animation = self.__get_tap_animation(cube_id)
        self._prev_cube_id = cube_id
        return await self.play_anim(animation, in_parallel=True)

    @staticmethod
    def __get_middle_cube_id() -> int:
        mat_positions = CubeMat.get_positions()
        return mat_positions[1]

    def __get_tap_animation(self, cube_id) -> str:
        """Returns a tap animation based upon the current and previously tapped cubes."""
        animation_lookup = self.__get_tap_animation_lookup()
        key = (cube_id, self._prev_cube_id)
        return animation_lookup[key]

    @staticmethod
    def __get_tap_animation_lookup() -> dict:
        """Build a tap animation lookup dictionary.

        The key is (cube_id, prev_cube_id),
        where cube_id is the ID of the cube Cozmo is tapping,
        and prev_cube_id is the ID of the previously tapped cube.

        There are 5 animations:
        1. center
        2. small right
        3. big right
        4. small left
        5. big left

        :return: The animation to tap the cube.
        """
        mat_positions = CubeMat.get_positions()

        # Build center animations
        keys = [(LightCube1Id, LightCube1Id),
                (LightCube2Id, LightCube2Id),
                (LightCube3Id, LightCube3Id)]
        center = 'anim_memorymatch_pointcenter_01'
        animations = [center, center, center]

        # Build small right animations
        first_two_elements = tuple(mat_positions[:-1])
        last_two_elements = tuple(mat_positions[-2:])
        keys.append(first_two_elements)
        keys.append(last_two_elements)
        small_right = 'anim_memorymatch_pointsmallright_fast_01'
        animations.append(small_right)
        animations.append(small_right)

        # Build big right animations
        first_and_last_elements = tuple([mat_positions[0], mat_positions[-1]])
        keys.append(first_and_last_elements)
        big_right = 'anim_memorymatch_pointbigright_01'
        animations.append(big_right)

        # Build small left animations
        first_two_elements_reversed = tuple(mat_positions[:-1][::-1])  # ::-1 reverses the order
        last_two_elements_reversed = tuple(mat_positions[-2:][::-1])
        keys.append(first_two_elements_reversed)
        keys.append(last_two_elements_reversed)
        small_left = 'anim_memorymatch_pointsmallleft_fast_01'
        animations.append(small_left)
        animations.append(small_left)

        # Build big left animations
        first_and_last_elements_reversed = tuple([mat_positions[0], mat_positions[-1]][::-1])
        keys.append(first_and_last_elements_reversed)
        big_left = 'anim_memorymatch_pointbigleft_01'
        animations.append(big_left)

        animation_lookup = dict(zip(keys, animations))
        return animation_lookup

    async def play_anim(self, animation_name: str, **kwargs) -> Animation:
        """Wrapper method for :meth:`~cozmo.robot.Robot.play_anim`.

        :param animation_name: The name of the animation.
        :param kwargs: See :meth:`~cozmo.robot.Robot.play_anim`.
        :return: :class:`~cozmo.anim.Animation`
        """
        return self._robot.play_anim(animation_name, **kwargs)

    def play_anim_trigger(self, animation_trigger, **kwargs) -> AnimationTrigger:
        """Wrapper method for :meth:`~cozmo.robot.Robot.play_anim_trigger`.

        :param animation_trigger: The animation trigger.
        :param kwargs: See :meth:`~cozmo.robot.Robot.play_anim_trigger`.
        :return: :class:`~cozmo.anim.AnimationTrigger`
        """
        return self._robot.play_anim_trigger(animation_trigger, **kwargs)

    def say_text(self, text: str) -> SayText:
        """Wrapper method for :meth:`~cozmo.robot.Robot.say_text`.

        :return: :class:`~cozmo.robot.SayText`
        """
        return self._robot.say_text(text)
