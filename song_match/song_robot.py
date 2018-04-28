"""Module containing :class:`~song_match.song_robot.SongRobot`."""

from asyncio import sleep
from random import random
from typing import List, Tuple, Union
from cozmo.anim import AnimationTrigger
from cozmo.objects import LightCube1Id, LightCube2Id, LightCube3Id
from cozmo.objects import LightCubeIDs
from cozmo.robot import Robot, world
from cozmo.robot import SayText
from .cube import NoteCube
from .song import Song, Note


class SongRobot:
    """Wrapper class for Cozmo :class:`~cozmo.robot.Robot` instance."""

    _NOTE_DELAY = 0.25  # Time to delay blinking the cube and playing the note
    _SLEEP_TIME = 0.1  # Time to sleep for while animation finishes

    def __init__(self, robot: Robot, song: Song):
        self._robot = robot
        self._song = song
        self._prev_cube_id = LightCube2Id  # Keep track of previously tapped cube
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
            if with_error:
                is_correct, note = await self.play_note_with_error(note, len(notes))
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
        action = await self.__tap_cube(cube_id)
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
        difficulty = .99

        round_difficulty = difficulty ** sequence_length

        cube_id = self._song.get_cube_id(note)

        if round_difficulty < random():
            played_correct_note = False
            cube_id = cube_id % len(LightCubeIDs) + 1
            wrong_note = self._song.get_note(cube_id)
            await self.play_note(wrong_note)
        else:
            await self.play_note(note)

        return played_correct_note, self._song.get_note(cube_id)

    async def turn_back_to_center(self, in_parallel=False) -> None:
        """Turn Cozmo back to the center.

        :param in_parallel: Whether to do the action in parallel or wait until it's completed.
        :return: None
        """
        if in_parallel:
            self._robot.turn_in_place(self._initial_angle, is_absolute=True)
        else:
            await self._robot.turn_in_place(self._initial_angle, is_absolute=True).wait_for_completed()
        self._prev_cube_id = LightCube2Id

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

    async def __tap_cube(self, cube_id) -> AnimationTrigger:
        animation = self.__get_tap_animation(cube_id)
        action = await self.play_animation(animation)
        self._prev_cube_id = cube_id
        return action

    def __get_tap_animation(self, cube_id) -> str:
        """Returns a tap animation based upon the current and previously tapped cubes."""
        point_center = 'anim_memorymatch_pointcenter_01'
        point_small_right = 'anim_memorymatch_pointsmallright_fast_01'
        point_big_right = 'anim_memorymatch_pointbigright_01'
        point_small_left = 'anim_memorymatch_pointsmallleft_fast_01'
        point_big_left = 'anim_memorymatch_pointbigleft_01'
        key = (cube_id, self._prev_cube_id)
        return {
            (LightCube1Id, LightCube1Id): point_center,
            (LightCube1Id, LightCube2Id): point_small_right,
            (LightCube1Id, LightCube3Id): point_big_right,
            (LightCube2Id, LightCube1Id): point_small_left,
            (LightCube2Id, LightCube2Id): point_center,
            (LightCube2Id, LightCube3Id): point_small_right,
            (LightCube3Id, LightCube1Id): point_big_left,
            (LightCube3Id, LightCube2Id): point_small_left,
            (LightCube3Id, LightCube3Id): point_center
        }[key]

    async def play_animation(self, animation_name: str) -> AnimationTrigger:
        return self._robot.play_anim(animation_name, in_parallel=True)

    def say_text(self, text: str) -> SayText:
        """Wrapper method for :meth:`~cozmo.robot.Robot.say_text`.

        :return: :class:`~cozmo.robot.SayText`
        """
        return self._robot.say_text(text)