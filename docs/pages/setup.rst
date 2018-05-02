Setup
=====

1. Setup the Cozmo SDK.

  * Please see `Initial Setup <http://cozmosdk.anki.com/docs/initial.html>`_ under the Cozmo SDK documentation.

2. Clone the repository.

::

$ git clone https://github.com/gbroques/cozmo-song-match.git

3. Navigate to the repository.

::

$ cd cozmo-song-match

4. Install dependencies.

::

$ pip install -r requirements.txt

.. Tip:: We recommend installing dependencies within a virtual environment. See `Virtual Environments <virtualenv.html>`_ for details.

5. With Cozmo connected, run the main program. For details on connecting Cozmo, see `Getting Started With the Cozmo SDK <http://cozmosdk.anki.com/docs/getstarted.html>`_.

::

$ python main.py

We support command line arguments for configuring what song you want to play, and how many players.
Use the help flag ``-h`` for help.

::

    $ python main.py -h

    usage: main.py [-h] [-s S] [-p N]

    Play Song Match with Cozmo.

    optional arguments:
      -h, --help  show this help message and exit
      -s S        The song to play. Hot Cross Buns (hcb), Mary Had A Little Lamb
                  (mhall), or Rain Rain Go Away (rrga). Defaults to a random song.
      -p N        The number of players for the game. Defaults to None. If None
                  then selecting the number of players will be handled in game.


6. `Download and Install PyCharm <https://www.jetbrains.com/pycharm/download/>`_ (Optional)

  * See `why we recommend you develop with PyCharm <pycharm.html>`_
