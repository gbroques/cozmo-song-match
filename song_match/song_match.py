"""Module containing :class:`~song_match.song_match.SongMatch`."""

from cozmo.objects import EvtObjectTapped
from cozmo.robot import Robot

from song_match.cube import NoteCube
from song_match.cube import NoteCubes
from .song import MaryHadALittleLamb
from .song import Note
from .song_robot import SongRobot


class SongMatch:
    """Main game class."""

    def __init__(self):
        self._robot = None
        self._tappedNoteIndex = 0
        self._cozmoError = True
        self._song = MaryHadALittleLamb()
        Note.init_mixer()

    async def play(self, robot: Robot) -> None:
        """Play the Song Match game.

        Pass this function into :func:`cozmo.run_program`.

        :param robot: Cozmo Robot instance.
        :type robot: :class:`~cozmo.robot.Robot`
        :return: None
        """
        self._robot = SongRobot(robot, self._song)
        await self.__setup()
        await self.__init_game_loop()

    async def __setup(self) -> None:
        await self._robot.world.wait_until_num_objects_visible(3)
        self._robot.world.add_event_handler(EvtObjectTapped, self.__tap_handler)

        self.__turn_on_cube_lights()

        # notes = [Note('E4'), Note('D4'), Note('C4')]
        # await self._robot.play_notes(notes)

    async def __tap_handler(self, evt, obj=None, tap_count=None, **kwargs):
        cube = evt.obj
        note_cube = NoteCube(cube, self._song)
        notes = self._song._notes
        self._tappedNoteIndex = note_cube._cube.cube_id - 1
        print("Tap Handler: " + str(self._tappedNoteIndex))
        await self._robot.play_note(notes[note_cube._cube.cube_id - 1])

    def __turn_on_cube_lights(self) -> None:
        note_cubes = NoteCubes(self.__get_cubes(), self._song)
        note_cubes.turn_on_lights()

    def __flash_cubes_red(self) -> None:
        note_cubes = NoteCubes(self.__get_cubes(), self._song)
        note_cubes.flash_lights_red()

    def __get_cubes(self):
        """Convenience method to get the light cubes."""
        return self._robot.world.light_cubes.values()

    async def __init_game_loop(self) -> None:
        gameContinue = True
        roundCounter = 3
        notes = self._song._notes
        song = self._song._sequence

        while gameContinue:
            print("Beginning of round!")
            game = 0
            player = 0
            coz = 0
            # the notes are played for the player to repeat
            while roundCounter <= len(song) and game < roundCounter:
                await self._robot.play_note_notap(song[game])
                game += 1

            # the user repeats the notes
            while player < game and gameContinue:
                await self._robot.world.wait_for(EvtObjectTapped)

                gameContinue = self._robot.compareNotes(notes[self._tappedNoteIndex], song[player])
                if gameContinue:
                    player += 1
                    print("Game continues")

                else:
                    print("Game over: Cozmo wins!")
                    self.__flash_cubes_red()
                    self.__flash_cubes_red()

            # Cozmo repeats the notes
            while coz < game and gameContinue and self._cozmoError:
                gameContinue = await self._robot.play_note_with_error(song[coz], coz)
                if gameContinue:
                    coz += 1
                    print("Game continues")

                else:
                    print("Game over: Player wins!")
                    self.__flash_cubes_red()
                    self.__flash_cubes_red()
            roundCounter += 1

            # Condition for the player winning the game at the end
            if game == len(song) and gameContinue:
                print("Player wins!")
                gameContinue = False