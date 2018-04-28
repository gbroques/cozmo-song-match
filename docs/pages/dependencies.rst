Dependencies
============

This page aims to explain Song Match's dependencies and why we need them.

All project dependencies are listed in
`requirements.txt <https://github.com/gbroques/cozmo-song-match/blob/master/requirements.txt>`_ in the repo.

.. Note:: Transitive dependencies (dependencies of dependencies) are also listed in this file.

This document will go over only primary dependencies.

Cozmo
-----
The first dependency is the Cozmo SDK.

You can find more information on their `documentation <http://cozmosdk.anki.com/docs/>`_.

Package names:

* ``cozmo``

Audio
-----

`PyGame <https://www.pygame.org/docs/>`_ is used for playing audio.

We initialize PyGame's mixer module in :meth:`~song_match.song.note.Note.init_mixer` by calling :func:`pygame.mixer.init`.

Two classes use the :class:`pygame.mixer.Sound` object.

1. :class:`~song_match.song.note.Note`
2. :class:`~song_match.effect.effect.Effect`

Package names:

* ``pygame``


Unit Tests and Coverage Reports
-------------------------------

For running unit tests and generating coverage reports we use `pytest <https://docs.pytest.org/en/latest/>`_,
`pytest-cov <https://pytest-cov.readthedocs.io/en/latest/>`_,
`coverage <https://coverage.readthedocs.io/en/coverage-4.5.1/>`_
and `coveralls <https://coveralls.io/>`_.

Package names:

* ``pytest``
* ``pytest-cov``
* ``coverage``
* ``coveralls``

Documentation
-------------

We use `Sphinx <http://www.sphinx-doc.org/en/master/>`_ to generate our documentation along with a number of other packages.

Package names:

* ``Sphinx``
* ``sphinx-rtd-theme`` - `Read the Docs Sphinx Theme <http://sphinx-rtd-theme.readthedocs.io/en/latest/>`_
* ``better-apidoc`` - A version of `sphinx-apidoc <http://www.sphinx-doc.org/en/stable/man/sphinx-apidoc.html>`_ with support for templating

We also use `Graphviz <https://www.graphviz.org/>`_ to generate inheritance diagrams.
You can download Graphviz `here <https://www.graphviz.org/download/>`_.

The rest of the packages found in ``requirements.txt`` are transitive dependencies.