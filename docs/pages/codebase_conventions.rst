Codebase Conventions
====================
This document aims to explain some of the common conventions found within the Song Match codebase.

Design Patterns
---------------
The Song Match codebase is almost entirely object oriented.
There are many design patterns relating to object oriented programming (OOP) found throughout the codebase.

Wrapper Objects
^^^^^^^^^^^^^^^
The first design pattern you'll see are our use of wrapper objects.
A "wrapper object" is an object that takes an already instantiated object in it's constructor
and extends it's functionality through custom methods.

More formally this is known as the `Decorator Pattern <https://en.wikipedia.org/wiki/Decorator_pattern>`_
because your *decorating* an object by wrapping it and adding behavior.

Common objects from the Cozmo SDK, like the objects representing Cozmo and the cubes,
have a corresponding wrapper object in the Song Match codebase:

* :class:`~song_match.song_robot.SongRobot` wraps :class:`~cozmo.robot.Robot`
* :class:`~song_match.cube.note_cube.NoteCube` wraps :class:`~cozmo.objects.LightCube`
* :class:`~song_match.cube.note_cubes.NoteCubes` wrap a list of 3 :class:`~cozmo.objects.LightCube` instances

Many methods and properties of the wrapper objects match the corresponding wrapped object.
For example, both :class:`~song_match.cube.note_cube.NoteCube`
and :class:`~cozmo.objects.LightCube` have a ``set_lights`` method.
The :meth:`~song_match.cube.note_cube.NoteCube.set_lights` method in ``NoteCube``
simply calls :meth:`~cozmo.objects.LightCube.set_lights` on the internal ``LightCube`` object.

.. code-block:: python

   # note_cube.py

   def set_lights(self, light: Light):
       self._cube.set_lights(light)

Object Creation Patterns
^^^^^^^^^^^^^^^^^^^^^^^^

Static Factory Methods
""""""""""""""""""""""
A *static factory method* is a static method used for creating an object.

There are two *static factory methods* in the codebase.
Both are methods named ``of``, a concise naming convention for static factory methods popularized by ``EnumSet`` in Java.
See `How to name factory like methods? <https://stackoverflow.com/questions/3368830/how-to-name-factory-like-methods>`_ for more details.

* ``NoteCube`` - :meth:`~song_match.cube.note_cube.NoteCube.of`
* ``NoteCubes`` - :meth:`~song_match.cube.note_cubes.NoteCubes.of`

Factories
"""""""""
A `factory <https://en.wikipedia.org/wiki/Factory_(object-oriented_programming)>`_ is an object for creating other objects.

In our codebase there is one factory, :class:`~song_match.effect.factory.EffectFactory` .

:class:`~song_match.effect.factory.EffectFactory` creates our various game effect subclasses:

  * :class:`~song_match.effect.effects.correct_sequence.CorrectSequenceEffect`
    - Played when a player matches the correct notes.
  * :class:`~song_match.effect.effects.round_transition.RoundTransitionEffect`
    - Played when transitioning between game rounds.
  * :class:`~song_match.effect.effects.wrong_note.WrongNoteEffect`
    - Played when a player fails to match the correct notes.


Inheritance
-----------

We favor `composition over inheritance <https://en.wikipedia.org/wiki/Composition_over_inheritance>`_ and avoid complex class hierarchies.

No class extends an instantiable class, but there are two abstract base classes:

* :class:`~song_match.effect.effect.Effect` - Abstract base class for various game effects
* :class:`~song_match.song.song.Song` - Abstract base class for various songs

Public, Protected, and Private
------------------------------
Python lacks access modifiers like ``private`` and ``protected`` found in languages like Java and C#.

We follow the convention of preceding ``private`` methods and attributes with two underscores. For example:

.. code-block:: python

   def __some_private_method():
       pass


``protected`` methods and attributes are preceded with a single underscore.

.. code-block:: python

   def _some_protected_method():
       pass


If you see anything that begins with a underscore, then it means don't use it outside of that class or module.

In general, all ``public`` members in Song Match have docstring comments, while ``private`` and ``protected`` members do not.

Our API reference includes only ``public`` members.

Type Hinting
------------
In general, all functions and methods are type hinted.
Below we see a function that adds two ``int`` values together, and returns an ``int``.

.. code-block:: python

   def add_two_numbers(a: int, b: int) -> int:
       return a + b

See `support for type hints <https://docs.python.org/3/library/typing.html>`_ for more details.

Style Guide
-----------
We follow Python's official style guide `PEP 8 <https://www.python.org/dev/peps/pep-0008/>`_.
