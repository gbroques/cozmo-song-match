.. Song Match documentation master file, created by
   sphinx-quickstart on Tue Mar 27 12:56:42 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. image:: _static/banner.png

|

========================
Song Match Documentation
========================

Welcome to the documentation for the Cozmo Song Match project!

Song Match is a game where you try to match the notes of a song by tapping blocks with Cozmo.
With each round, the game gets longer and a little harder. Song Match supports up to 3 players.

.. raw:: html

   <iframe width="560" height="315" style="margin-bottom: 25px;" src="https://www.youtube.com/embed/videoseries?list=PLesiP49zG6skUxroov9oCfs_aiWAZ3bYs" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>

Song Match is brought to you by four undergraduate students from the University of Missouri - St. Louis.
Collectively, we are `The Cozmonauts <pages/the_cozmonauts.html>`_.

How It Works
------------
The game starts by playing the first three notes of a song.
Each time a note is played, a corresponding cube flashes.
The player must match the notes by tapping the correct sequence of cubes.
If the player gets the sequence correct, then Cozmo tries to match the correct sequence.
If either the player or Cozmo gets *three* notes incorrect, then they lose the game.

This makes up **one** round.
Each round the length of the sequence increases, until you reach the end of the song.

Please view our `User's Guide <_static/SongMatch.pdf>`_ for detailed information on how to play the game.

:download:`Download User's Guide <_static/SongMatch.pdf>`

Also, for some ideas on how to pitch the game to children, check out our `Educator's Guide <_static/Educator_Guide.pdf>`_.

:download:`Download Educator's Guide <_static/Educator_Guide.pdf>`

.. toctree::
   :caption: Getting Started
   :maxdepth: 2

   pages/setup
   pages/virtualenv
   pages/pycharm
   pages/codebase_conventions
   pages/package_structure
   pages/game_flow.rst

.. toctree::
   :maxdepth: 2
   :caption: Song Match API

   song_match/song_match

.. toctree::
   :maxdepth: 2
   :caption: Dependencies

   pages/dependencies
   pages/graphic_assets

.. toctree::
   :maxdepth: 1
   :caption: Troubleshooting

   pages/troubleshooting

.. toctree::
   :maxdepth: 1
   :caption: Future Expansion

   pages/moving_forward

.. toctree::
   :maxdepth: 1
   :caption: About

   pages/the_cozmonauts
   README


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
